# Automated Stock Market Posting Bot

This project is an **AI-powered stock market posting agent** that:
- Fetches the latest Apple ($AAPL) stock price using [yfinance](https://github.com/ranaroussi/yfinance).  
- Generates **charts** showing recent price trends.  
- Uses an **AI helper** (Gemini LLM) to generate:
    - Human-like captions for posts.  
    - A financial summary with related news headlines.  
    - Auto-generated hashtags. 
- Posts automatically to a **Telegram channel** with images and summaries.  
- Runs on an **automated schedule**: every 6 hours on weekdays (Mon–Fri).  

## Features

- Real-time stock price fetch (AAPL only).  
- Chart generation with matplotlib.  
- AI-generated captions & financial summaries with news context.  
- Auto hashtags.  
- Scheduled auto-posting every 6 hours, Mon–Fri.  
- Database logging for posted content.  

## Project Structure

- `telegram_bot.py` — Main bot logic and posting loop
- `ai_helper.py` — AI caption and summary generation
- `db_helper.py` — SQLite logging
- `logger.py` — Rotating file logger
- `config.py` — Loads environment variables
- `charts/` — (optional) Chart images
- `data/stock_bot.db` — SQLite database
- `logs/stock_bot.log` — Log file

## Setup

1. **Clone the repository**  
   ```sh
   git clone https://github.com/seelneas/Automated-AI-Posting-Agent.git
   ```
2. **Create a virtual environment**
    ```sh
        python3 -m venv venv
        source venv/bin/activate # On Linux/macOS
        venv\Scripts\activate    # On Windows 
    ```
2. **Install dependencies**  
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure environment variables**  
   Edit `.env` with your credentials:
   ```
   TELEGRAM_BOT_TOKEN = "<your-telegram-bot-token>"
   CHANNEL_ID = "<your-channel-id>"
   GOOGLE_API_KEY = "<your-google-api-key>"
   ```

4. **Run the bot**  
   ```sh
   python telegram_bot.py
   ```


## Future Improvements

- Multi-stock support.
- Better error handling for API rate limits.
- Integration with more financial news sources.
- Web dashboard for monitoring posts.

## Contribution
Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to improve.