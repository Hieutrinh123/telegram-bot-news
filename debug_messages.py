"""
Debug script to check specific message and see all recent messages from a channel.
"""
import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient
from config import Config

async def check_messages():
    """Check recent messages from overheardonct channel"""
    client = TelegramClient(
        'sessions/news_bot_user_session',
        Config.TELEGRAM_API_ID,
        Config.TELEGRAM_API_HASH
    )
    
    await client.start()
    
    channel = 'overheardonct'
    cutoff_time = datetime.now() - timedelta(hours=24)
    
    print(f"🔍 Checking messages from @{channel}")
    print(f"Current time: {datetime.now()}")
    print(f"Cutoff time (24h ago): {cutoff_time}")
    print(f"\nRecent messages:\n")
    
    count = 0
    async for message in client.iter_messages(channel, limit=10):
        count += 1
        msg_time = message.date.replace(tzinfo=None)
        within_24h = msg_time >= cutoff_time
        
        print(f"Message #{count} (ID: {message.id})")
        print(f"  Time: {msg_time}")
        print(f"  Within 24h: {'✅ YES' if within_24h else '❌ NO'}")
        print(f"  Text preview: {message.text[:100] if message.text else 'No text'}...")
        print()
    
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(check_messages())
