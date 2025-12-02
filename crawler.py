"""
Telegram channel crawler to fetch messages from the last 24 hours.
"""
import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient
from config import Config

class ChannelCrawler:
    """Crawls Telegram channels for recent messages"""
    
    def __init__(self):
        # Use user session for reading channels (bots can't read channel history)
        self.client = TelegramClient(
            'sessions/news_bot_user_session',  # Session file for user authentication
            Config.TELEGRAM_API_ID,
            Config.TELEGRAM_API_HASH
        )
    
    async def crawl_channels(self, hours=24):
        """
        Crawl messages from configured channels within the specified time window.

        Args:
            hours (int): Number of hours to look back (default: 24)

        Returns:
            dict: Messages grouped by channel
        """
        print(f"🔍 Starting to crawl channels for the last {hours} hours...")

        # Connect and check authorization
        await self.client.connect()

        if not await self.client.is_user_authorized():
            print("❌ Session not authorized!")
            print("Please run the authentication script first to authorize the session.")
            await self.client.disconnect()
            return {}

        print("✅ Session authorized")
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        all_messages = {}
        
        for channel in Config.SOURCE_CHANNELS:
            channel = channel.strip()
            print(f"  📡 Crawling @{channel}...")
            
            messages = []
            try:
                async for message in self.client.iter_messages(channel):
                    # Stop if message is older than cutoff time
                    if message.date.replace(tzinfo=None) < cutoff_time:
                        break
                    
                    if message.text:
                        messages.append({
                            'text': message.text,
                            'date': message.date,
                            'id': message.id,
                            'channel': channel
                        })
                
                all_messages[channel] = messages
                print(f"    ✅ Found {len(messages)} messages from @{channel}")
                
            except Exception as e:
                print(f"    ❌ Error crawling @{channel}: {e}")
                all_messages[channel] = []
        
        await self.client.disconnect()
        
        total_messages = sum(len(msgs) for msgs in all_messages.values())
        print(f"✅ Crawling complete! Total messages: {total_messages}\n")
        
        return all_messages
    
    async def close(self):
        """Close the Telegram client connection"""
        if self.client.is_connected():
            await self.client.disconnect()

async def crawl_channels(hours=24):
    """
    Convenience function to crawl channels.
    
    Args:
        hours (int): Number of hours to look back
    
    Returns:
        dict: Messages grouped by channel
    """
    crawler = ChannelCrawler()
    try:
        messages = await crawler.crawl_channels(hours)
        return messages
    finally:
        await crawler.close()

if __name__ == '__main__':
    # Test the crawler
    async def test():
        messages = await crawl_channels(24)
        for channel, msgs in messages.items():
            print(f"\n@{channel}: {len(msgs)} messages")
            if msgs:
                print(f"  Latest: {msgs[0]['text'][:100]}...")
    
    asyncio.run(test())
