
import numpy as np

def monte_carlo_dcf(fcff, wacc_mean, g_mean, n=5000):
    wacc = np.random.normal(wacc_mean, 0.01, n)
    g = np.random.normal(g_mean, 0.005, n)
    return (fcff * (1 + g)) / (wacc - g)
