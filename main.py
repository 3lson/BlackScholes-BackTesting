from src.data_loader import fetch_stock_data, save_data, load_data, generate_options_data
from src.black_scholes import black_scholes
from src.implied_vol import implied_volatility
from src.plots import plot_prices, plot_backtest_results
from src.backtest import backtest  # Import the backtest function
import pandas as pd
import os

# Step 1: Fetch stock data
ticker = "AAPL"
start_date = "2023-01-01"
end_date = "2023-12-31"

print("Fetching stock data...")
stock_data = fetch_stock_data(ticker, start_date, end_date)
if not os.path.exists("data"):
    os.makedirs("data")
save_data(stock_data, "data/stocks.csv")
print("Stock data saved to data/stocks.csv")

# Step 2: Generate or load options data
options_filepath = "data/options_sample.csv"
if not os.path.exists(options_filepath):
    print("Generating options data dynamically...")
    generate_options_data(stock_data, options_filepath)
    print(f"Options data saved to {options_filepath}")
else:
    print(f"Options data found at {options_filepath}. Loading...")
options_data = load_data(options_filepath)

# Step 3: Add Black-Scholes prices to the options dataset
r = 0.05  # Risk-free rate
print("Calculating Black-Scholes prices...")
options_data['bs_price'] = options_data.apply(
    lambda row: black_scholes(
        S=stock_data.loc[stock_data['date'] == row['date'], 'stock_price'].values[0],
        K=row['strike_price'],
        T=row['time_to_maturity'],
        r=r,
        sigma=0.2,
        option_type=row['option_type']
    ),
    axis=1
)

# Step 4: Calculate implied volatilities
print("Calculating implied volatilities...")
options_data['implied_vol'] = options_data.apply(
    lambda row: implied_volatility(
        S=stock_data.loc[stock_data['date'] == row['date'], 'stock_price'].values[0],
        K=row['strike_price'],
        T=row['time_to_maturity'],
        r=r,
        market_price=row['market_price'],
        option_type=row['option_type']
    ),
    axis=1
)

# Step 5: Save updated options data
save_data(options_data, "data/updated_options_data.csv")
print("Updated options data with Black-Scholes prices and implied volatilities saved to data/updated_options_data.csv")

# Step 6: Backtest the strategy
print("Starting backtest...")
backtest_results = backtest(options_data, stock_data, initial_capital=10000)
save_data(backtest_results, "data/backtest_results.csv")
print("Backtest results saved to data/backtest_results.csv")

# Step 7: Plot the prices and backtest results
print("Generating plots...")
plot_prices(options_data)
plot_backtest_results(backtest_results)
print("Plotting complete!")
