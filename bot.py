"""
Telegram bot for posting summaries to target channel.
"""
import asyncio
from telegram import Bot
from telegram.constants import ParseMode
from config import Config

class NewsBot:
    """Telegram bot for posting news summaries"""
    
    def __init__(self):
        self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
    
    async def send_summary(self, summary_text):
        """
        Send summary to the target channel.
        
        Args:
            summary_text (str): Formatted summary text to send
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Use channel ID directly (should be in format -100XXXXXXXXXX)
            channel_id = Config.TARGET_CHANNEL_ID
            
            # Convert to int if it's a numeric string
            if isinstance(channel_id, str) and channel_id.lstrip('-').isdigit():
                channel_id = int(channel_id)
            
            print(f"📤 Sending summary to channel {channel_id}...")
            
            # Send message with Markdown V2 formatting
            message = await self.bot.send_message(
                chat_id=channel_id,
                text=summary_text,
                parse_mode=ParseMode.MARKDOWN_V2
            )
            
            print(f"✅ Summary posted successfully! Message ID: {message.message_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending summary: {e}")
            return False
    
    async def send_test_message(self):
        """Send a test message to verify bot configuration"""
        test_text = "🤖 *Test Message*\n\nThis is a test message from the News Bot\\.\n\n_If you see this, the bot is configured correctly\\!_"
        return await self.send_summary(test_text)

async def send_summary(summary_text):
    """
    Convenience function to send a summary.
    
    Args:
        summary_text (str): Summary text to send
    
    Returns:
        bool: True if successful
    """
    bot = NewsBot()
    return await bot.send_summary(summary_text)

async def send_test_message():
    """Send a test message"""
    bot = NewsBot()
    return await bot.send_test_message()

if __name__ == '__main__':
    # Test the bot
    asyncio.run(send_test_message())
