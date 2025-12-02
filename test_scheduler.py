"""
Test script to verify scheduler configuration and next run time.
"""
import asyncio
from datetime import datetime
from pytz import timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config import Config

# Define timezone (UTC+7 = Asia/Bangkok, Asia/Ho_Chi_Minh, etc.)
ICT = timezone('Asia/Bangkok')

async def test_scheduler():
    print("="*60)
    print("🧪 Testing Scheduler Configuration")
    print("="*60)

    # Current time in ICT
    now_ict = datetime.now(ICT)
    print(f"⏰ Current time (ICT): {now_ict.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # Current time in UTC
    now_utc = datetime.now(timezone('UTC'))
    print(f"⏰ Current time (UTC): {now_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    print(f"\n📋 Configuration:")
    print(f"   SUMMARY_HOUR: {Config.SUMMARY_HOUR}")
    print(f"   SUMMARY_MINUTE: {Config.SUMMARY_MINUTE}")
    print(f"   Timezone: ICT (Asia/Bangkok, UTC+7)")

    # Create scheduler with ICT timezone
    scheduler = AsyncIOScheduler(timezone=ICT)

    # Schedule the daily job with proper timezone support
    trigger = CronTrigger(
        hour=Config.SUMMARY_HOUR,
        minute=Config.SUMMARY_MINUTE,
        timezone=ICT
    )

    async def dummy_job():
        pass

    scheduler.add_job(
        dummy_job,
        trigger=trigger,
        id='test_job',
        name='Test Job'
    )

    scheduler.start()

    # Get next run time
    next_run = scheduler.get_job('test_job').next_run_time
    if next_run:
        next_run_ict = next_run.astimezone(ICT)
        next_run_utc = next_run.astimezone(timezone('UTC'))

        print(f"\n✅ Next scheduled run:")
        print(f"   ICT: {next_run_ict.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print(f"   UTC: {next_run_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")

        # Calculate time until next run
        time_until = next_run - datetime.now(timezone('UTC'))
        hours = int(time_until.total_seconds() // 3600)
        minutes = int((time_until.total_seconds() % 3600) // 60)

        print(f"\n⏳ Time until next run: {hours}h {minutes}m")

    scheduler.shutdown()
    print("\n" + "="*60)

if __name__ == '__main__':
    asyncio.run(test_scheduler())
