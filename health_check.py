"""
Health check script to verify Telegram API connectivity.
Tests both Bot API and User API (Telethon) connections.
"""
import asyncio
import sys
from telegram import Bot
from telethon import TelegramClient
from config import Config

async def check_bot_api():
    """Check if Telegram Bot API is accessible"""
    try:
        print("🔍 Testing Telegram Bot API...")
        bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        bot_info = await bot.get_me()
        print(f"✅ Bot API OK - Connected as @{bot_info.username}")
        return True
    except Exception as e:
        print(f"❌ Bot API Failed: {e}")
        return False

async def check_user_api():
    """Check if Telegram User API (Telethon) is accessible"""
    try:
        print("🔍 Testing Telegram User API (Telethon)...")
        client = TelegramClient(
            'health_check_session',
            Config.TELEGRAM_API_ID,
            Config.TELEGRAM_API_HASH
        )

        await client.connect()

        if await client.is_user_authorized():
            me = await client.get_me()
            print(f"✅ User API OK - Authorized as {me.first_name}")
            await client.disconnect()
            return True
        else:
            print("⚠️  User API: Not authorized yet (needs first-time login)")
            await client.disconnect()
            return True  # Not a critical failure for health check

    except Exception as e:
        print(f"❌ User API Failed: {e}")
        return False

async def check_config():
    """Validate configuration"""
    try:
        print("🔍 Checking configuration...")
        Config.validate()
        print("✅ Configuration OK")
        return True
    except Exception as e:
        print(f"❌ Configuration Failed: {e}")
        return False

async def main():
    """Run all health checks"""
    print("\n" + "="*60)
    print("  🏥 TELEGRAM BOT HEALTH CHECK")
    print("="*60 + "\n")

    # Check configuration
    config_ok = await check_config()
    if not config_ok:
        print("\n❌ Health check FAILED: Configuration error")
        sys.exit(1)

    print()

    # Check Bot API
    bot_ok = await check_bot_api()
    print()

    # Check User API
    user_ok = await check_user_api()
    print()

    # Overall status
    print("="*60)
    if bot_ok and user_ok:
        print("✅ ALL CHECKS PASSED - Bot is healthy!")
        print("="*60 + "\n")
        sys.exit(0)
    else:
        print("❌ HEALTH CHECK FAILED")
        print("="*60 + "\n")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
