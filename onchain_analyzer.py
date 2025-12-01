"""
Onchain movement analyzer using OpenRouter API.
Extracts and ranks significant onchain movements from tweets.
"""
from openai import OpenAI
from config import Config
import json
import re

class OnchainAnalyzer:
    """Analyzes tweets to identify and rank onchain movements"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=Config.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )
    
    def analyze_tweets(self, tweets_by_account):
        """
        Analyze tweets to extract top onchain movements.
        
        Args:
            tweets_by_account (dict): Tweets grouped by account
            
        Returns:
            list: Top 5 onchain movements ranked by volume
        """
        print("🔍 Analyzing onchain movements from tweets...")
        
        # Collect all tweets into a single list
        all_tweets = []
        for account, tweets in tweets_by_account.items():
            for tweet in tweets:
                # Include URL in the text so AI can associate it
                all_tweets.append(f"[{account}] {tweet['text']} (Link: {tweet['url']})")
        
        if not all_tweets:
            print("  ⚠️ No tweets to analyze")
            return []
            
        # Combine tweets for analysis
        combined_text = "\n\n".join(all_tweets)
        
        # Create prompt for AI
        prompt = f"""
You are an expert onchain analyst. Analyze the following tweets and extract onchain movements.

Tweets:
{combined_text[:12000]}

Requirements:
1. Process EVERY single tweet provided in the input.
2. For EACH tweet, extract the USD volume. If no volume is mentioned, use 0.
3. IMPORTANT: Extract the FIRST https://t.co/... link found INSIDE the tweet text itself. 
   - DO NOT use the tweet URL that appears after "(Link: ...)" at the end
   - ONLY extract the t.co link that is part of the actual tweet content
   - These t.co links are shortened URLs that point to blockchain explorers
   - If no t.co link is found in the tweet text, leave the "link" field empty
4. Return a JSON object with a "movements" key containing an array of objects with these fields:
   - "description": A concise 1-sentence description of the movement (e.g., "Whale 0x123 bought $5M $ETH"). Ensure all tickers have $ prefix.
   - "volume_usd": The numeric value in USD (e.g., 5000000). Use 0 if unknown.
   - "source": The Twitter account name (e.g., "lookonchain")
   - "link": The FIRST t.co link found IN the tweet text. Empty string if none found.

5. Sort the array by "volume_usd" in descending order.
6. Return the top 5 movements with the highest volume.
7. Format: {{"movements": [...]}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=1500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                result = json.loads(content)
                movements = result.get('movements', [])
                
                # If the AI returned a direct list instead of {movements: []}
                if isinstance(result, list):
                    movements = result
                elif isinstance(result, dict):
                    # Check if it has 'movements' key
                    if 'movements' in result and isinstance(result['movements'], list):
                        movements = result['movements']
                    # Check if the dict itself is a movement object (has volume_usd)
                    elif 'volume_usd' in result:
                        movements = [result]
                    else:
                        # Try to find a list in the dictionary
                        for key, value in result.items():
                            if isinstance(value, list):
                                movements = value
                                break
                
                # Ensure we have a list
                if not isinstance(movements, list):
                    movements = []
                
                # Sort by volume just in case
                movements.sort(key=lambda x: x.get('volume_usd', 0), reverse=True)
                
                # Take top 5 (updated from 3)
                top_movements = movements[:5]
                
                print(f"  ✅ Identified {len(movements)} movements, selecting top {len(top_movements)}")
                return top_movements
                
            except json.JSONDecodeError:
                print("  ❌ Failed to parse AI response as JSON")
                return []
                
        except Exception as e:
            print(f"  ❌ Error analyzing tweets: {e}")
            return []

    def format_onchain_summary(self, top_movements):
        """
        Format the top movements for the summary.
        
        Args:
            top_movements (list): List of movement objects
            
        Returns:
            str: Formatted bullet points with clickable links
        """
        if not top_movements:
            return "- No significant onchain movements detected."
            
        bullets = []
        for mov in top_movements:
            desc = mov.get('description', '').rstrip('.')
            link = mov.get('link', '')  # Changed from 'url' to 'link'
            
            # Don't add volume here - the AI already includes it in the description
            
            # Add link in format: description ([link](url))
            if link:
                bullets.append(f"- {desc} ([link]({link}))")
            else:
                bullets.append(f"- {desc}")
            
        return "\n\n".join(bullets)
