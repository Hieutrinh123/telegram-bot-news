"""
Helper script to test bot access to the target channel.
This will help verify the channel ID and bot permissions.
"""
import asyncio
from telegram import Bot
from config import Config

async def test_bot_access():
    """Test if the bot can access the target channel"""
    bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
    
    print("🔍 Testing bot access to target channel...")
    print(f"Bot Token: {Config.TELEGRAM_BOT_TOKEN[:20]}...")
    print(f"Target Channel ID: {Config.TARGET_CHANNEL_ID}\n")
    
    try:
        # Try to get chat information
        chat = await bot.get_chat(chat_id=Config.TARGET_CHANNEL_ID)
        print(f"✅ Successfully accessed channel!")
        print(f"   Title: {chat.title}")
        print(f"   Type: {chat.type}")
        print(f"   ID: {chat.id}")
        
        # Try to send a test message
        print("\n📤 Attempting to send test message...")
        message = await bot.send_message(
            chat_id=Config.TARGET_CHANNEL_ID,
            text="🤖 Test message from News Bot"
        )
        print(f"✅ Test message sent successfully! Message ID: {message.message_id}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nPossible issues:")
        print("1. The bot is not added to the channel")
        print("2. The bot doesn't have permission to post messages")
        print("3. The channel ID is incorrect")
        print("\nTo fix:")
        print("1. Add the bot to your channel as an administrator")
        print("2. Give it permission to post messages")
        print("3. Verify the channel ID is correct")

if __name__ == '__main__':
    asyncio.run(test_bot_access())
