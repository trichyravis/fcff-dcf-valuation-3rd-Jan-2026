
"""
SEC 10-K Downloader and Parser
Fetch and extract key financial data from SEC EDGAR 10-K filings
"""
import json
try:
    from sec_edgar_downloader import Downloader
    DOWNLOADER_AVAILABLE = True
except ImportError:
    DOWNLOADER_AVAILABLE = False
    print("⚠️  sec-edgar-downloader not installed. Run: pip install sec-edgar-downloader")

import os
import re
from pathlib import Path
from typing import Optional, Dict, Any

# Optional: Only import BeautifulSoup if needed for parsing
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    print("ℹ️  beautifulsoup4 not installed. Install for financial extraction: pip install beautifulsoup4 lxml")

class SEC10KDownloader:
    """Download and parse SEC 10-K filings"""
    
    def __init__(self, company_name="Mountain Path Finance", email="finance@mountainpath.edu"):
        self.company_name = company_name
        self.email = email
        
        if DOWNLOADER_AVAILABLE:
            self.downloader = Downloader(company_name, email)
        else:
            self.downloader = None
    
    def download_10k(self, ticker: str, limit: int = 1) -> bool:
        """Download 10-K filings for a company"""
        if not DOWNLOADER_AVAILABLE:
            print(f"❌ sec-edgar-downloader not available for {ticker}")
            return False
        
        try:
            print(f"📥 Downloading latest {limit} 10-K(s) for {ticker}...")
            self.downloader.get("10-K", ticker, limit=limit)
            print(f"✅ Downloaded 10-K for {ticker}")
            return True
        except Exception as e:
            print(f"❌ Error downloading {ticker}: {e}")
            return False
    
    def _find_latest_10k_html(self, ticker: str) -> Optional[Path]:
        """Find the main HTML file of the latest 10-K filing"""
        base_dir = Path("sec-edgar-filings") / ticker / "10-K"
        if not base_dir.exists():
            return None
        
        # Find all accession subfolders (e.g., 0001234567-23-000123)
        accession_folders = [f for f in base_dir.iterdir() if f.is_dir()]
        if not accession_folders:
            return None
        
        # Get the most recently downloaded (or alphabetically latest)
        latest_folder = sorted(accession_folders, reverse=True)[0]
        
        # Look for primary document (often the largest .html or named 'primary-document.html')
        html_files = list(latest_folder.glob("*.html"))
        if not html_files:
            return None
        
        # Heuristic: pick the largest file (usually the full 10-K)
        primary_doc = max(html_files, key=lambda f: f.stat().st_size)
        return primary_doc

    def extract_financials_from_10k(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Extract key financial metrics from downloaded 10-K (simplified)"""
        if not BS4_AVAILABLE:
            print("⚠️  BeautifulSoup not available. Skipping extraction.")
            return None

        html_path = self._find_latest_10k_html(ticker)
        if not html_path:
            print(f"⚠️  No 10-K HTML found for {ticker}")
            return None

        try:
            with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
                soup = BeautifulSoup(f, 'lxml')
                text = soup.get_text()
        except Exception as e:
            print(f"❌ Error reading HTML for {ticker}: {e}")
            return None

        # Simplified regex extraction (case-insensitive, handles commas, decimals, parentheses)
        def extract_number(pattern, text):
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                # Clean number: remove commas, handle (100) as -100
                num_str = match.group(1).replace(',', '')
                if num_str.startswith('(') and num_str.endswith(')'):
                    num_str = '-' + num_str[1:-1]
                try:
                    return float(num_str)
                except ValueError:
                    return None
            return None

        # Patterns: Look for lines like "Net income... 123,456" or "(789,012)"
        financials = {
            "Net Income": extract_number(r"(?:Consolidated\s+)?Net\s+(?:income|loss)[^\d\.\-\(\)]*[\(]?([\d,\.]+)[\)]?", text),
            "Total Assets": extract_number(r"(?:Total\s+assets)[^\d\.\-\(\)]*[\(]?([\d,\.]+)[\)]?", text),
            "Total Debt": extract_number(r"(?:Total\s+debt|Long-term\s+debt)[^\d\.\-\(\)]*[\(]?([\d,\.]+)[\)]?", text),
            "EBITDA": extract_number(r"(?:EBITDA|Earnings\s+before\s+interest)[^\d\.\-\(\)]*[\(]?([\d,\.]+)[\)]?", text),
        }

        print(f"📊 Extracted financials for {ticker}: {financials}")
        return financials

if __name__ == "__main__":
    downloader = SEC10KDownloader("Mountain Path Finance", "prof@mountainpath.edu")
    tickers = ["AAPL", "MSFT", "TSLA"]

    print("🔍 Starting SEC 10-K Downloads...\n")
    
    for ticker in tickers:
        downloader.download_10k(ticker, limit=1)
    
    print("\n" + "="*50)
    print("🔍 Attempting Financial Extraction...\n")
    
    results = {}
    for ticker in tickers:
        data = downloader.extract_financials_from_10k(ticker)
        results[ticker] = data or {"Error": "Extraction failed"}
    
    # Optional: Save to JSON or Excel (you prefer Excel!)
    output_file = "10k_financials.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Results saved to {output_file}")
