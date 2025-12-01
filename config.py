"""
Configuration management for the Telegram News Bot.
Loads and validates environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for bot settings"""
    
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Telegram API Credentials
    TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
    TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
    
    # OpenRouter API
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    
    # Channel Configuration - Load from channels.txt file
    @staticmethod
    def load_channels():
        """Load channel list from tele_channels.txt file"""
        channels_file = os.path.join(os.path.dirname(__file__), 'news-source', 'tele_channels.txt')
        channels = []
        
        if os.path.exists(channels_file):
            with open(channels_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith('#'):
                        # Remove @ if present
                        channel = line.lstrip('@')
                        channels.append(channel)
        
        # Fallback to .env if tele_channels.txt is empty
        if not channels:
            channels = os.getenv('SOURCE_CHANNELS', 'infinityhedge,overheardonct').split(',')
        
        return channels
    
    SOURCE_CHANNELS = load_channels.__func__()
    TARGET_CHANNEL_ID = os.getenv('TARGET_CHANNEL_ID')
    
    # Twitter API Configuration
    TWITTER_API_KEY = 'new1_bec1ba033121454192b302fa702577b3'
    
    @staticmethod
    def load_twitter_accounts():
        """Load Twitter account list from twitter_channels.txt file"""
        twitter_file = os.path.join(os.path.dirname(__file__), 'news-source', 'twitter_channels.txt')
        accounts = []
        
        if os.path.exists(twitter_file):
            with open(twitter_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith('#'):
                        # Remove @ if present
                        account = line.lstrip('@')
                        accounts.append(account)
        
        return accounts
    
    TWITTER_ACCOUNTS = load_twitter_accounts.__func__()
    
    # Scheduling Configuration
    SUMMARY_HOUR = int(os.getenv('SUMMARY_HOUR', '9'))
    SUMMARY_MINUTE = int(os.getenv('SUMMARY_MINUTE', '0'))
    
    @classmethod
    def validate(cls):
        """Validate that all required configuration is present"""
        errors = []
        
        if not cls.TELEGRAM_BOT_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN is not set")
        
        if not cls.TELEGRAM_API_ID:
            errors.append("TELEGRAM_API_ID is not set")
        
        if not cls.TELEGRAM_API_HASH:
            errors.append("TELEGRAM_API_HASH is not set")
        
        if not cls.OPENROUTER_API_KEY:
            errors.append("OPENROUTER_API_KEY is not set")
        
        if not cls.TARGET_CHANNEL_ID:
            errors.append("TARGET_CHANNEL_ID is not set - please add your target channel ID to .env")
        
        if errors:
            raise ValueError(f"Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors))
        
        return True

# Validate configuration on import
try:
    Config.validate()
    print("✅ Configuration loaded successfully")
except ValueError as e:
    print(f"⚠️  Configuration warning: {e}")
