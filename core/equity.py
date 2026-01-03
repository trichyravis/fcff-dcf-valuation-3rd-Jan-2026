
import pandas as pd

def get_share_count(xbrl):
    tags = [
        "WeightedAverageNumberOfDilutedSharesOutstanding",
        "WeightedAverageNumberOfSharesOutstandingBasic",
        "CommonStockSharesOutstanding"
    ]

    for tag in tags:
        try:
            df = pd.DataFrame(xbrl["facts"]["us-gaap"][tag]["units"]["shares"])
            df = df[df["form"] == "10-K"].sort_values("end")
            return int(df.iloc[-1]["val"])
        except:
            continue

    raise ValueError("Share count not available")
