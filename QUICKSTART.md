# Quick Start Guide

Get your Security Status Bot up and running in 5 minutes!

## 🚀 Quick Setup (5 minutes)

### 1. Create Your Telegram Bot (2 minutes)
1. Message `@BotFather` on Telegram
2. Send: `/newbot`
3. Name your bot: `Community Security Bot`
4. Username: `your_community_security_bot`
5. **Copy the token!** (looks like: `1234567890:ABCdef...`)

### 2. Get Your User ID (1 minute)
1. Message `@userinfobot` on Telegram
2. Copy your User ID (a number like: `123456789`)

### 3. Configure the Bot (1 minute)
1. Copy `security-status-bot\.env.example` to `security-status-bot\.env`
2. Edit the `.env` file:
   ```env
   BOT_TOKEN=your_bot_token_here
   ADMIN_USER_IDS=your_user_id_here
   DATABASE_PATH=security_reports.db
   ```

### 4. Install & Run (1 minute)
```bash
# Install dependencies (if you have Python)
pip install python-telegram-bot==20.7 python-dotenv==1.0.0

# Run the bot
python bot.py
```

**Don't have Python?** Install it from: https://python.org

## 🎯 First Steps After Setup

### Test the Bot
1. Add your bot to a Telegram group
2. Send `/start` to see if it responds
3. Try `/status` (should show "no reports")

### Add Your First Focal Person
1. Send `/addfocal` in the group
2. Enter a Telegram User ID (get from `@userinfobot`)
3. Enter their full name (letters only)
4. They can now send `/report`

## 📋 Essential Commands

| Command | Who Can Use | What It Does |
|---------|-------------|--------------|
| `/start` | Everyone | Show help |
| `/status` | Everyone | Recent reports |
| `/location Area Name` | Everyone | Search by area |
| `/report` | Focal People | Submit report |
| `/addfocal` | Admins | Add reporter |
| `/listfocal` | Admins | List reporters |

## 🔥 Pro Tips

1. **Test privately first**: Message your bot directly before adding to group
2. **Get User IDs easily**: Have users send `/start` to your bot
3. **Location names**: Only use letters and spaces (no numbers/symbols)
4. **Multiple admins**: Separate User IDs with commas in `.env`
5. **Keep it running**: Use `screen` or `tmux` on Linux for persistent running

## ⚠️ Common Issues

- **"BOT_TOKEN not found"** → Check your `.env` file
- **Bot not responding** → Make sure it has message permissions in group
- **"Only authorized focal people"** → Add them with `/addfocal` first
- **Admin commands not working** → Check your User ID in `ADMIN_USER_IDS`

## 🆘 Need Help?

1. Check the full [README.md](README.md) for detailed instructions
2. Look at the logs when running `python bot.py`
3. Test commands in private chat with bot first
4. Verify your `.env` file has correct values

---

**Ready to go?** Your community security bot is now operational! 🛡️
