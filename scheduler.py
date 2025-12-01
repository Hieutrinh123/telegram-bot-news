"""
Scheduler for running daily news summaries.
"""
import asyncio
import schedule
import time
from datetime import datetime
from crawler import crawl_channels
from summarizer import summarize_messages
from bot import send_summary
from config import Config

async def run_daily_summary():
    """
    Main workflow: Crawl channels → Summarize → Post to channel
    """
    print("\n" + "="*60)
    print(f"🚀 Starting daily summary job at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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

def schedule_daily_summary():
    """
    Schedule the daily summary to run at the configured time.
    """
    schedule_time = f"{Config.SUMMARY_HOUR:02d}:{Config.SUMMARY_MINUTE:02d}"
    
    print(f"⏰ Scheduling daily summary at {schedule_time}")
    
    # Schedule the job
    schedule.every().day.at(schedule_time).do(
        lambda: asyncio.run(run_daily_summary())
    )
    
    print(f"✅ Scheduler configured! Next run: {schedule.next_run()}\n")

def run_scheduler():
    """
    Run the scheduler continuously.
    """
    print("="*60)
    print("🤖 Telegram News Bot - Scheduler Started")
    print("="*60)
    print(f"📡 Monitoring Telegram: {', '.join(['@' + ch for ch in Config.SOURCE_CHANNELS])}")
    print(f"🐦 Monitoring Twitter: {', '.join(['@' + acc for acc in Config.TWITTER_ACCOUNTS])}")
    print(f"📤 Posting to: {Config.TARGET_CHANNEL_ID}")
    print(f"⏰ Schedule: Daily at {Config.SUMMARY_HOUR:02d}:{Config.SUMMARY_MINUTE:02d}")
    print("="*60 + "\n")
    
    # Schedule the daily job
    schedule_daily_summary()
    
    # Keep running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\n⚠️  Scheduler stopped by user")
        print("="*60)

if __name__ == '__main__':
    run_scheduler()
