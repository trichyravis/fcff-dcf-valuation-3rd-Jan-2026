import pandas as pd

def get_share_count(xbrl):
    """
    Returns best available share count for valuation.
    Preference: Diluted → Basic → Outstanding
    """

    tag_priority = [
        "WeightedAverageNumberOfDilutedSharesOutstanding",
        "WeightedAverageNumberOfSharesOutstandingBasic",
        "CommonStockSharesOutstanding"
    ]

    for tag in tag_priority:
        try:
            data = xbrl["facts"]["us-gaap"][tag]["units"]["shares"]
            df = pd.DataFrame(data)
            df = df[df["form"] == "10-K"].sort_values("end")
            return int(df.iloc[-1]["val"])
        except:
            continue

    raise ValueError("Share count not available in 10-K")

