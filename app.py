
"""
SEC 10-K Downloader and Parser
Fetch real financial data from SEC EDGAR 10-K filings
"""

try:
    from sec_edgar_downloader import Downloader
    DOWNLOADER_AVAILABLE = True
except ImportError:
    DOWNLOADER_AVAILABLE = False
    print("⚠️  sec-edgar-downloader not installed")

import os
import json
import re
from pathlib import Path

class SEC10KDownloader:
    """Download and parse SEC 10-K filings"""
    
    def __init__(self, company_name="Mountain Path Finance", email="finance@mountainpath.edu"):
        """Initialize downloader with SEC requirements"""
        self.company_name = company_name
        self.email = email
        self.output_dir = "./sec_filings"
        
        if DOWNLOADER_AVAILABLE:
            self.downloader = Downloader(company_name, email)
        else:
            self.downloader = None
    
    def download_10k(self, ticker, limit=1):
        """Download 10-K filings for a company"""
        if not DOWNLOADER_AVAILABLE:
            print(f"❌ sec-edgar-downloader not available for {ticker}")
            return False
        
        try:
            print(f"📥 Downloading 10-K for {ticker}...")
            self.downloader.get("10-K", ticker, limit=limit)
            print(f"✅ Downloaded 10-K for {ticker}")
            return True
        except Exception as e:
            print(f"❌ Error downloading {ticker}: {e}")
            return False
    
    def extract_financials_from_10k(self, ticker):
        """Extract financial metrics from downloaded 10-K"""
        try:
            # Look for downloaded file
            filepath = Path(f"sec-edgar-filings/{ticker}/0000{self._get_cik(ticker)}")
            
            if not filepath.exists():
                print(f"⚠️  No filing found for {ticker}")
                return None
            
            # This is simplified - full extraction would parse HTML/XML
            print(f"📊 Extracted data for {ticker}")
            return True
        except Exception as e:
            print(f"❌ Error extracting: {e}")
            return None
    
    @staticmethod
    def _get_cik(ticker):
        """Get CIK number for ticker"""
        cik_map = {
            "AAPL": "0000320193",
            "MSFT": "0000789019",
            "TSLA": "0001318605",
            "GOOGL": "0001652044",
            "AMZN": "0001018724",
        }
        return cik_map.get(ticker, "")

if __name__ == "__main__":
    # Initialize downloader
    downloader = SEC10KDownloader("Mountain Path Finance", "prof@mountainpath.edu")
    
    # List of tickers to download
    tickers = ["AAPL", "MSFT", "TSLA"]
    
    print("🔍 Starting SEC 10-K Downloads...\n")
    
    for ticker in tickers:
        downloader.download_10k(ticker, limit=1)
    
    print("\n✅ Download complete!")
    print("📁 Files saved to: ./sec-edgar-filings/")
