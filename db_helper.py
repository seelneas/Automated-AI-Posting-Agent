import sqlite3
from datetime import datetime

DB_FILE = "data/stock_bot.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        stock_symbol TEXT,
        price REAL,
        price_change REAL,
        ai_caption TEXT,
        status TEXT,
        error_message TEXT
    )
    """)
    conn.commit()
    conn.close()

def log_post(stock_symbol, price, price_change, ai_caption, status, error_message=None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO posts (timestamp, stock_symbol, price, price_change, ai_caption, status, error_message)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), stock_symbol, price, price_change, ai_caption, status, error_message))
    conn.commit()
    conn.close()
