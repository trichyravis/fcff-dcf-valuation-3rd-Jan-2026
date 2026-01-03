
import pandas as pd
import numpy as np

def sensitivity_matrix(fcff_last, wacc_range, g_range):
    matrix = pd.DataFrame(index=wacc_range, columns=g_range)

    for w in wacc_range:
        for g in g_range:
            matrix.loc[w, g] = fcff_last*(1+g)/(w-g)

    return matrix
