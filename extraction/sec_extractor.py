"""
SEC EDGAR Data Extraction Module
Fetches 10-K filings from SEC EDGAR and extracts financial facts into normalized format
Prof. V. Ravichandran - The Mountain Path - World of Finance
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import sqlite3
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SECEDGARExtractor:
    """
    Fetches and processes SEC EDGAR Company Facts JSON
    This is the authoritative source for XBRL-tagged financial data
    """
    
    BASE_URL = "https://data.sec.gov/api/xbrl"
    COMPANY_FACTS_ENDPOINT = "/companyfacts/CIK{cik}.json"
    
    # User-Agent required by SEC
    HEADERS = {
        "User-Agent": "Financial Education Platform (contact: ravichandran@financialmodeling.edu)"
    }
    
    def __init__(self, db_connection: sqlite3.Connection):
        self.db = db_connection
        self.cursor = self.db.cursor()
    
    def fetch_company_facts(self, cik: str) -> Dict:
        """
        Fetch Company Facts JSON from SEC EDGAR
        
        Args:
            cik: Central Index Key (with leading zeros, 10 digits)
        
        Returns:
            Dictionary containing all financial facts for the company
        """
        # Format CIK with leading zeros
        cik_formatted = str(cik).zfill(10)
        url = f"{self.BASE_URL}{self.COMPANY_FACTS_ENDPOINT}".format(cik=cik_formatted)
        
        logger.info(f"Fetching company facts for CIK: {cik_formatted}")
        
        try:
            response = requests.get(url, headers=self.HEADERS, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch data from SEC: {e}")
            return None
    
    def extract_company_info(self, facts_json: Dict) -> Tuple[str, str, str]:
        """Extract company identifier information"""
        entity_info = facts_json.get("entityName", "Unknown")
        cik = facts_json.get("cik_str", "")
        
        return cik, entity_info, None  # sector/industry from SEC requires different endpoint
    
    def get_financial_facts_for_period(self, facts_json: Dict, 
                                       period_end: str, 
                                       filing_type: str = "10-K") -> Dict[str, float]:
        """
        Extract financial facts for a specific period
        
        The Company Facts JSON structure is:
        {
            "facts": {
                "us-gaap": {
                    "NetIncomeLoss": [
                        {
                            "accession": "0000789019-24-000045",
                            "end": "2023-12-31",
                            "val": 45000000,
                            "fy": 2023,
                            "filed": "2024-01-29",
                            "form": "10-K"
                        },
                        ...
                    ]
                }
            }
        }
        """
        financial_facts = {}
        
        facts_structure = facts_json.get("facts", {})
        us_gaap = facts_structure.get("us-gaap", {})
        
        # Iterate through all XBRL tags
        for xbrl_tag, values_list in us_gaap.items():
            if not isinstance(values_list, list):
                continue
            
            # Find the entry matching our period and filing type
            for entry in values_list:
                entry_date = entry.get("end", "")
                entry_form = entry.get("form", "")
                entry_fy = entry.get("fy", 0)
                
                # Match by period end date and form type
                if entry_date == period_end and entry_form == filing_type:
                    value = entry.get("val", 0)
                    accession = entry.get("accession", "")
                    filed_date = entry.get("filed", "")
                    
                    financial_facts[xbrl_tag] = {
                        "value": value,
                        "accession": accession,
                        "filed": filed_date,
                        "fy": entry_fy
                    }
                    break
        
        return financial_facts
    
    def insert_company(self, ticker: str, cik: str, company_name: str) -> int:
        """Insert or get company ID"""
        self.cursor.execute("""
            INSERT OR IGNORE INTO companies (ticker, cik, company_name)
            VALUES (?, ?, ?)
        """, (ticker, cik, company_name))
        
        self.cursor.execute("SELECT id FROM companies WHERE ticker = ?", (ticker,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def insert_financial_period(self, company_id: int, 
                               period_end: str,
                               fiscal_year: int,
                               filing_type: str,
                               accession: str) -> int:
        """Insert financial period and return period_id"""
        filing_date = datetime.now().strftime("%Y-%m-%d")
        
        self.cursor.execute("""
            INSERT OR IGNORE INTO financial_periods 
            (company_id, period_end_date, fiscal_year, filing_type, filing_date, accession_number)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (company_id, period_end, fiscal_year, filing_type, filing_date, accession))
        
        self.cursor.execute("""
            SELECT id FROM financial_periods 
            WHERE company_id = ? AND period_end_date = ? AND filing_type = ?
        """, (company_id, period_end, filing_type))
        
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def classify_line_item(self, xbrl_tag: str) -> Tuple[str, str]:
        """
        Classify XBRL tag into statement type and standardized line item
        
        Returns:
            (statement_type, standardized_line_item)
            statement_type: 'INCOME', 'BALANCE_SHEET', 'CASH_FLOW'
        """
        # Income statement tags
        income_tags = [
            "Revenues", "CostOfRevenue", "GrossProfit", "OperatingExpenses",
            "OperatingIncomeLoss", "InterestExpense", "OtherIncomeExpenseNet",
            "IncomeTaxExpenseBenefit", "NetIncomeLoss"
        ]
        
        # Balance sheet tags
        balance_tags = [
            "Assets", "AssetsCurrent", "AssetsNonCurrent", "Cash",
            "AccountsReceivable", "Inventory", "PropertyPlantAndEquipmentNet",
            "Goodwill", "IntangibleAssetsNetOtherThanGoodwill",
            "Liabilities", "LiabilitiesCurrent", "AccountsPayable",
            "LongTermBorrowings", "StockholdersEquity"
        ]
        
        # Cash flow tags
        cashflow_tags = [
            "NetCashProvidedByUsedInOperatingActivities",
            "PaymentsForAcquisitionsOfProductiveAssets",
            "DepreciationDepletionAndAmortization", "DepreciationAndAmortization"
        ]
        
        if xbrl_tag in income_tags:
            return "INCOME", xbrl_tag
        elif xbrl_tag in balance_tags:
            return "BALANCE_SHEET", xbrl_tag
        elif xbrl_tag in cashflow_tags:
            return "CASH_FLOW", xbrl_tag
        else:
            return "OTHER", xbrl_tag
    
    def insert_financial_facts(self, period_id: int, facts: Dict):
        """Insert extracted financial facts into appropriate tables"""
        
        for xbrl_tag, fact_data in facts.items():
            value = fact_data.get("value", 0)
            
            statement_type, line_item = self.classify_line_item(xbrl_tag)
            
            try:
                if statement_type == "INCOME":
                    self.cursor.execute("""
                        INSERT OR REPLACE INTO income_statement
                        (period_id, line_item, xbrl_tag, value, unit)
                        VALUES (?, ?, ?, ?, 'USD')
                    """, (period_id, line_item, xbrl_tag, value))
                
                elif statement_type == "BALANCE_SHEET":
                    self.cursor.execute("""
                        INSERT OR REPLACE INTO balance_sheet
                        (period_id, line_item, xbrl_tag, value, unit)
                        VALUES (?, ?, ?, ?, 'USD')
                    """, (period_id, line_item, xbrl_tag, value))
                
                elif statement_type == "CASH_FLOW":
                    self.cursor.execute("""
                        INSERT OR REPLACE INTO cash_flow_statement
                        (period_id, line_item, xbrl_tag, value, unit, section)
                        VALUES (?, ?, ?, ?, 'USD', 'OPERATING')
                    """, (period_id, line_item, xbrl_tag, value))
            
            except sqlite3.Error as e:
                logger.error(f"Error inserting {xbrl_tag}: {e}")
        
        self.db.commit()
    
    def process_company_10k(self, ticker: str, cik: str, company_name: str) -> bool:
        """
        Complete pipeline: fetch 10-K data and insert into database
        
        Args:
            ticker: Stock ticker (e.g., 'AAPL')
            cik: Central Index Key
            company_name: Official company name
        
        Returns:
            Success/failure boolean
        """
        # Fetch data from SEC
        facts_json = self.fetch_company_facts(cik)
        if not facts_json:
            logger.error(f"Failed to fetch facts for {ticker}")
            return False
        
        # Insert company
        company_id = self.insert_company(ticker, cik, company_name)
        if not company_id:
            logger.error(f"Failed to insert company {ticker}")
            return False
        
        logger.info(f"✓ Inserted/found company: {company_name} (ID: {company_id})")
        
        # Extract all 10-K periods
        us_gaap = facts_json.get("facts", {}).get("us-gaap", {})
        
        # Use a known tag to extract all available 10-K periods
        net_income_data = us_gaap.get("NetIncomeLoss", [])
        
        periods_inserted = 0
        for entry in net_income_data:
            if entry.get("form") == "10-K":
                period_end = entry.get("end", "")
                fiscal_year = entry.get("fy", 0)
                accession = entry.get("accession", "")
                
                if not period_end or not fiscal_year:
                    continue
                
                # Insert period
                period_id = self.insert_financial_period(
                    company_id, period_end, fiscal_year, "10-K", accession
                )
                
                if period_id:
                    # Extract all facts for this period
                    facts = self.get_financial_facts_for_period(
                        facts_json, period_end, "10-K"
                    )
                    
                    # Insert facts
                    self.insert_financial_facts(period_id, facts)
                    periods_inserted += 1
                    
                    logger.info(f"  ✓ Period {period_end}: {len(facts)} financial facts loaded")
        
        logger.info(f"✓ Completed: {periods_inserted} 10-K periods processed\n")
        return periods_inserted > 0


if __name__ == "__main__":
    from database.schema import FinancialDatabaseSchema
    
    # Initialize database
    FinancialDatabaseSchema.initialize_database()
    
    # Example: Extract Apple's 10-K data
    conn = FinancialDatabaseSchema.get_connection()
    extractor = SECEDGARExtractor(conn)
    
    extractor.process_company_10k("AAPL", "0000320193", "Apple Inc.")
    
    conn.close()
