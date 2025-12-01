#!/bin/bash
# Helper script to start the Telegram News Bot in a screen session

BOT_DIR="/Users/jonestrinh/.gemini/antigravity/scratch/telegram-news-bot"
SESSION_NAME="telegram-bot"

# Check if screen session already exists
if screen -list | grep -q "$SESSION_NAME"; then
    echo "⚠️  Screen session '$SESSION_NAME' already exists!"
    echo ""
    echo "Options:"
    echo "  1. Reattach to existing session: screen -r $SESSION_NAME"
    echo "  2. Kill existing session first: screen -X -S $SESSION_NAME quit"
    exit 1
fi

# Navigate to bot directory
cd "$BOT_DIR" || exit 1

# Start screen session and run the bot
echo "🚀 Starting Telegram News Bot in screen session..."
echo "📍 Session name: $SESSION_NAME"
echo ""
echo "To detach: Press Ctrl+A, then D"
echo "To reattach later: screen -r $SESSION_NAME"
echo ""
echo "Starting in 3 seconds..."
sleep 3

# Start screen with the bot
screen -S "$SESSION_NAME" python3 main.py
