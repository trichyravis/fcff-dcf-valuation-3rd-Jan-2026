
import streamlit as st
import os
import json
import re
from pathlib import Path

# Try imports
try:
    from sec_edgar_downloader import Downloader
    DOWNLOADER_AVAILABLE = True
except ImportError:
    DOWNLOADER_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

# Page config
st.set_page_config(page_title="SEC 10-K Financial Extractor", layout="wide")
st.title("SEC 10-K Financial Data Extractor")

# Sidebar input
st.sidebar.header("Settings")
tickers_input = st.sidebar.text_input("Enter tickers (comma-separated)", "AAPL,MSFT,TSLA")
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

download_limit = st.sidebar.slider("10-Ks per company", 1, 3, 1)

if not DOWNLOADER_AVAILABLE:
    st.error("⚠️ `sec-edgar-downloader` not installed. Install it in requirements.txt")
if not BS4_AVAILABLE:
    st.warning("⚠️ `beautifulsoup4` not installed. Extraction may fail.")

# Button to run
if st.button("📥 Download & Extract 10-K Financials"):
    if not DOWNLOADER_AVAILABLE:
        st.stop()

    dl = Downloader("Mountain Path Finance", "prof@mountainpath.edu")
    results = {}

    progress = st.progress(0)
    status = st.empty()

    for i, ticker in enumerate(tickers):
        status.info(f"📥 Downloading {ticker}...")
        try:
            dl.get("10-K", ticker, limit=download_limit)
        except Exception as e:
            st.warning(f"Failed to download {ticker}: {e}")
            results[ticker] = {"Error": str(e)}
            continue

        # Try to extract
        status.info(f"🔍 Extracting {ticker}...")
        financials = extract_financials(ticker)
        results[ticker] = financials or {"Error": "Extraction failed"}

        progress.progress((i + 1) / len(tickers))

    status.success("✅ Done!")
    st.subheader("Extracted Financials")
    st.json(results)

    # Offer download
    json_str = json.dumps(results, indent=2)
    st.download_button(
        label="💾 Download JSON",
        data=json_str,
        file_name="10k_financials.json",
        mime="application/json"
    )

# --- Helper function (must be defined at module level) ---
def extract_financials(ticker: str):
    if not BS4_AVAILABLE:
        return None

    base_dir = Path("sec-edgar-filings") / ticker / "10-K"
    if not base_dir.exists():
        return None

    accession_folders = [f for f in base_dir.iterdir() if f.is_dir()]
    if not accession_folders:
        return None

    latest_folder = sorted(accession_folders, reverse=True)[0]
    html_files = list(latest_folder.glob("*.html"))
    if not html_files:
        return None

    primary_doc = max(html_files, key=lambda f: f.stat().st_size)

    try:
        with open(primary_doc, 'r', encoding='utf-8', errors='ignore') as f:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(f, 'lxml')
            text = soup.get_text()
    except Exception as e:
        return {"Parse Error": str(e)}

    def extract_number(pattern, text):
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            num_str = match.group(1).replace(',', '').replace('$', '').strip()
            if num_str.startswith('(') and num_str.endswith(')'):
                num_str = '-' + num_str[1:-1]
            try:
                return float(num_str)
            except ValueError:
                return None
        return None

    return {
        "Net Income": extract_number(r"(?:Net\s+(?:income|loss)).*?[\(]?([\d,\.]+)\s*million", text),
        "Total Assets": extract_number(r"(?:Total\s+assets).*?[\(]?([\d,\.]+)\s*million", text),
        "Total Debt": extract_number(r"(?:Total\s+debt|Long-term\s+debt).*?[\(]?([\d,\.]+)\s*million", text),
    }
