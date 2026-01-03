import numpy as np

def monte_carlo_dcf(fcff_last, wacc_mean, g_mean, sims=10000):
    wacc = np.random.normal(wacc_mean, 0.01, sims)
    g = np.random.normal(g_mean, 0.005, sims)

    values = (fcff_last*(1+g))/(wacc-g)
    return values

