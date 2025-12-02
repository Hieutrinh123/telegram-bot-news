"""
Scheduler for running daily news summaries.
"""
import asyncio
from datetime import datetime
from pytz import timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from crawler import crawl_channels
from summarizer import summarize_messages
from bot import send_summary
from config import Config

# Define timezone (UTC+7 = Asia/Bangkok, Asia/Ho_Chi_Minh, etc.)
ICT = timezone('Asia/Bangkok')

async def run_daily_summary():
    """
    Main workflow: Crawl channels → Summarize → Post to channel
    """
    print("\n" + "="*60)
    now_ict = datetime.now(ICT)
    print(f"🚀 Starting daily summary job at {now_ict.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print("="*60 + "\n")
    
    try:
        # Step 1: Crawl Telegram channels
        telegram_messages = await crawl_channels(hours=24)
        
        # Step 2: Crawl Twitter accounts
        from twitter_crawler import crawl_twitter_accounts
        twitter_tweets = await crawl_twitter_accounts(hours=24)
        
        # Step 3: Generate combined summary
        from summarizer import summarize_all
        summary = summarize_all(telegram_messages, twitter_tweets)
        
        print("\n" + "-"*60)
        print("📝 Generated Summary:")
        print("-"*60)
        print(summary)
        print("-"*60 + "\n")
        
        # Step 3: Send to target channel
        success = await send_summary(summary)
        
        if success:
            print("\n✅ Daily summary job completed successfully!\n")
        else:
            print("\n⚠️  Summary generated but failed to post to channel\n")
            
    except Exception as e:
        print(f"\n❌ Error in daily summary job: {e}\n")
    
    print("="*60 + "\n")

async def run_scheduler_async():
    """
    Run the scheduler continuously with APScheduler (async version).
    """
    print("="*60)
    print("🤖 Telegram News Bot - Scheduler Started")
    print("="*60)
    print(f"📡 Monitoring Telegram: {', '.join(['@' + ch for ch in Config.SOURCE_CHANNELS])}")
    print(f"🐦 Monitoring Twitter: {', '.join(['@' + acc for acc in Config.TWITTER_ACCOUNTS])}")
    print(f"📤 Posting to: {Config.TARGET_CHANNEL_ID}")
    print(f"⏰ Schedule: Daily at {Config.SUMMARY_HOUR:02d}:{Config.SUMMARY_MINUTE:02d} ICT (UTC+7)")
    print("="*60 + "\n")

    # Create scheduler with ICT timezone
    scheduler = AsyncIOScheduler(timezone=ICT)

    # Schedule the daily job with proper timezone support
    trigger = CronTrigger(
        hour=Config.SUMMARY_HOUR,
        minute=Config.SUMMARY_MINUTE,
        timezone=ICT
    )

    scheduler.add_job(
        run_daily_summary,
        trigger=trigger,
        id='daily_summary',
        name='Daily News Summary',
        replace_existing=True
    )

    # Start the scheduler
    scheduler.start()

    # Get next run time in ICT
    next_run = scheduler.get_job('daily_summary').next_run_time
    if next_run:
        next_run_ict = next_run.astimezone(ICT)
        print(f"✅ Scheduler configured! Next run: {next_run_ict.strftime('%Y-%m-%d %H:%M:%S %Z')}\n")

    # Keep running
    try:
        # Run forever using asyncio sleep
        while True:
            await asyncio.sleep(3600)  # Sleep for 1 hour, then continue
    except (KeyboardInterrupt, SystemExit):
        print("\n\n⚠️  Scheduler stopped by user")
        scheduler.shutdown()
        print("="*60)

def run_scheduler():
    """
    Wrapper to run the async scheduler.
    """
    asyncio.run(run_scheduler_async())

if __name__ == '__main__':
    run_scheduler()
