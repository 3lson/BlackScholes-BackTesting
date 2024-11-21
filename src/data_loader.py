import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import random

def fetch_stock_data(ticker, start_date, end_date):
    # Fetch historical stock data from Yahoo Finance.
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data = stock_data[['Close']].reset_index()
    stock_data.columns = ['date', 'stock_price']
    return stock_data

def save_data(data, filepath):
    data.to_csv(filepath, index=False)

def load_data(filepath):
    return pd.read_csv(filepath)

def generate_options_data(stock_data, filepath):
    options_data = []
    for _, row in stock_data.iterrows():
        strike_price = round(row["stock_price"] * (1 + random.uniform(-0.05, 0.05)), 2)  
        time_to_maturity = random.uniform(0.1, 1.0)  
        market_price = random.uniform(0.05, 0.15) * row["stock_price"]  
        option_type = random.choice(["call", "put"])  # Randomly assign call or put

        options_data.append({
            "date": row["date"],
            "strike_price": strike_price,
            "time_to_maturity": round(time_to_maturity, 2),
            "market_price": round(market_price, 2),
            "option_type": option_type
        })

    # Save the generated data to a CSV file
    options_df = pd.DataFrame(options_data)
    options_df.to_csv(filepath, index=False)