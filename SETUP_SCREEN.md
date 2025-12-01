# Running the Bot Persistently with Screen

This guide will help you run the Telegram News Bot in the background using `screen`, so it continues running even after you close your terminal.

## Prerequisites

Install `screen` if not already installed:
```bash
brew install screen
```

## Step-by-Step Setup

### 1. Start a Screen Session

Open your terminal and navigate to the bot directory:
```bash
cd /Users/jonestrinh/.gemini/antigravity/scratch/telegram-news-bot
```

Create a new screen session named `telegram-bot`:
```bash
screen -S telegram-bot
```

### 2. Start the Bot

Inside the screen session, run the bot:
```bash
python3 main.py
```

You should see:
```
🤖 Telegram News Bot - Scheduler Started
⏰ Schedule: Daily at 09:00
```

The bot is now running and will execute at 9:00 AM daily.

### 3. Detach from Screen

To leave the bot running in the background:
- Press `Ctrl + A`, then press `D` (detach)

You'll see: `[detached from telegram-bot]`

The bot is now running in the background! You can safely close your terminal.

## Managing the Screen Session

### Check if the Bot is Running

List all screen sessions:
```bash
screen -ls
```

You should see:
```
There is a screen on:
    12345.telegram-bot    (Detached)
```

### Reattach to the Bot

To view the bot's output or interact with it:
```bash
screen -r telegram-bot
```

### Stop the Bot

1. Reattach to the screen session:
   ```bash
   screen -r telegram-bot
   ```

2. Stop the bot:
   - Press `Ctrl + C`

3. Exit the screen session:
   ```bash
   exit
   ```

## Verify Schedule Configuration

The bot is configured to run at **9:00 AM daily** in your `.env` file:
```
SUMMARY_HOUR=9
SUMMARY_MINUTE=0
```

To verify this is set correctly, check your `.env` file or the startup banner when you run the bot.

## Troubleshooting

### Bot Not Running at 9 AM?

1. **Check the time zone**: The bot uses your system's local time. Verify:
   ```bash
   date
   ```

2. **Reattach and check logs**:
   ```bash
   screen -r telegram-bot
   ```
   Look for any error messages.

3. **Verify the schedule**: When the bot starts, it shows:
   ```
   ⏰ Schedule: Daily at 09:00
   ✅ Scheduler configured! Next run: 2025-11-29 09:00:00
   ```

### Screen Session Lost?

If you can't find your screen session after a system restart:
- Screen sessions don't survive reboots
- You'll need to start a new session following steps 1-3 above

### Multiple Screen Sessions?

If you accidentally created multiple sessions:
```bash
# List all sessions
screen -ls

# Kill a specific session
screen -X -S telegram-bot quit
```

## Quick Reference

| Command | Description |
|---------|-------------|
| `screen -S telegram-bot` | Create new session |
| `Ctrl+A, D` | Detach from session |
| `screen -r telegram-bot` | Reattach to session |
| `screen -ls` | List all sessions |
| `screen -X -S telegram-bot quit` | Kill session |
| `exit` | Exit session (after Ctrl+C) |

## Running on System Startup (Optional)

If you want the bot to start automatically when your Mac boots, consider using a LaunchAgent instead. Let me know if you'd like help setting that up!
