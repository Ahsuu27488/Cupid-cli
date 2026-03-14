#!/usr/bin/env python3
"""
Quick verification script for Cupid.
Tests that everything is set up correctly before chatting.
"""

import sys
from cupid.config import config
from cupid.agent import SupportAgent
from cupid.memory import MemoryDB

def test_setup():
    print("🔍 Verifying Cupid setup...\n")

    # Test 1: Config
    print("1️⃣  Configuration")
    try:
        config.validate()
        print("   ✅ OPENAI_API_KEY is set")
        print(f"   ✅ Model: {config.model}")
    except ValueError as e:
        print(f"   ❌ Configuration error: {e}")
        print("\n💡 Fix: Create .env file with OPENAI_API_KEY")
        return False

    # Test 2: Database
    print("\n2️⃣  Database")
    try:
        mem = MemoryDB(config.memory_db_path)
        stats = mem.get_stats()
        print(f"   ✅ Database accessible: {config.memory_db_path}")
        print(f"   ✅ Current messages: {stats['total_messages']}")
        mem.close()
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False

    # Test 3: Agent
    print("\n3️⃣  AI Agent")
    try:
        agent = SupportAgent()
        print("   ✅ Agent created")
        print("   ✅ OpenAI client connected")
        agent.close()
    except Exception as e:
        print(f"   ❌ Agent error: {e}")
        return False

    print("\n" + "=" * 50)
    print("✅ ALL CHECKS PASSED! Cupid is ready! 💕")
    print("=" * 50)
    print("\n🚀 Run: python -m cupid.main")
    return True

if __name__ == "__main__":
    success = test_setup()
    sys.exit(0 if success else 1)
