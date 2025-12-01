# 🚀 Quick Start with Docker

Get the Telegram News Bot running in 3 minutes!

## Step 1: Prerequisites

Make sure you have:
- Docker and Docker Compose installed
- Telegram Bot Token (from @BotFather)
- Telegram API credentials (from my.telegram.org/apps)
- OpenRouter API key

## Step 2: Configure

```bash
# Clone the repo (if not already)
git clone <your-repo-url>
cd telegram-bot-news

# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env
```

Fill in these required values:
```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abc123def456...
OPENROUTER_API_KEY=sk-or-v1-...
TARGET_CHANNEL_ID=-1001234567890
```

## Step 3: Run

```bash
# Build and start
docker-compose up -d

# Check if it's running
docker ps

# View logs
docker-compose logs -f telegram-bot
```

## Step 4: First-Time Setup (Important!)

On first run, Telethon needs authentication:

```bash
# Run interactively
docker-compose run --rm telegram-bot uv run python crawler.py
```

You'll be prompted for:
1. Your phone number (with country code, e.g., +1234567890)
2. Verification code sent to your Telegram app

After this one-time setup, the session is saved and you won't need to authenticate again.

## Step 5: Test Health

```bash
# Run health check
docker-compose exec telegram-bot uv run python health_check.py
```

You should see:
```
✅ Bot API OK - Connected as @your_bot_name
✅ User API OK - Authorized as Your Name
✅ ALL CHECKS PASSED - Bot is healthy!
```

## Common Commands

```bash
# View logs
docker-compose logs -f

# Restart bot
docker-compose restart

# Stop bot
docker-compose down

# Run summary immediately (test)
docker-compose exec telegram-bot uv run python main.py --now

# Update channels and restart
nano news-source/tele_channels.txt
docker-compose restart
```

## Troubleshooting

### "Configuration Error"
- Check `.env` file has all required values
- No spaces around `=` signs
- No quotes needed

### "Not authorized"
- Run the interactive setup (Step 4)
- Make sure you enter the correct phone number

### "Can't read channel history"
- Telegram bots can't read channels, that's why we use Telethon with your user account
- Make sure your account has access to the source channels

### Container keeps restarting
```bash
# Check logs for errors
docker-compose logs telegram-bot

# Run health check
docker-compose exec telegram-bot uv run python health_check.py
```

## Next Steps

- Edit `news-source/tele_channels.txt` to add Telegram channels
- Edit `news-source/twitter_channels.txt` to add Twitter accounts
- Adjust schedule in `.env` (SUMMARY_HOUR and SUMMARY_MINUTE)
- See [DOCKER.md](DOCKER.md) for advanced Docker usage
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment options

## Production Deployment

Deploy to a VPS:

```bash
# On your local machine
scp -r ./* user@your-server:/opt/telegram-bot/

# SSH into server
ssh user@your-server
cd /opt/telegram-bot

# Configure and run
cp .env.example .env
nano .env
docker-compose up -d
```

The bot will auto-restart on server reboot thanks to `restart: unless-stopped` policy.
