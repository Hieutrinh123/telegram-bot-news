# Telegram & Twitter News Bot

A bot that crawls content from Telegram channels and Twitter accounts, with AI-powered summarization capabilities.

## Features Overview

This project contains **two independent crawlers**:

### 🔵 Telegram Crawler
- 📡 **Channel Crawling**: Monitors multiple Telegram channels for new messages
- 🤖 **AI Summarization**: Uses OpenRouter API (GPT-4) to extract key bullet points
- ⏰ **Automated Scheduling**: Posts summaries daily at 9 AM ICT (UTC+7) using APScheduler
- 📊 **Customizable**: Easy configuration via `tele_channels.txt`

### 🐦 Twitter Crawler (Standalone)
- 🔍 **Account Monitoring**: Fetches latest tweets from specified Twitter accounts
- 📝 **Original Tweets Only**: Filters out replies, only gets original tweets
- 🎯 **Configurable**: Manage accounts via `twitter_channels.txt`
- 🔌 **API-Based**: Uses TwitterAPI.io for reliable data fetching

---

## 🔵 Telegram Feature

### Prerequisites

1. **Telegram Bot Token**: Create a bot via [@BotFather](https://t.me/BotFather)
2. **Telegram API Credentials**: Get API ID and Hash from [my.telegram.org/apps](https://my.telegram.org/apps)
3. **OpenRouter API Key**: Sign up at [openrouter.ai](https://openrouter.ai)
4. **Target Channel**: The bot must be added as an admin to the channel where summaries will be posted

### Configuration

1. **Edit `news-source/tele_channels.txt`** to add Telegram channels to monitor:
   ```
   # One channel per line (with or without @)
   infinityhedge
   overheardonct
   ```

2. **Edit `news-source/twitter_channels.txt`** to add Twitter accounts to monitor:
   ```
   # One account per line (with or without @)
   mlmabc
   lookonchain
   ```

3. **Set up `.env` file** with your credentials:
   ```bash
   cp .env.example .env
   nano .env  # Fill in your credentials
   ```

   Required variables:
   - `TELEGRAM_BOT_TOKEN`: Your bot token from @BotFather
   - `TELEGRAM_API_ID`: Your API ID from my.telegram.org
   - `TELEGRAM_API_HASH`: Your API Hash from my.telegram.org
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `TARGET_CHANNEL_ID`: Channel ID where summaries will be posted (format: -100XXXXXXXXXX)
   - `SUMMARY_HOUR`: Hour to run daily (default: 9)
   - `SUMMARY_MINUTE`: Minute to run (default: 0)

4. **Authenticate Telegram session** (required for crawling channels):
   ```bash
   uv run python authenticate_session.py
   ```

   This will:
   - Prompt for your phone number (with country code, e.g., +1234567890)
   - Ask for verification code from Telegram
   - Create an authorized session file in `sessions/`

### Usage

**Run the scheduler** (posts daily summaries at configured time):
```bash
uv run python main.py
```

**Run summary immediately** (for testing):
```bash
uv run python main.py --now
```

**Test the crawler only**:
```bash
uv run python crawler.py
```

**Test the scheduler configuration**:
```bash
uv run python test_scheduler.py
```

### How It Works

1. **Scheduling**: APScheduler runs daily at 9 AM ICT (UTC+7) with proper timezone support
2. **Crawling**: Uses Telethon to read messages from the last 24 hours from both Telegram and Twitter
3. **Summarization**: Sends messages to OpenRouter API (GPT-4) for bullet points
4. **Posting**: Posts formatted summary to target channel via Telegram Bot API

---

## 🐦 Twitter Feature

### Prerequisites

- Twitter API access via TwitterAPI.io (API key configured in `config.py`)

### Configuration

**Edit `news-source/twitter_channels.txt`** to add Twitter accounts to monitor:
```
# One account per line (with or without @)
mlmabc
lookonchain
OnchainDataNerd
```

### Usage

**Run the Twitter crawler**:
```bash
uv run python twitter_crawler.py
```

This will:
- Fetch the latest tweets from each account
- Filter out replies (only original tweets)
- Display tweet content, likes, retweets, and URLs

### How It Works

1. **Account Loading**: Reads accounts from `news-source/twitter_channels.txt`
2. **API Fetching**: Calls TwitterAPI.io endpoint for each account
3. **Filtering**: Removes replies, keeps only original tweets
4. **Output**: Returns structured tweet data with metadata

---

## Installation

### Using Docker (Recommended for Production)

```bash
# 1. Configure environment
cp .env.example .env
nano .env  # Fill in your credentials

# 2. Authenticate session (run locally first)
uv run python authenticate_session.py

# 3. Build and run
docker-compose up -d

# 4. View logs
docker-compose logs -f
```

The Docker container will:
- Run the scheduler automatically on startup
- Post summaries daily at 9 AM ICT (UTC+7)
- Restart automatically if it crashes
- Use persistent volumes for sessions and configuration

### Using uv (Recommended for Development - Fast!)

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Navigate to project directory**:
   ```bash
   cd telegram-bot-news
   ```

3. **Install dependencies** (uv automatically creates a virtual environment):
   ```bash
   uv sync
   ```

4. **Authenticate session**:
   ```bash
   uv run python authenticate_session.py
   ```

5. **Run the bot**:
   ```bash
   uv run python main.py
   ```

### Using pip (Traditional)

1. **Navigate to project directory**:
   ```bash
   cd telegram-bot-news
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Authenticate and run**:
   ```bash
   python authenticate_session.py
   python main.py
   ```

## Project Structure

```
telegram-bot-news/
├── main.py                     # Entry point for the bot
├── config.py                   # Configuration management
├── scheduler.py                # APScheduler-based scheduling with timezone support
├── crawler.py                  # Telegram channel crawler
├── twitter_crawler.py          # Twitter account crawler
├── summarizer.py               # AI-powered summarization
├── bot.py                      # Telegram bot for posting
├── authenticate_session.py     # Interactive session authentication
├── test_scheduler.py           # Test scheduler configuration
├── health_check.py             # Health check for Docker
├── news-source/
│   ├── tele_channels.txt       # Telegram channels list
│   └── twitter_channels.txt    # Twitter accounts list
├── sessions/                   # Session files directory
│   ├── news_bot_user_session.session
│   └── README.md
├── pyproject.toml              # uv project configuration
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose setup
├── .env                        # Environment variables (not in git)
└── .env.example                # Environment template
```

## Testing Components

**Test scheduler configuration**:
```bash
uv run python test_scheduler.py
```

**Test Telegram crawler**:
```bash
uv run python crawler.py
```

**Test Twitter crawler**:
```bash
uv run python twitter_crawler.py
```

**Test summarizer**:
```bash
uv run python summarizer.py
```

**Test bot**:
```bash
uv run python bot.py
```

## Troubleshooting

### Scheduling Issues

**"Scheduler not running at correct time"**
- The bot now uses APScheduler with proper timezone support
- Default schedule: 9 AM ICT (UTC+7) = 2 AM UTC
- Run `test_scheduler.py` to verify next run time
- Check Docker container logs: `docker-compose logs -f`

### Session Issues

**"Session not authorized"**
- Run `python authenticate_session.py` to create an authorized session
- Session file must be in `sessions/` directory
- Session file: `sessions/news_bot_user_session.session`

**"Cannot find session file"**
- Ensure session file is in `sessions/` directory
- Check file exists: `ls -la sessions/`
- Re-authenticate if needed: `python authenticate_session.py`

### Telegram Issues

**"Configuration errors" on startup**
- Make sure all required variables are set in `.env`
- Verify your API credentials are correct

**"Error crawling channel"**
- Ensure the channels are public or you have access
- Check that your Telegram API credentials are valid
- Verify session is authorized

**"Error sending summary"**
- Verify the bot is added as an admin to the target channel
- Check that `TARGET_CHANNEL_ID` is correct (format: -100XXXXXXXXXX)

### Twitter Issues

**"API returned error"**
- Check that the Twitter username is correct
- Verify the account exists and is public

**No tweets returned**
- Account may have only posted replies recently
- Try with a different account that has original tweets

## Recent Updates

### v2.0 - December 2025
- ✅ **Fixed scheduler timezone issues**: Replaced `schedule` library with APScheduler
- ✅ **Proper timezone support**: Now correctly schedules at 9 AM ICT (UTC+7)
- ✅ **Session management**: Added authentication script and moved sessions to `sessions/` directory
- ✅ **Session validation**: Added authorization checks before crawling
- ✅ **Testing utilities**: Added `test_scheduler.py` for verifying configuration
- ✅ **Docker improvements**: Updated Dockerfile to use `uv` for faster builds

## Notes

- **Telegram bot** needs to remain running to post summaries on schedule
- **Session files** (`.session`) are created by Telethon and should not be shared
- **Timezone**: Scheduler uses ICT (UTC+7) timezone by default
- **Docker**: Recommended for production deployment with automatic restarts
- Consider using Docker or systemd for production deployments

## License

This project is for personal use.
