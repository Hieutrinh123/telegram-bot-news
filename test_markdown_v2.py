"""
Test script to verify Markdown V2 escaping and message sending.
"""
import asyncio
from bot import NewsBot

async def test_markdown_v2():
    """Test that messages with special characters are properly escaped"""
    
    bot = NewsBot()
    
    # Test 1: Simple message with special characters
    print("Test 1: Simple message with special characters")
    test_msg_1 = "🗓 Summary 03\\-12\\-2025\n\n🔥 Daily News\n\n\\- Bitcoin reaches \\$95,000 \\(new ATH\\)\\!\n\n🤓 Onchain actions\n\n\\- Whale bought \\$5M \\$ETH \\([link](https://t.co/abc123)\\)"
    
    result = await bot.send_summary(test_msg_1)
    if result:
        print("✅ Test 1 passed\n")
    else:
        print("❌ Test 1 failed\n")
    
    # Test 2: Message with links and special characters
    print("Test 2: Message with links")
    test_msg_2 = "\\- Whale 0x123 bought \\$5M \\$ETH \\([link](https://t.co/test)\\)\n\n\\- Another movement \\$2M \\$BTC"
    
    result = await bot.send_summary(test_msg_2)
    if result:
        print("✅ Test 2 passed\n")
    else:
        print("❌ Test 2 failed\n")
    
    # Test 3: Edge cases with multiple special characters
    print("Test 3: Edge cases")
    test_msg_3 = "\\- Test with \\(parentheses\\), \\[brackets\\], \\{braces\\}, and \\#hashtags\\!\n\n\\- Also test \\. \\- \\+ \\= \\| symbols"
    
    result = await bot.send_summary(test_msg_3)
    if result:
        print("✅ Test 3 passed\n")
    else:
        print("❌ Test 3 failed\n")

if __name__ == '__main__':
    print("Testing Markdown V2 escaping...\n")
    asyncio.run(test_markdown_v2())
