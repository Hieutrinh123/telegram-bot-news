# Telegram & Twitter News Bot

A bot that crawls content from Telegram channels and Twitter accounts, with AI-powered summarization capabilities.

## Features Overview

This project contains **two independent crawlers**:

### 🔵 Telegram Crawler
- 📡 **Channel Crawling**: Monitors multiple Telegram channels for new messages
- 🤖 **AI Summarization**: Uses OpenRouter API (GPT-4) to extract key bullet points
- ⏰ **Automated Scheduling**: Posts summaries every 24 hours at a configured time
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

1. **Edit `tele_channels.txt`** to add Telegram channels to monitor:
   ```
   # One channel per line (with or without @)
   infinityhedge
   overheardonct
   ```

2. **Set up `.env` file** with your credentials:
   ```bash
   cp .env.example .env
   nano .env  # Fill in your credentials
   ```
   
   Required variables:
   - `TELEGRAM_BOT_TOKEN`: Your bot token from @BotFather
   - `TELEGRAM_API_ID`: Your API ID from my.telegram.org
   - `TELEGRAM_API_HASH`: Your API Hash from my.telegram.org
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `TARGET_CHANNEL_ID`: Channel ID where summaries will be posted

### Usage

**Run the scheduler** (posts daily summaries):
```bash
python main.py
```

**Run summary immediately** (for testing):
```bash
python main.py --now
```

**Test the crawler only**:
```bash
python crawler.py
```

### How It Works

1. **Crawling**: Uses Telethon to read messages from the last 24 hours
2. **Summarization**: Sends messages to OpenRouter API (GPT-4) for bullet points
3. **Posting**: Posts formatted summary to target channel via Telegram Bot API

---

## 🐦 Twitter Feature

### Prerequisites

- Twitter API access via TwitterAPI.io (API key included in code)

### Configuration

**Edit `twitter_channels.txt`** to add Twitter accounts to monitor:
```
# One account per line (with or without @)
Cbb0fe
```

### Usage

**Run the Twitter crawler**:
```bash
python twitter_crawler.py
```

This will:
- Fetch the latest 10 tweets from each account
- Filter out replies (only original tweets)
- Display tweet content, likes, retweets, and URLs

### How It Works

1. **Account Loading**: Reads accounts from `twitter_channels.txt`
2. **API Fetching**: Calls TwitterAPI.io endpoint for each account
3. **Filtering**: Removes replies, keeps only original tweets
4. **Output**: Returns structured tweet data with metadata

---

## Installation

1. **Navigate to project directory**:
   ```bash
   cd /Users/jonestrinh/.gemini/antigravity/scratch/telegram-news-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
telegram-news-bot/
├── main.py                  # Entry point for Telegram bot
├── config.py                # Configuration management
├── crawler.py               # Telegram channel crawler
├── twitter_crawler.py       # Twitter account crawler (standalone)
├── summarizer.py            # AI-powered summarization
├── bot.py                   # Telegram bot for posting
├── scheduler.py             # Daily scheduling logic
├── tele_channels.txt        # Telegram channels list
├── twitter_channels.txt     # Twitter accounts list
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in git)
└── .env.example             # Environment template
```

## Testing Components

**Test Telegram crawler**:
```bash
python crawler.py
```

**Test Twitter crawler**:
```bash
python twitter_crawler.py
```

**Test summarizer**:
```bash
python summarizer.py
```

**Test bot**:
```bash
python bot.py
```

## Troubleshooting

### Telegram Issues

**"Configuration errors" on startup**
- Make sure all required variables are set in `.env`
- Verify your API credentials are correct

**"Error crawling channel"**
- Ensure the channels are public or the bot has access
- Check that your Telegram API credentials are valid

**"Error sending summary"**
- Verify the bot is added as an admin to the target channel
- Check that `TARGET_CHANNEL_ID` is correct

**First-time Telethon authentication**
- On first run, Telethon may ask for phone number and verification code
- This creates a session file that will be reused for future runs

### Twitter Issues

**"API returned error"**
- Check that the Twitter username is correct
- Verify the account exists and is public

**No tweets returned**
- Account may have only posted replies recently
- Try with a different account that has original tweets

## Notes

- **Telegram bot** needs to remain running to post summaries on schedule
- **Twitter crawler** is standalone and not integrated with the main bot
- Consider using a process manager like `pm2` or `systemd` for production
- Session files (`.session`) are created by Telethon and should not be shared

## License

This project is for personal use.
