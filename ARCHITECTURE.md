# Telegram & Twitter News Bot - Architecture Diagram

## System Flow

```mermaid
flowchart TD
    Start([User runs main.py]) --> Schedule{Run Mode?}
    
    Schedule -->|--now flag| RunNow[Run Immediately]
    Schedule -->|No flag| Scheduler[Start Scheduler]
    
    Scheduler --> Wait[Wait for scheduled time<br/>Default: 09:00 daily]
    Wait --> RunNow
    
    RunNow --> DailySummary[run_daily_summary<br/>scheduler.py]
    
    DailySummary --> CrawlTele[Crawl Telegram Channels<br/>crawler.py]
    DailySummary --> CrawlTwitter[Crawl Twitter Accounts<br/>twitter_crawler.py]
    
    CrawlTele --> TeleData[(Telegram Messages<br/>Last 24 hours)]
    CrawlTwitter --> TwitterData[(Twitter Tweets<br/>Last 24 hours)]
    
    TeleData --> Summarizer[Generate Summary<br/>summarizer.py]
    TwitterData --> Analyzer[Analyze Onchain<br/>onchain_analyzer.py]
    
    Summarizer --> AI1[OpenRouter API<br/>GPT-4o]
    Analyzer --> AI2[OpenRouter API<br/>GPT-4o]
    
    AI1 --> NewsBullets[News Bullets<br/>2-3 per channel]
    AI2 --> OnchainTop5[Top 5 Onchain<br/>Sorted by volume]
    
    NewsBullets --> Format[Format Combined Summary<br/>summarizer.py]
    OnchainTop5 --> Format
    
    Format --> FinalSummary[Final Summary<br/>News + Onchain Actions]
    
    FinalSummary --> Post[Post to Telegram<br/>bot.py]
    
    Post --> Success{Posted?}
    Success -->|Yes| Done([✅ Complete])
    Success -->|No| Error([❌ Error])
    
    style Start fill:#e1f5e1
    style Done fill:#e1f5e1
    style Error fill:#ffe1e1
    style AI1 fill:#e1e5ff
    style AI2 fill:#e1e5ff
    style FinalSummary fill:#fff4e1
```

## Component Details

```mermaid
flowchart LR
    subgraph Config["Configuration (config.py)"]
        TeleChannels[tele_channels.txt]
        TwitterAccounts[twitter_channels.txt]
        EnvVars[.env file]
    end
    
    subgraph Crawlers["Data Collection"]
        TeleCrawler[Telegram Crawler<br/>Uses Telethon API]
        TwitterCrawler[Twitter Crawler<br/>Uses TwitterAPI.io]
    end
    
    subgraph Processing["AI Processing"]
        NewsSummarizer[News Summarizer<br/>Extracts key points]
        OnchainAnalyzer[Onchain Analyzer<br/>Extracts movements<br/>+ volumes + links]
    end
    
    subgraph Output["Output"]
        Formatter[Format Summary<br/>News + Onchain sections]
        TeleBot[Telegram Bot<br/>Posts to channel]
    end
    
    Config --> Crawlers
    Crawlers --> Processing
    Processing --> Output
    
    style Config fill:#f0f0f0
    style Crawlers fill:#e1f5e1
    style Processing fill:#e1e5ff
    style Output fill:#fff4e1
```

## Data Flow Detail

```mermaid
sequenceDiagram
    participant User
    participant Main
    participant Scheduler
    participant TeleCrawler
    participant TwitterCrawler
    participant Summarizer
    participant Analyzer
    participant AI as OpenRouter API
    participant Bot
    participant Telegram
    
    User->>Main: python3 main.py --now
    Main->>Scheduler: run_daily_summary()
    
    par Crawl Data Sources
        Scheduler->>TeleCrawler: crawl_channels(hours=24)
        TeleCrawler->>TeleCrawler: Filter last 24h messages
        TeleCrawler-->>Scheduler: Telegram messages
    and
        Scheduler->>TwitterCrawler: crawl_twitter_accounts(hours=24)
        TwitterCrawler->>TwitterCrawler: Filter replies & 24h
        TwitterCrawler-->>Scheduler: Twitter tweets
    end
    
    Scheduler->>Summarizer: summarize_all(tele, twitter)
    
    Summarizer->>AI: Generate news bullets
    AI-->>Summarizer: News bullet points
    
    Summarizer->>Analyzer: analyze_tweets(twitter)
    Analyzer->>AI: Extract onchain movements
    AI-->>Analyzer: Top 5 movements (sorted by volume)
    
    Analyzer-->>Summarizer: Formatted onchain actions
    Summarizer->>Summarizer: Combine News + Onchain
    Summarizer-->>Scheduler: Final summary text
    
    Scheduler->>Bot: send_summary(text)
    Bot->>Telegram: Post message
    Telegram-->>Bot: Success
    Bot-->>Scheduler: Posted ✅
    Scheduler-->>User: Job complete
```

## File Structure

```
telegram-news-bot/
├── main.py                 # Entry point
├── scheduler.py            # Orchestrates daily workflow
├── crawler.py              # Telegram channel crawler
├── twitter_crawler.py      # Twitter account crawler
├── summarizer.py           # AI news summarization
├── onchain_analyzer.py     # AI onchain analysis
├── bot.py                  # Telegram bot posting
├── config.py               # Configuration loader
├── tele_channels.txt       # Telegram channels list
├── twitter_channels.txt    # Twitter accounts list
├── requirements.txt        # Dependencies
└── .env                    # API keys & settings
```

## Key Features

### 1. **Dual Source Crawling**
- **Telegram**: Crawls messages from channels using Telethon
- **Twitter**: Crawls tweets from accounts using TwitterAPI.io
- Both filter to last 24 hours only

### 2. **AI-Powered Analysis**
- **News Summarization**: GPT-4o extracts 2-3 key bullet points per channel
- **Onchain Analysis**: GPT-4o identifies top 5 movements by USD volume
- Includes blockchain explorer links (t.co shortened URLs)

### 3. **Smart Filtering**
- Telegram: All messages from channels
- Twitter: Excludes replies, only original tweets
- Time-based: Strict 24-hour window (UTC)

### 4. **Output Format**
```
Summary DD-MM-YYYY

News:
- Bullet point 1
- Bullet point 2
- Bullet point 3

Onchain Actions:
- Movement 1 ([link](url))
- Movement 2 ([link](url))
- Movement 3 ([link](url))
- Movement 4 ([link](url))
- Movement 5 ([link](url))
```

### 5. **Scheduling**
- Default: Runs daily at 09:00
- Manual: `python3 main.py --now`
- Configurable via `.env` file
