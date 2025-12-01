"""
Twitter crawler to fetch recent tweets from specified accounts.
Uses TwitterAPI.io to fetch tweets (excluding replies).
"""
import asyncio
import requests
from datetime import datetime, timedelta, timezone
from dateutil import parser as date_parser
from config import Config

class TwitterCrawler:
    """Crawls Twitter accounts for recent tweets"""
    
    def __init__(self):
        self.api_key = Config.TWITTER_API_KEY
        self.base_url = "https://api.twitterapi.io/twitter/user/last_tweets"
        self.headers = {
            "X-API-Key": self.api_key
        }
    
    async def crawl_account(self, username, count=50, hours=24):
        """
        Crawl tweets from a single Twitter account within a time window.
        
        Args:
            username (str): Twitter username (without @)
            count (int): Number of tweets to fetch from API (default: 50)
            hours (int): Only return tweets from last N hours (default: 24)
        
        Returns:
            list: List of tweet objects (excluding replies, within time window)
        """
        # Remove @ if present
        username = username.lstrip('@')
        
        print(f"  🐦 Crawling @{username} (last {hours} hours)...")
        
        # Calculate cutoff time (UTC)
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        params = {
            "userName": username,  # API requires camelCase 'userName'
            "count": count  # Fetch more to account for filtering
        }

        
        try:
            # Make synchronous request (we'll wrap in async)
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            # Debug: Print response details
            print(f"    📊 Response status: {response.status_code}")
            
            # Try to get error details before raising
            if response.status_code != 200:
                try:
                    error_data = response.json()
                    print(f"    📋 API Response: {error_data}")
                except:
                    print(f"    📋 Response text: {response.text[:200]}")
            
            response.raise_for_status()
            
            data = response.json()
            
            # Extract tweets from response - API returns {data: {tweets: [...]}}
            if 'data' not in data or 'tweets' not in data['data']:
                print(f"    ❌ Unexpected API response structure for @{username}")
                print(f"    📋 Response: {data}")
                return []
            
            tweets = data['data']['tweets']
            
            # Filter out replies and tweets outside time window
            filtered_tweets = []
            for tweet in tweets:
                # Skip if it's a reply (API uses 'isReply' not 'is_reply')
                if tweet.get('isReply', False):
                    continue
                
                # Parse tweet date and check if within time window
                try:
                    tweet_date_str = tweet.get('createdAt', '')
                    tweet_date = date_parser.parse(tweet_date_str)
                    
                    # Convert to UTC naive for comparison with datetime.utcnow()
                    # If it's aware, convert to UTC then strip info
                    if tweet_date.tzinfo:
                        tweet_date = tweet_date.astimezone(timezone.utc).replace(tzinfo=None)
                    else:
                        # Assume it was already UTC if naive (API usually returns UTC)
                        pass
                    
                    # Skip if tweet is older than cutoff
                    if tweet_date < cutoff_time:
                        continue
                except Exception as e:
                    print(f"    ⚠️  Could not parse date for tweet {tweet.get('id')}: {e}")
                    continue
                
                filtered_tweets.append({
                    'text': tweet.get('text', ''),
                    'created_at': tweet.get('createdAt', ''),  # API uses 'createdAt'
                    'id': tweet.get('id', ''),
                    'username': username,
                    'likes': tweet.get('likeCount', 0),  # API uses 'likeCount'
                    'retweets': tweet.get('retweetCount', 0),  # API uses 'retweetCount'
                    'url': tweet.get('url', f"https://twitter.com/{username}/status/{tweet.get('id', '')}")
                })
            
            print(f"    ✅ Found {len(filtered_tweets)} tweets from @{username} (last {hours} hours)")
            return filtered_tweets
            
        except requests.exceptions.RequestException as e:
            print(f"    ❌ Error crawling @{username}: {e}")
            return []
        except Exception as e:
            print(f"    ❌ Unexpected error for @{username}: {e}")
            return []
    
    async def crawl_accounts(self, hours=24):
        """
        Crawl tweets from all configured Twitter accounts within a time window.
        
        Args:
            hours (int): Only return tweets from last N hours (default: 24)
        
        Returns:
            dict: Tweets grouped by username
        """
        print(f"🔍 Starting to crawl Twitter accounts (last {hours} hours)...\n")
        
        all_tweets = {}
        
        for username in Config.TWITTER_ACCOUNTS:
            username = username.strip()
            tweets = await self.crawl_account(username, count=50, hours=hours)
            all_tweets[username] = tweets
            
            # Add delay to respect API rate limits (1 request per 5 seconds for free tier)
            print("    ⏳ Waiting 6 seconds to respect API rate limits...")
            await asyncio.sleep(6)
        
        total_tweets = sum(len(tweets) for tweets in all_tweets.values())
        print(f"\n✅ Twitter crawling complete! Total tweets: {total_tweets}\n")
        
        return all_tweets

async def crawl_twitter_accounts(hours=24):
    """
    Convenience function to crawl Twitter accounts.
    
    Args:
        hours (int): Only return tweets from last N hours (default: 24)
    
    Returns:
        dict: Tweets grouped by username
    """
    crawler = TwitterCrawler()
    tweets = await crawler.crawl_accounts(hours)
    return tweets

if __name__ == '__main__':
    # Test the Twitter crawler
    async def test():
        tweets = await crawl_twitter_accounts(hours=24)
        for username, tweet_list in tweets.items():
            print(f"\n{'='*80}")
            print(f"@{username}: {len(tweet_list)} tweets (last 24 hours)\n")
            for i, tweet in enumerate(tweet_list, 1):
                print(f"Tweet {i}:")
                print(f"  Text: {tweet['text']}")
                print(f"  Date: {tweet['created_at']}")
                print(f"  Likes: {tweet['likes']} | Retweets: {tweet['retweets']}")
                print(f"  URL: {tweet['url']}")
                print()
    
    asyncio.run(test())
