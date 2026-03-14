"""
Memory system using SQLite with token tracking and summarization.
"""

import asyncio
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import tiktoken
from openai import AsyncOpenAI


class MemoryDB:
    """Manages conversation memory in SQLite with summarization."""

    def __init__(self, db_path: str, openai_client: Optional[AsyncOpenAI] = None):
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()
        self.encoding = tiktoken.get_encoding("cl100k_base")  # OpenAI tokenizer
        self.openai_client = openai_client

    def _init_schema(self) -> None:
        """Create database schema if not exists."""
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,  -- 'user' or 'assistant'
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    tokens INTEGER DEFAULT 0,
                    summary_id INTEGER NULL
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    start_id INTEGER NOT NULL,
                    end_id INTEGER NOT NULL,
                    token_count INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (start_id) REFERENCES conversations(id),
                    FOREIGN KEY (end_id) REFERENCES conversations(id)
                )
                """
            )
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON conversations(timestamp)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_summary_id ON conversations(summary_id)")

    def _count_tokens(self, text: str) -> int:
        """Count tokens in text using OpenAI's tokenizer."""
        return len(self.encoding.encode(text))

    def add_message(self, role: str, content: str) -> int:
        """Add a message to memory and return its ID."""
        tokens = self._count_tokens(content)
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO conversations (role, content, tokens) VALUES (?, ?, ?)",
                (role, content, tokens)
            )
            msg_id = cursor.lastrowid
            return msg_id

    async def maybe_summarize(self) -> None:
        """Check if summarization is needed and perform it if so."""
        total_tokens = self._get_total_tokens()
        if total_tokens > self._get_threshold():
            await self._create_summary()

    def get_all_messages(self, limit: Optional[int] = None) -> List[sqlite3.Row]:
        """Retrieve all messages for context building."""
        query = "SELECT * FROM conversations ORDER BY id ASC"
        if limit:
            query += f" LIMIT {limit}"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def get_recent_messages(self, max_tokens: int) -> List[sqlite3.Row]:
        """Get recent messages fitting within token limit, including summaries."""
        # Start with raw messages
        messages = []
        total_tokens = 0

        cursor = self.conn.execute("SELECT * FROM conversations ORDER BY id DESC")
        all_rows = cursor.fetchall()

        for row in reversed(all_rows):  # Process from oldest to newest
            is_summary = row["summary_id"] is not None
            tokens = row["tokens"]

            # If total + tokens exceeds limit, stop
            if total_tokens + tokens > max_tokens:
                break

            messages.append(row)
            total_tokens += tokens

        return list(reversed(messages))  # Return in chronological order

    async def _create_summary(self) -> None:
        """Summarize old messages and replace them with a summary."""
        # Get messages to summarize (oldest ones)
        cursor = self.conn.execute(
            "SELECT id, role, content FROM conversations WHERE summary_id IS NULL ORDER BY id ASC LIMIT 10"
        )
        messages = cursor.fetchall()

        if len(messages) < 3:  # Need at least 3 messages to summarize
            return

        start_id = messages[0]["id"]
        end_id = messages[-1]["id"]

        # Build summary text - try AI first, fallback to simple
        try:
            if self.openai_client:
                summary_text = await self._generate_ai_summary(messages)
            else:
                summary_text = self._generate_summary_text(messages)
        except Exception:
            # Fallback to simple summary on any error
            summary_text = self._generate_summary_text(messages)

        summary_tokens = self._count_tokens(summary_text)

        # Store summary
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO summaries (content, start_id, end_id, token_count) VALUES (?, ?, ?, ?)",
                (summary_text, start_id, end_id, summary_tokens)
            )
            summary_id = cursor.lastrowid

            # Mark original messages as summarized
            ids = [str(row["id"]) for row in messages]
            self.conn.execute(
                f"UPDATE conversations SET summary_id = ? WHERE id IN ({','.join(ids)})",
                (summary_id,)
            )

    def _get_total_tokens(self) -> int:
        """Get total tokens in conversation history (excluding summaries)."""
        cursor = self.conn.execute("SELECT SUM(tokens) FROM conversations WHERE summary_id IS NULL")
        result = cursor.fetchone()[0]
        return result or 0

    def _get_threshold(self) -> int:
        """Get summarization threshold from config."""
        from cupid.config import config
        return config.summarization_threshold

    def _create_summary(self) -> None:
        """Summarize old messages and replace them with a summary."""
        # Get messages to summarize (oldest ones)
        cursor = self.conn.execute(
            "SELECT id, role, content FROM conversations WHERE summary_id IS NULL ORDER BY id ASC LIMIT 10"
        )
        messages = cursor.fetchall()

        if len(messages) < 3:  # Need at least 3 messages to summarize
            return

        start_id = messages[0]["id"]
        end_id = messages[-1]["id"]

        # Build summary text - try AI first, fallback to simple
        try:
            if self.openai_client:
                summary_text = asyncio.run(self._generate_ai_summary(messages))
            else:
                summary_text = self._generate_summary_text(messages)
        except Exception:
            # Fallback to simple summary on any error
            summary_text = self._generate_summary_text(messages)

        summary_tokens = self._count_tokens(summary_text)

        # Store summary
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO summaries (content, start_id, end_id, token_count) VALUES (?, ?, ?, ?)",
                (summary_text, start_id, end_id, summary_tokens)
            )
            summary_id = cursor.lastrowid

            # Mark original messages as summarized
            ids = [str(row["id"]) for row in messages]
            self.conn.execute(
                f"UPDATE conversations SET summary_id = ? WHERE id IN ({','.join(ids)})",
                (summary_id,)
            )

    def _generate_summary_text(self, messages: List[sqlite3.Row]) -> str:
        """Create a brief summary of conversation thread."""
        # Simple summary: list of exchanges
        lines = ["Conversation summary:"]
        for row in messages:
            prefix = "User:" if row["role"] == "user" else "Cupid:"
            content = row["content"][:100] + ("..." if len(row["content"]) > 100 else "")
            lines.append(f"{prefix} {content}")
        return "\n".join(lines)

    async def _generate_ai_summary(self, messages: List[sqlite3.Row]) -> str:
        """Generate an intelligent summary using OpenAI."""
        # Build conversation text
        conversation = []
        for row in messages:
            prefix = "User" if row["role"] == "user" else "Cupid"
            conversation.append(f"{prefix}: {row['content']}")

        prompt = """Summarize this conversation in 1-2 concise sentences. Focus on:
- Main topic or intent
- Key details or emotions expressed
- Any decisions or outcomes

Keep it brief and neutral. Don't use "User:" or "Cupid:" in the summary."""

        response = await self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "\n".join(conversation)}
            ],
            temperature=0.3,
            max_tokens=100,
        )

        summary = response.choices[0].message.content.strip()
        return f"[AI Summary]: {summary}"

    def clear(self) -> None:
        """Clear all conversations and summaries."""
        with self.conn:
            self.conn.execute("DELETE FROM conversations")
            self.conn.execute("DELETE FROM summaries")

    def get_stats(self) -> dict:
        """Get conversation statistics."""
        cursor = self.conn.execute("SELECT COUNT(*) FROM conversations")
        total_messages = cursor.fetchone()[0]

        cursor = self.conn.execute("SELECT COUNT(*) FROM summaries")
        total_summaries = cursor.fetchone()[0]

        cursor = self.conn.execute("SELECT SUM(tokens) FROM conversations")
        total_tokens = cursor.fetchone()[0] or 0

        cursor = self.conn.execute("SELECT COUNT(*) FROM conversations WHERE summary_id IS NOT NULL")
        summarized_messages = cursor.fetchone()[0]

        return {
            "total_messages": total_messages,
            "total_summaries": total_summaries,
            "total_tokens": total_tokens,
            "summarized_messages": summarized_messages,
            "active_messages": total_messages - summarized_messages
        }

    def close(self) -> None:
        """Close database connection."""
        self.conn.close()

    def build_context_messages(self, max_tokens: int) -> List[dict]:
        """Build context messages for LLM including summaries."""
        rows = self.get_recent_messages(max_tokens)
        messages = []

        for row in rows:
            if row["summary_id"] is not None:
                # This is a summary row
                messages.append({"role": "system", "content": f"[Earlier conversation summary]: {row['content']}"})
            else:
                messages.append({"role": row["role"], "content": row["content"]})

        return messages
