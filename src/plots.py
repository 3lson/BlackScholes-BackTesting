import plotly.graph_objects as go
import plotly.express as px

def plot_prices(data):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data['date'], y=data['market_price'],
        mode='lines', name='Market Price', line=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=data['date'], y=data['bs_price'],
        mode='lines', name='Black-Scholes Price', line=dict(color='red', dash='dash')
    ))

    fig.update_layout(
        title='Stock and Option Prices',
        xaxis_title='Date',
        yaxis_title='Price',
        legend_title='Legend',
        template='plotly_dark',  # Change this for a different theme
        hovermode='closest'
    )

    fig.show()

def plot_implied_volatility(data):
    # Create a plot for Implied Volatility vs. Strike Price
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data['strike_price'], y=data['implied_vol'],
        mode='markers+lines', name='Implied Volatility', line=dict(color='green', dash='dot')
    ))

    fig.update_layout(
        title='Implied Volatility vs Strike Price',
        xaxis_title='Strike Price',
        yaxis_title='Implied Volatility',
        template='plotly_dark',
        hovermode='closest'
    )

    fig.show()

def plot_bs_vs_time_to_maturity(data):
    # Create a plot for Black-Scholes Price vs Time to Maturity
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data['time_to_maturity'], y=data['bs_price'],
        mode='markers+lines', name='Black-Scholes Price', line=dict(color='purple', dash='solid')
    ))

    fig.update_layout(
        title='Black-Scholes Price vs Time to Maturity',
        xaxis_title='Time to Maturity (Years)',
        yaxis_title='Black-Scholes Price',
        template='plotly_dark',
        hovermode='closest'
    )

    fig.show()

def plot_volatility_surface(data):
    # Create a 3D surface plot of implied volatility
    fig = go.Figure(data=[go.Surface(
        z=data.pivot('strike_price', 'time_to_maturity', 'implied_vol').values,
        x=data['strike_price'].unique(),
        y=data['time_to_maturity'].unique(),
        colorscale='Viridis'
    )])

    fig.update_layout(
        title='Volatility Surface',
        scene=dict(
            xaxis_title='Strike Price',
            yaxis_title='Time to Maturity',
            zaxis_title='Implied Volatility'
        ),
        template='plotly_dark'
    )

    fig.show()

def plot_backtest_results(backtest_data):
    """
    Plot the portfolio value over time from the backtest results.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=backtest_data['date'], y=backtest_data['portfolio_value'],
                             mode='lines', name='Portfolio Value'))

    fig.update_layout(title='Backtest Portfolio Value Over Time',
                      xaxis_title='Date',
                      yaxis_title='Portfolio Value',
                      template="plotly_dark")
    fig.show()
