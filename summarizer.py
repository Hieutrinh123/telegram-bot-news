"""
Message summarization using OpenRouter API.
Extracts main bullet points from crawled messages.
"""
from openai import OpenAI
from config import Config

class MessageSummarizer:
    """Summarizes Telegram messages using AI"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=Config.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )
    
    def summarize_all(self, telegram_messages, twitter_tweets):
        """
        Generate a combined summary of Telegram news and Twitter onchain actions.
        
        Args:
            telegram_messages (dict): Telegram messages grouped by channel
            twitter_tweets (dict): Twitter tweets grouped by account
            
        Returns:
            str: Formatted summary with News and Onchain Actions
        """
        # 1. Generate Telegram News Summary
        news_bullets = self._generate_news_bullets(telegram_messages)
        
        # 2. Generate Onchain Analysis
        from onchain_analyzer import OnchainAnalyzer
        analyzer = OnchainAnalyzer()
        top_movements = analyzer.analyze_tweets(twitter_tweets)
        onchain_text = analyzer.format_onchain_summary(top_movements)
        
        # 3. Format Final Output
        return self._format_final_summary(news_bullets, onchain_text)
    
    def _generate_news_bullets(self, messages_by_channel):
        """Generate bullet points for Telegram news"""
        print("🤖 Generating AI summary for Telegram news...")
        
        all_bullets = []
        
        for channel, messages in messages_by_channel.items():
            if not messages:
                continue
            
            # Combine all messages from this channel
            combined_text = "\n\n---\n\n".join([msg['text'] for msg in messages])
            
            prompt = f"""
You are a news summarization bot. Analyze the following messages from the Telegram channel @{channel} and extract the main bullet points.

Requirements:
1. Create 2-3 CONCISE bullet points highlighting ONLY the most important information
2. Each bullet point should be ONE sentence maximum
3. Focus on key events, major announcements, or significant updates only
4. Remove all redundant, minor, or trivial information
5. Be extremely concise and to-the-point
6. Use professional language

Messages from @{channel}:
{combined_text[:8000]}  

Provide ONLY the bullet points, no introduction or conclusion.
"""
            
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                
                summary = response.choices[0].message.content.strip()
                
                # Clean up bullets
                lines = summary.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and (line.startswith('-') or line.startswith('•')):
                        clean_line = line.lstrip('-•').strip()
                        all_bullets.append(f"- {clean_line}")
                    elif line and not line.startswith('*'):
                        all_bullets.append(f"- {line}")
                
                print(f"  ✅ Summarized {len(messages)} messages from @{channel}")
                
            except Exception as e:
                print(f"  ❌ Error summarizing @{channel}: {e}")
                
        if not all_bullets:
            return ["- No significant news found in the last 24 hours."]
            
        return all_bullets

    def _format_final_summary(self, news_bullets, onchain_text):
        """Format the final combined summary"""
        from datetime import datetime
        
        date_str = datetime.now().strftime('%d-%m-%Y')
        
        summary = f"🗓 Summary {date_str}\n\n"
        
        summary += "🔥 Daily News\n\n"
        summary += "\n\n".join(news_bullets)
        
        summary += "\n\n🤓 Onchain actions\n\n"
        summary += onchain_text
        
        return summary

    def summarize_messages(self, messages_by_channel):
        """Legacy method for backward compatibility"""
        # This is kept if needed, but main workflow uses summarize_all
        news_bullets = self._generate_news_bullets(messages_by_channel)
        
        from datetime import datetime
        header = f"*Summary {datetime.now().strftime('%d-%m-%Y')}*\n\n"
        return header + "\n".join(news_bullets)

def summarize_all(telegram_messages, twitter_tweets):
    """Convenience function for combined summary"""
    summarizer = MessageSummarizer()
    return summarizer.summarize_all(telegram_messages, twitter_tweets)

def summarize_messages(messages_by_channel):
    """Convenience function for legacy summary"""
    summarizer = MessageSummarizer()
    return summarizer.summarize_messages(messages_by_channel)


if __name__ == '__main__':
    # Test with sample data
    sample_messages = {
        'infinityhedge': [
            {'text': 'Bitcoin reaches new all-time high at $95,000', 'date': None, 'id': 1},
            {'text': 'Ethereum upgrade scheduled for next month', 'date': None, 'id': 2}
        ],
        'overheardonct': [
            {'text': 'Major DeFi protocol announces new features', 'date': None, 'id': 3}
        ]
    }
    
    summary = summarize_messages(sample_messages)
    print(summary)
