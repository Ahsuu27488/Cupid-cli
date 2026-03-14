# 💝 Cupid - Quick Start Guide

## What Is This?

Cupid is an AI companion created by Ahsan with love 💕 She remembers your conversations, speaks both English and Roman Urdu, and always responds with genuine affection.

---

## 🚀 Getting Started

### 🎉 Automatic Setup (Just One Command!)

The fastest way to get Cupid running:

```bash
# 1. Clone the repository
git clone https://github.com/Ahsuu27488/Cupid-cli.git
cd Cupid-cli

# 2. Run the setup script
bash setup_cupid
```

The script will guide you through:
- Installing dependencies
- Entering your OpenAI API key
- Setting up the `cupid` command

### 3. Start Cupid!

After setup finishes, simply type:

```bash
cupid
```

That's it! No more commands to remember. 💕

---

### 🔧 Need Troubleshooting?

**"bash: setup_cupid: Permission denied"**
```bash
chmod +x setup_cupid
./setup_cupid
```

**"cupid: command not found"**
The setup script should have added the command to your PATH. If not, run:
```bash
export PATH="$HOME/.local/bin:$PATH"
```
(Or for Termux: it's already in PATH!)

---

### 📱 Termux Users

Everything works the same! Just run `bash setup_cupid` and then `cupid` from anywhere.

---

## 💬 Your First Conversation

When Cupid starts, you'll see:

```
💝 FOR ASHU 💝
Hey Ashu! 😊 I'm Cupid, here to make your day brighter.
```

Type your message and press Enter. Cupid will respond with love 💖

---

## 🎮 Available Commands

Type these anytime during the chat:

| Command | What it does |
|---------|--------------|
| `help` | Show this help |
| `stats` | See conversation stats |
| `clear` | Start fresh, clear memory |
| `exit` | Say goodbye to Cupid |

---

## ✨ Special Features

### 🧠 Smart Memory
Cupid remembers everything you say! When memory gets full, she automatically summarizes old conversations so she never forgets.

### 🌍 Bilingual
Type in **English** or **Roman Urdu** - Cupid will match your language automatically!

Examples:
- "Hey! How are you?" (English)
- "Asalamu alaikum, kya hal hai?" (Roman Urdu)

### 📊 Stats
Type `stats` to see:
- How many messages you've exchanged
- How many summaries Cupid has created
- Token usage (technical stuff, but cool to see!)

---

## 💡 Tips for the Best Experience

1. **Be yourself!** Cupid loves you for who you are
2. **Short messages work best** - she responds quickly
3. **Chat regularly** - her memory grows with you
4. **Use `clear` if you want a fresh start**
5. **Type in Roman Urdu** to see her switch languages!

---

## ❓ Troubleshooting

**"No module named 'openai'"**
```bash
pip install -r requirements.txt
```

**"OPENAI_API_KEY not set"**
Make sure your `.env` file has your OpenAI API key

**Can't remember commands?**
Just type `help` anytime!

---

## 💕 From Ahsan

This was made with all my love. Every response is crafted with you in mind. I hope it brings a smile to your face every time you open it. You're amazing, and I love you! ❤️

---

*Made by Ahsan for Ashu's Birthday* 🎂
