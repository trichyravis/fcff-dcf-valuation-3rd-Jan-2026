import requests
import pandas as pd

HEADERS = {"User-Agent": "FCFF-DCF academic your_email@example.com"}

def get_cik_from_ticker(ticker):
    url = "https://www.sec.gov/files/company_tickers.json"
    data = requests.get(url, headers=HEADERS).json()
    for c in data.values():
        if c["ticker"].lower() == ticker.lower():
            return str(c["cik_str"]).zfill(10)
    raise ValueError("Ticker not found")

def get_company_xbrl(cik):
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    return requests.get(url, headers=HEADERS).json()

def extract_series(xbrl, tags, col):
    """
    tags: list of acceptable XBRL tags (ordered by preference)
    """
    for tag in tags:
        try:
            df = pd.DataFrame(xbrl["facts"]["us-gaap"][tag]["units"]["USD"])
            df = df[df["form"] == "10-K"].sort_values("end").tail(5)
            df["Year"] = pd.to_datetime(df["end"]).dt.year
            return df[["Year", "val"]].rename(columns={"val": col})
        except:
            continue

    return pd.DataFrame(columns=["Year", col])
def extract_working_capital_change(xbrl):
    try:
        # Current Assets (excluding cash)
        ca = extract_series(
            xbrl,
            ["AssetsCurrent"],
            "CA"
        )

        # Cash & equivalents
        cash = extract_series(
            xbrl,
            ["CashAndCashEquivalentsAtCarryingValue"],
            "Cash"
        )

        # Current Liabilities
        cl = extract_series(
            xbrl,
            ["LiabilitiesCurrent"],
            "CL"
        )

        if ca.empty or cl.empty:
            return pd.DataFrame()

        df = ca.merge(cl, on="Year", how="inner")

        if not cash.empty:
            df = df.merge(cash, on="Year", how="left")
            df["Cash"] = df["Cash"].fillna(0)
        else:
            df["Cash"] = 0

        # Net Working Capital (operating)
        df["NWC"] = (df["CA"] - df["Cash"]) - df["CL"]

        # ΔWC
        df["ΔWC"] = df["NWC"].diff()

        return df[["Year", "ΔWC"]].dropna()

    except:
        return pd.DataFrame()
