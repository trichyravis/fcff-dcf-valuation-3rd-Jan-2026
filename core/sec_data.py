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

def extract_series(xbrl, tag, col):
    try:
        df = pd.DataFrame(xbrl["facts"]["us-gaap"][tag]["units"]["USD"])
        df = df[df["form"] == "10-K"].sort_values("end").tail(5)
        df["Year"] = pd.to_datetime(df["end"]).dt.year
        return df[["Year", "val"]].rename(columns={"val": col})
    except:
        return pd.DataFrame(columns=["Year", col])
