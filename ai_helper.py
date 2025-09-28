import google.generativeai as genai
from config import GOOGLE_API_KEY
from logger import logger

genai.configure(api_key=GOOGLE_API_KEY)

async def generate_ai_caption(symbol, price):
    prompt = f"""
    You are a creative social media manager writing captions for a finance page that provides stock updates.  
    Write a short, authentic caption about the stock {symbol}, with its latest price at ${price}.  

    Requirements:  
    - Keep it under 30 words (like a real Telegram/Twitter caption).  
    - Always start with an attention hook (emoji + phrase).  
    - Mention {symbol} and its price clearly.  
    - Add a couple of emojis (finance, trend, or emotional tone).  
    - Sound casual, conversational, and energetic — not like a news report.  
    - Optionally end with a quick question or call-to-action (e.g., "Bullish or bearish?").  
    - Avoid being too formal or generic.  

    Examples (for inspiration, don’t copy literally):  
    - "🚀 {symbol} is on the move! Trading at ${price} right now — where’s it heading next? 📊🔥"  
    - "📉 Market shake-up: {symbol} slips to ${price}. Buying the dip or staying cautious? 🤔💵"  
    - "💎 {symbol} holding strong at ${price}! Bulls still in charge, or will bears take over? 🐂🐻"  
    """


    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        ai_text = response.text.strip()
        return ai_text
    except Exception as e:
        print(f"❌ Error generating AI caption: {e}")
        return f"{symbol} current price: ${price}"
    



async def generate_ai_summary_post(symbol, price, price_change=None, headlines=None):
    """
    Generates a human-like stock summary with related news headlines.
    """
    pct_change_text = f"{price_change:.2f}%" if price_change else "N/A"
    news_text = "\n".join(headlines) if headlines else "No major headlines."

    prompt = f"""
    You are a human financial content creator writing a Telegram-style post.
    Stock: {symbol}
    Current price: ${price} ({pct_change_text} today)
    Latest news headlines:
    {news_text}

    Write a short, engaging, and human-sounding summary (2-3 short paragraphs) about {symbol} for Telegram:
    - Mention the price clearly
    - Include the context from news headlines
    - Use casual and relatable language
    - Add relevant emojis (📊📈📉💡💵)
    - End with a question or call-to-action
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"❌ Error generating AI summary for {symbol}: {e}")
        return f"📊 {symbol} is trading at ${price}."
    




