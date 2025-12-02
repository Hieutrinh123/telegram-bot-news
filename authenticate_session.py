"""
Interactive script to authenticate the Telegram user session.
Run this ONCE to create an authorized session file.
"""
import asyncio
from telethon import TelegramClient
from config import Config

async def authenticate():
    """Authenticate and create a session file for crawling channels"""

    print("="*60)
    print("  🔐 TELEGRAM USER SESSION AUTHENTICATION")
    print("="*60)
    print("\nThis script will authenticate your Telegram account.")
    print("You'll need to:")
    print("  1. Enter your phone number (with country code, e.g., +1234567890)")
    print("  2. Enter the verification code sent to your Telegram app")
    print("  3. Enter 2FA password if enabled")
    print("\n" + "="*60 + "\n")

    # Create client with session file in sessions/ directory
    client = TelegramClient(
        'sessions/news_bot_user_session',
        Config.TELEGRAM_API_ID,
        Config.TELEGRAM_API_HASH
    )

    # Start interactive authentication
    await client.start()

    # Verify we're authorized
    if await client.is_user_authorized():
        me = await client.get_me()
        print("\n" + "="*60)
        print(f"✅ SUCCESS! Authenticated as: {me.first_name}")
        print(f"   Phone: {me.phone}")
        print(f"   Username: @{me.username}" if me.username else "")
        print("\nSession file saved to: sessions/news_bot_user_session.session")
        print("="*60 + "\n")
    else:
        print("\n❌ Authentication failed!\n")

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(authenticate())
