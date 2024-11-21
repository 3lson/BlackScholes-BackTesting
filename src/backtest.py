import pandas as pd

def backtest(options_data, stock_data, initial_capital=10000, max_position_size=10):
    capital = initial_capital
    position = 0
    portfolio_value = []
    entry_price = 0
    entry_date = None
    last_stock_price = None

    # Ensure both date columns are datetime objects
    stock_data['date'] = pd.to_datetime(stock_data['date'])
    options_data['date'] = pd.to_datetime(options_data['date'])

    # Merge the stock and options data on the 'date' column
    merged_data = pd.merge(stock_data, options_data, on='date', how='left')

    print("Starting backtest...")

    for i, row in merged_data.iterrows():
        date = row['date']
        stock_price = row['stock_price']
        option_price = row['market_price']
        strike_price = row['strike_price']

        print(f"Date: {date}, Stock Price: {stock_price:.2f}")

        # Check if there's option data for this date
        if pd.notna(option_price) and pd.notna(strike_price):
            print(f"  Option Price: {option_price:.2f}, Strike Price: {strike_price:.2f}")

            # Buy when stock price is above strike price (and we are not in a position)
            if position == 0 and stock_price > strike_price:
                # Calculate how many contracts we can afford (but limit to max_position_size)
                max_contracts = min(capital // (option_price * 100), max_position_size)
                if max_contracts > 0:
                    position = max_contracts
                    cost = position * option_price * 100
                    if cost <= capital:  # Ensure we can afford the position
                        capital -= cost  # Deduct the cost from available capital
                        entry_price = option_price
                        entry_date = date
                        print(f"  Bought {position} contracts at price {entry_price:.2f} on {entry_date}")
                    else:
                        print(f"  Not enough capital to buy {max_contracts} contracts.")
                        position = 0
                else:
                    print("  Not enough capital to buy any options")

            # Sell when stock price is below strike price or after holding for 5 days
            elif position > 0:
                if (stock_price < strike_price or 
                    (entry_date is not None and (pd.to_datetime(date) - pd.to_datetime(entry_date)).days >= 5)):
                    current_value = position * option_price * 100
                    capital += current_value  # Add the current value to capital
                    print(f"  Sold {position} contracts at price {option_price:.2f} on {date}")
                    position = 0  # Reset position
                    entry_price = 0
                    entry_date = None
        else:
            print(f"  No option data available for {date}")

        # Calculate portfolio value after each day
        current_value = capital + (position * option_price * 100 if position > 0 else 0)
        portfolio_value.append(current_value)

        last_stock_price = stock_price  # Update last stock price for next day's decision

    print("Backtest complete.")

    return pd.DataFrame({
        'date': stock_data['date'],
        'portfolio_value': portfolio_value
    })

