from scipy.optimize import minimize
from src.black_scholes import black_scholes

def implied_volatility(S, K, T, r, market_price, option_type="call"):
    #Calculate implied volatility by minimizing the error between the market price and the Black-Scholes price.
    def objective_function(sigma):
        return (black_scholes(S, K, T, r, sigma, option_type) - market_price)**2

    result = minimize(objective_function, 0.2, bounds=[(1e-4, 5)])
    return result.x[0] if result.success else None
