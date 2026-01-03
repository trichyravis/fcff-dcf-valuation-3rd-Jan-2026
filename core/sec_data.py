
import requests

HEADERS = {
    "User-Agent": "FCFF-DCF research your_email@example.com"
}

def get_cik_from_ticker(ticker):
    url = "https://www.sec.gov/files/company_tickers.json"
    data = requests.get(url, headers=HEADERS).json()

    for c in data.values():
        if c["ticker"].lower() == ticker.lower():
            return str(c["cik_str"]).zfill(10)

    raise ValueError("Ticker not found")

def get_company_xbrl(cik):
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()

def extract_series(xbrl, tags, col):
    import pandas as pd

    for tag in tags:
        try:
            df = pd.DataFrame(xbrl["facts"]["us-gaap"][tag]["units"].values())
            df = df[df["form"] == "10-K"].sort_values("end")
            df["Year"] = pd.to_datetime(df["end"]).dt.year
            return df[["Year", "val"]].rename(columns={"val": col})
        except:
            continue

    return pd.DataFrame(columns=["Year", col])
