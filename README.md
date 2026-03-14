# 💝 For Ashu - Cupid

Welcome! This is a special AI companion named **Cupid**, created just for you by Ahsan. It's designed to chat with you, flirt a little, and brighten your day with charm and genuine affection.

## 🎯 What is Cupid?

A smart Python chatbot that uses OpenAI's GPT to respond with charming, flirty replies. Cupid:

- 💬 **Remembers your conversations** with smart AI-powered summarization
- 🌍 **Speaks both English and Roman Urdu** - matches your language automatically
- 🧠 **Has long-term memory** using SQLite - conversations persist between sessions
- ✨ **Keeps it real** - short, sweet responses with Ahsan's genuine affection
- 📊 **Conversation stats** - see how much you've chatted

## 🚀 Quick Setup (Automatic Installation)

The easiest way to install Cupid - just one command:

```bash
git clone https://github.com/Ahsuu27488/Cupid-cli.git
cd Cupid-cli
bash setup_cupid
```

The **`setup_cupid`** script will:
- ✅ Detect your platform (Termux/Linux/macOS)
- ✅ Install Python dependencies automatically
- ✅ Prompt for your OpenAI API key (securely)
- ✅ Create the `cupid` command (works from **anywhere**!)
- ✅ Test the installation

After setup completes, simply run:

```bash
cupid
```

That's it! No need to remember complex commands. 💕

### What does the setup script do?

1. Checks for Python and installs if missing (Termux)
2. Creates a virtual environment
3. Installs all required packages
4. Configures your `.env` file with API key
5. Creates a global `cupid` command symlink
6. Verifies everything works

### Platform-Specific Notes

**📱 Termux (Android):**
- Works perfectly! The `cupid` command will be placed in Termux's bin directory
- Run `cupid` from any folder

**🖥️ Linux/macOS:**
- The `cupid` command will be linked to `~/.local/bin/cupid`
- You may need to add `~/.local/bin` to your PATH (the installer will prompt you)

### Manual Setup (Advanced)

If you prefer manual control or the script doesn't work:

#### Using UV (recommended for developers):

```bash
git clone https://github.com/Ahsuu27488/Cupid-cli.git
cd Cupid-cli
uv sync
```

#### Using PIP:

```bash
git clone https://github.com/Ahsuu27488/Cupid-cli.git
cd Cupid-cli
pip install -r requirements.txt
```

Then configure your `.env` file:

```env
OPENAI_API_KEY=your_key_here
MODEL=gpt-4o-mini
```

Get your API key from: https://platform.openai.com/api-keys

### Running Cupid

**After automatic setup:**

```bash
cupid
```

**After manual setup:**

```bash
python -m cupid.main
```

**Important:** Never run `python main.py` from inside the `cupid/` folder - that causes import errors! Always run from the project root.

## 💬 Example Conversation

```
You: Hey! How are you?
Cupid: Doing great, especially knowing you're here! 😊

You: I had a tough day at work
Cupid: Oh no, I'm sorry to hear that 😔 Tell me more, babe. I'm here to listen.
```

## 🌍 Languages Supported

- **English** - Type normally
- **Roman Urdu** - e.g., "Asalamu alaikum, kya hal hai?"

Cupid automatically matches your language!

## 🎮 Commands

While chatting, you can use these commands:

- **exit** - Say goodbye to Cupid
- **clear** - Clear conversation history, start fresh
- **stats** - See conversation statistics (messages, tokens, summaries)
- **help** - Show this help message

## ⚙️ Customization

Want to tweak Cupid's personality? Edit these in `cupid/config.py`:

```python
# Change the AI model (default: gpt-4o-mini)
MODEL=gpt-4o-mini

# Maximum response length in tokens (default: 150)
MAX_RESPONSE_TOKENS=150

# Memory settings
MAX_CONTEXT_TOKENS=2000        # Max context window
SUMMARIZATION_THRESHOLD=1500   # When to auto-summarize old messages
MEMORY_DB=memory.db           # Database file path

# Personality mood (currently only 'flirty')
DEFAULT_MOOD=flirty
```

Or modify the system prompt in `cupid/agent.py` to change Cupid's personality!

## 🧠 How Memory Works

Cupid uses smart memory management:

1. **Every message is stored** in a SQLite database
2. **Token counting** tracks how much context is used
3. **AI summarization** automatically compresses old conversations when the token limit is reached
4. **Summaries are included** in context to maintain conversation continuity
5. **Memory persists** between sessions - Cupid never forgets!

### Stats Breakdown

When you type `stats`, you'll see:

- **Total Messages**: All messages exchanged
- **Active Messages**: Recent messages in full detail
- **Summaries**: AI-generated conversation compressions
- **Tokens**: OpenAI tokens used (affects cost)

## 🎁 Features

✨ **AI-Powered Responses** - Uses GPT-4o-mini for natural, loving replies
✨ **Persistent Memory** - SQLite database remembers everything
✨ **Smart Summarization** - OpenAI creates concise summaries of old chats
✨ **Bilingual** - English + Roman Urdu support
✨ **Beautiful CLI** - Rich terminal interface with colors and emojis
✨ **Conversation Stats** - Track your chat history
✨ **Error Recovery** - Graceful handling with cute error messages

## 🐛 Troubleshooting

**"Command 'python' not found"**
- Try `python3 main.py` instead
- Make sure Python 3.11+ is installed and added to PATH

**"No module named 'openai'"**
```bash
pip install -r requirements.txt
# or
uv sync
```

**"OPENAI_API_KEY not set"**
- Make sure you created the `.env` file
- Check that the API key is correct and has credits

**"Connection error" / "Rate limit"**
- Check your internet connection
- You might have hit API rate limits - wait a moment
- Verify your OpenAI account has sufficient credits

**Database errors**
- Delete `memory.db` and restart (this clears conversation history)
- Make sure the app has permission to write files

## 📦 Project Structure

```
cupid/
├── agent.py       # AI agent with memory and personality
├── config.py      # Configuration management
├── memory.py      # SQLite database + summarization
├── main.py        # CLI interface with Rich
└── __init__.py

memory.db          # SQLite database (auto-created)
.env               # Your API key (create this)
requirements.txt   # Python dependencies
pyproject.toml    # Project metadata
```

## 🎵 Have Fun!

This is your space to chat, laugh, and enjoy genuine affection. Ahsan put his heart into this for you.

Cupid is always here to make your day brighter. 💕

---

*Made with ❤️ by Ahsan for Ashu*
