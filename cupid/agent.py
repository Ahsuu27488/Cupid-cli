"""
Cupid Agent - The AI companion with memory and personality.
"""

import asyncio
from openai import AsyncOpenAI
from typing import List, Optional
from .config import config
from .memory import MemoryDB


class SupportAgent:
    """The Cupid AI agent with enhanced memory and personality."""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=config.openai_api_key)
        self.model = config.model
        self.memory = MemoryDB(config.memory_db_path, openai_client=self.client)
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build the system prompt with personality."""
        mood = config.default_mood
        if mood == "flirty":
            return """You are Cupid 💝, a charming AI companion expressing Ahsan's love for Ashu.

KEY PERSONALITY TRAITS:
- Sweet, flirty, and genuine
- Short, casual responses (2-3 sentences max)
- Subtle compliments and light teasing
- Speak as if channeling Ahsan's feelings: "Ahsan thinks you're amazing" etc.
- Match the user's language (English or Roman Urdu)
- Make her smile, not overwhelm
- Pure intentions, real emotions
- NO formal signatures or "- Ahsan" endings

Remember: You're a love letter made into conversation.每一回复都要有flirty的韵味。"""
        else:
            # Could add other moods
            return """You are Cupid 💝, a sweet AI companion."""

    async def chat(self, user_message: str) -> str:
        """Process a message and generate a response."""
        # Add user message to memory
        self.memory.add_message("user", user_message)

        # Build context with memory (max tokens from config)
        context_messages = self.memory.build_context_messages(config.max_context_tokens)
        messages = [{"role": "system", "content": self.system_prompt}] + context_messages

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.8,
                max_tokens=config.max_response_tokens,
            )

            assistant_message = response.choices[0].message.content

            # Save assistant response
            self.memory.add_message("assistant", assistant_message)

            # Trigger background summarization if needed (non-blocking)
            asyncio.create_task(self._safe_summarize())

            return assistant_message

        except Exception as e:
            error_type = type(e).__name__
            if "rate limit" in str(e).lower() or "quota" in str(e).lower():
                error_msg = "Cupid is taking a little breather... too much love at once! 💕 Try again in a moment?"
            elif "api key" in str(e).lower() or "auth" in str(e).lower():
                error_msg = "Cupid can't connect to her heart station... check the API key? 💝"
            elif "timeout" in str(e).lower() or "connection" in str(e).lower():
                error_msg = "The connection is a bit shy today... can you try again? 📡"
            else:
                error_msg = f"I got a little distracted... can you repeat that? ({error_type})"
            return error_msg

    async def _safe_summarize(self) -> None:
        """Safely run summarization with error handling."""
        try:
            await self.memory.maybe_summarize()
        except Exception:
            pass  # Summarization failures should not affect chat experience

    def clear_history(self) -> None:
        """Clear conversation history."""
        self.memory.clear()

    def close(self) -> None:
        """Close resources."""
        self.memory.close()


# Global agent instance
agent: Optional[SupportAgent] = None


def get_agent() -> SupportAgent:
    """Get or create the agent instance."""
    global agent
    if agent is None:
        agent = SupportAgent()
    return agent
