from src.black_scholes import black_scholes

def test_black_scholes_call():
    price = black_scholes(100, 100, 1, 0.05, 0.2, "call")
    assert abs(price - 10.45) < 0.01

def test_black_scholes_put():
    price = black_scholes(100, 100, 1, 0.05, 0.2, "put")
    assert abs(price - 5.57) < 0.01
