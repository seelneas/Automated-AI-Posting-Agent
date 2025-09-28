import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from telegram import Bot
import asyncio
import os
import re
import datetime
from ai_helper import generate_ai_caption, generate_ai_summary_post
from db_helper import log_post, init_db
from logger import logger
from config import TELEGRAM_BOT_TOKEN, CHANNEL_ID


init_db()
bot = Bot(token=TELEGRAM_BOT_TOKEN)
SYMBOL = "AAPL"  


def fetch_price(symbol=SYMBOL):
    """Fetch latest price and 7-day history for Apple."""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="7d", interval="1h")
        if hist.empty or len(hist["Close"]) < 2:
            logger.error(f"No price data available for {symbol}")
            return None, None
        latest_price = round(hist["Close"].iloc[-1], 2)
        prev_price = round(hist["Close"].iloc[-2], 2)
        pct_change = ((latest_price - prev_price) / prev_price) * 100
        return latest_price, hist, pct_change
    except Exception as e:
        logger.error(f"❌ Error fetching {symbol}: {e}")
        return None, None, None

def sanitize_ai_text(text):
    return re.sub(r"[*_~`]", "", text)

def fetch_news(symbol=SYMBOL, count=5):
    """Fetch latest news headlines from yfinance."""
    try:
        stock = yf.Ticker(symbol)
        news_items = stock.news[:count] if stock.news else []
        headlines = [item["title"] for item in news_items]
        return headlines
    except Exception as e:
        logger.warning(f"No news fetched for {symbol}: {e}")
        return []


def generate_chart(symbol, hist):
    """Generate chart from yfinance historical data."""
    try:
        last_price = hist["Close"].iloc[-1]
        prev_price = hist["Close"].iloc[-2]
        pct_change = ((last_price - prev_price) / prev_price) * 100
        arrow = "▲" if pct_change > 0 else "▼"
        color = "green" if pct_change > 0 else "red"

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(hist.index, hist["Close"], label="Price", color="blue", linewidth=2)
        ax.set_title(f"{symbol} Stock Price {arrow} {pct_change:.2f}%", fontsize=14, color=color)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        ax.legend()
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d\n%H:%M"))
        fig.autofmt_xdate(rotation=45)

        chart_path = f"{symbol}_chart.png"
        plt.savefig(chart_path, dpi=200, bbox_inches="tight")
        plt.close()
        logger.info(f"Chart saved to {chart_path}")
        return chart_path
    except Exception as e:
        logger.error(f"Error generating chart for {symbol}: {e}")
        return None


def generate_hashtags(symbol, pct_change):
    """Generate relevant hashtags based on price trend."""
    trend_tag = "#Bullish" if pct_change > 0 else "#Bearish" if pct_change < 0 else "#FlatMarket"
    hashtags = [f"#{symbol}", trend_tag, "#Stocks", "#Finance", "#Trading", "#Investing"]
    return " ".join(hashtags)


async def post_update():
    """Fetch Apple data, generate chart, AI caption, news, hashtags, and post."""
    price, hist, pct_change = fetch_price()
    if price is None or hist is None:
        logger.warning(f"Skipping {SYMBOL} due to missing data")
        return

    chart_path = generate_chart(SYMBOL, hist)
    if chart_path is None:
        logger.warning(f"Skipping {SYMBOL} due to chart generation failure")
        return

    headlines = fetch_news(SYMBOL, count=5)

    # AI-generated caption
    post_text = await generate_ai_caption(SYMBOL, price)
    post_text = sanitize_ai_text(post_text)
    hashtags = generate_hashtags(SYMBOL, pct_change)
    full_post = f"{post_text}\n\n{hashtags}"

    with open(chart_path, "rb") as img:
        await bot.send_photo(chat_id=CHANNEL_ID, photo=img, caption=full_post)

    log_post(SYMBOL, price, pct_change, full_post, "success")
    os.remove(chart_path)
    logger.info(f"✅ Post for {SYMBOL} sent and chart cleaned up")

    # AI-generated market summary with news
    summary_caption = await generate_ai_summary_post(SYMBOL, price, pct_change, headlines)
    summary_caption = sanitize_ai_text(summary_caption)
    summary_hashtags = generate_hashtags(SYMBOL, pct_change)
    full_summary = f"{summary_caption}\n\n{summary_hashtags}"
    await bot.send_message(chat_id=CHANNEL_ID, text=full_summary)
    log_post("SUMMARY", price, pct_change, full_summary, "success")
    logger.info("✅ Market summary post with headlines sent successfully")


async def run_auto():
    interval_hours = 6
    logger.info("🤖 Bot started. Auto-posting every 6 hours on weekdays (Mon–Fri)...")
    
    while True:
        today = datetime.datetime.today().weekday()  
        if today < 5:  
            logger.info("📈 Market open (Weekday). Running post_update...")
            await post_update()
        else:
            logger.info("📉 Weekend detected. Skipping post_update.")
        
        logger.info(f"⏳ Waiting {interval_hours} hours until next check...")
        await asyncio.sleep(interval_hours * 3600)


if __name__ == "__main__":
    asyncio.run(run_auto())
