"""
Configuration management for Cupid.
Loads environment variables and provides app settings.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Application configuration"""

    # OpenAI API
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    model: str = os.getenv("MODEL", "gpt-4o-mini")

    # Memory
    max_context_tokens: int = int(os.getenv("MAX_CONTEXT_TOKENS", "2000"))
    summarization_threshold: int = int(os.getenv("SUMMARIZATION_THRESHOLD", "1500"))
    memory_db_path: str = os.getenv("MEMORY_DB", "memory.db")

    # Personality
    default_mood: str = os.getenv("DEFAULT_MOOD", "flirty")
    max_response_tokens: int = int(os.getenv("MAX_RESPONSE_TOKENS", "150"))

    def validate(self) -> None:
        """Validate required configuration"""
        if not self.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY not set. Please create a .env file with your OpenAI API key.\n"
                "Get your key from: https://platform.openai.com/api-keys"
            )


# Global config instance
config = Config()
