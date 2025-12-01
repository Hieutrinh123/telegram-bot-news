"""
Telegram News Bot - Main Entry Point

This bot crawls messages from specified Telegram channels,
generates AI-powered summaries, and posts them daily to a target channel.
"""
import asyncio
import sys
from scheduler import run_scheduler, run_daily_summary
from config import Config

def print_banner():
    """Print welcome banner"""
    print("\n" + "="*60)
    print("  🤖 TELEGRAM NEWS BOT")
    print("="*60)
    print(f"  📡 Source Channels: {', '.join(['@' + ch for ch in Config.SOURCE_CHANNELS])}")
    print(f"  📤 Target Channel: {Config.TARGET_CHANNEL_ID}")
    print(f"  ⏰ Schedule: Daily at {Config.SUMMARY_HOUR:02d}:{Config.SUMMARY_MINUTE:02d} ICT (UTC+7)")
    print("="*60 + "\n")

def print_help():
    """Print usage help"""
    print("\nUsage:")
    print("  python main.py              - Start the scheduler (runs daily)")
    print("  python main.py --now        - Run summary immediately (one-time)")
    print("  python main.py --help       - Show this help message")
    print()

def main():
    """Main entry point"""
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            print_banner()
            print_help()
            return
        elif sys.argv[1] == '--now':
            print_banner()
            print("🚀 Running summary immediately...\n")
            asyncio.run(run_daily_summary())
            return
        else:
            print(f"❌ Unknown argument: {sys.argv[1]}")
            print_help()
            return
    
    # Default: Run scheduler
    print_banner()
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"❌ Configuration Error:\n{e}\n")
        print("Please update your .env file with the required values.")
        return
    
    print("✅ Configuration validated successfully!\n")
    
    # Start the scheduler
    run_scheduler()

if __name__ == '__main__':
    main()
