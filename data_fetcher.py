import yfinance as yf
import sqlite3
from datetime import datetime, timedelta

# Set the end date to today and start date to one year ago
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

# List of stock symbols
symbols = ['AMZN']

# Fetch data and store in SQLite database
conn = sqlite3.connect('stock_data.db')

for symbol in symbols:
    # Fetch data
    stock = yf.Ticker(symbol)
    df = stock.history(start=start_date, end=end_date)
    
    # Store data in the database
    df.to_sql(symbol, conn, if_exists='replace')

conn.close()

print("Data fetching complete. Data stored in 'stock_data.db'.")