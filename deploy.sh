#!/bin/bash

# Telegram News Bot - Automated Deployment Script
# This script sets up the environment and systemd service on Ubuntu/Debian.

set -e  # Exit on error

# Configuration
APP_DIR=$(pwd)
USER_NAME=$(whoami)
SERVICE_NAME="telegram-bot"
PYTHON_BIN="$APP_DIR/venv/bin/python3"

echo "🚀 Starting deployment for Telegram News Bot..."
echo "📍 App Directory: $APP_DIR"
echo "👤 User: $USER_NAME"

# 1. Install System Dependencies
echo "📦 Installing system dependencies..."
if [ "$EUID" -ne 0 ]; then
    sudo apt update && sudo apt install -y python3 python3-pip python3-venv git
else
    apt update && apt install -y python3 python3-pip python3-venv git
fi

# 2. Set up Python Virtual Environment
echo "🐍 Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   ✅ Virtual environment created."
else
    echo "   ✅ Virtual environment already exists."
fi

# 3. Install Python Requirements
echo "📥 Installing Python dependencies..."
"$APP_DIR/venv/bin/pip" install -r requirements.txt

# 4. Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  WARNING: .env file not found!"
    echo "   Please create the .env file with your API keys before starting the bot."
    echo "   You can copy .env.example to .env and edit it."
fi

# 5. Create Systemd Service
echo "⚙️  Creating systemd service..."

SERVICE_CONTENT="[Unit]
Description=Telegram News Bot
After=network.target

[Service]
User=$USER_NAME
WorkingDirectory=$APP_DIR
ExecStart=$PYTHON_BIN $APP_DIR/main.py
Restart=always
RestartSec=10
EnvironmentFile=$APP_DIR/.env

[Install]
WantedBy=multi-user.target"

# Write service file (requires sudo)
if [ "$EUID" -ne 0 ]; then
    echo "$SERVICE_CONTENT" | sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null
    sudo systemctl daemon-reload
    sudo systemctl enable $SERVICE_NAME
    sudo systemctl restart $SERVICE_NAME
else
    echo "$SERVICE_CONTENT" > /etc/systemd/system/$SERVICE_NAME.service
    systemctl daemon-reload
    systemctl enable $SERVICE_NAME
    systemctl restart $SERVICE_NAME
fi

echo "✅ Deployment Complete!"
echo "--------------------------------------------------"
echo "🤖 Bot Service Status:"
if [ "$EUID" -ne 0 ]; then
    sudo systemctl status $SERVICE_NAME --no-pager
else
    systemctl status $SERVICE_NAME --no-pager
fi
echo "--------------------------------------------------"
echo "📜 To view logs: sudo journalctl -u $SERVICE_NAME -f"
echo "🛑 To stop bot:  sudo systemctl stop $SERVICE_NAME"
echo "▶️  To start bot: sudo systemctl start $SERVICE_NAME"
