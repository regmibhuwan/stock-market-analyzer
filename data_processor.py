import sqlite3
import pandas as pd
import numpy as np

# Connect to the SQLite database
conn = sqlite3.connect('stock_data.db')

# List of stock symbols
symbols = ['AMZN']

for symbol in symbols:
    # Read data from the database
    df = pd.read_sql(f"SELECT * FROM '{symbol}'", conn)
    
    # Set the date as the index
    df.set_index('Date', inplace=True)
    
    # Calculate daily returns
    df['Returns'] = df['Close'].pct_change()
    
    # Calculate moving averages
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()
    
    # Calculate RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Store processed data back to the database
    df.to_sql(f'{symbol}_processed', conn, if_exists='replace')

conn.close()

print("Data processing complete. Processed data stored in 'stock_data.db'.")

# ... (rest of your code)
with open('static/data_processor_complete', 'w') as f:
    f.write('complete')