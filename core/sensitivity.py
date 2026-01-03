
import pandas as pd

def sensitivity_matrix(fcff, waccs, gs):
    table = pd.DataFrame(index=waccs, columns=gs)
    for w in waccs:
        for g in gs:
            table.loc[w, g] = (fcff * (1 + g)) / (w - g)
    return table
