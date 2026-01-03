"""
Financial Database Schema for 10-K Data Storage
Implements normalized relational design for professional DCF analysis
Prof. V. Ravichandran - The Mountain Path - World of Finance
"""

import sqlite3
from datetime import datetime
from pathlib import Path

class FinancialDatabaseSchema:
    """Initialize and manage financial data schema"""
    
    DB_PATH = Path("data/financial_database.db")
    
    CREATE_STATEMENTS = {
        "companies": """
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT UNIQUE NOT NULL,
                cik TEXT UNIQUE NOT NULL,
                company_name TEXT NOT NULL,
                sector TEXT,
                industry TEXT,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        
        "financial_periods": """
            CREATE TABLE IF NOT EXISTS financial_periods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                period_end_date DATE NOT NULL,
                fiscal_year INTEGER NOT NULL,
                fiscal_quarter INTEGER,  -- NULL for annual, 1-3 for Q1-Q3
                filing_type TEXT NOT NULL,  -- 10-K, 10-Q, 8-K
                filing_date DATE NOT NULL,
                accession_number TEXT UNIQUE,
                data_quality_score REAL,  -- 0-1, indicates validation pass rate
                FOREIGN KEY (company_id) REFERENCES companies(id),
                UNIQUE(company_id, period_end_date, filing_type)
            )
        """,
        
        "income_statement": """
            CREATE TABLE IF NOT EXISTS income_statement (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_id INTEGER NOT NULL,
                line_item TEXT NOT NULL,  -- NetIncomeLoss, Revenues, OperatingIncomeLoss, etc.
                xbrl_tag TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT DEFAULT 'USD',
                FOREIGN KEY (period_id) REFERENCES financial_periods(id),
                UNIQUE(period_id, xbrl_tag)
            )
        """,
        
        "balance_sheet": """
            CREATE TABLE IF NOT EXISTS balance_sheet (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_id INTEGER NOT NULL,
                line_item TEXT NOT NULL,  -- Assets, Liabilities, StockholdersEquity, etc.
                xbrl_tag TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT DEFAULT 'USD',
                side TEXT,  -- 'ASSET', 'LIABILITY', 'EQUITY'
                FOREIGN KEY (period_id) REFERENCES financial_periods(id),
                UNIQUE(period_id, xbrl_tag)
            )
        """,
        
        "cash_flow_statement": """
            CREATE TABLE IF NOT EXISTS cash_flow_statement (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_id INTEGER NOT NULL,
                line_item TEXT NOT NULL,  -- CapitalExpenditure, DepreciationAmortization, etc.
                xbrl_tag TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT DEFAULT 'USD',
                section TEXT,  -- 'OPERATING', 'INVESTING', 'FINANCING'
                FOREIGN KEY (period_id) REFERENCES financial_periods(id),
                UNIQUE(period_id, xbrl_tag)
            )
        """,
        
        "shares_outstanding": """
            CREATE TABLE IF NOT EXISTS shares_outstanding (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_id INTEGER NOT NULL,
                shares_issued REAL,
                shares_outstanding REAL,
                treasury_shares REAL,
                weighted_avg_shares REAL,
                FOREIGN KEY (period_id) REFERENCES financial_periods(id)
            )
        """,
        
        "validation_log": """
            CREATE TABLE IF NOT EXISTS validation_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_id INTEGER NOT NULL,
                check_name TEXT NOT NULL,
                expected_value REAL,
                actual_value REAL,
                variance REAL,
                tolerance REAL,
                passed BOOLEAN,
                check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (period_id) REFERENCES financial_periods(id)
            )
        """,
        
        "dcf_calculations": """
            CREATE TABLE IF NOT EXISTS dcf_calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                base_year_id INTEGER NOT NULL,
                calculation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                projection_years INTEGER,
                wacc REAL NOT NULL,
                terminal_growth_rate REAL NOT NULL,
                fcff_year_1 REAL,
                fcff_year_2 REAL,
                fcff_year_3 REAL,
                fcff_year_4 REAL,
                fcff_year_5 REAL,
                terminal_value REAL,
                enterprise_value REAL,
                equity_value REAL,
                price_per_share REAL,
                current_price REAL,
                upside_downside_pct REAL,
                FOREIGN KEY (company_id) REFERENCES companies(id),
                FOREIGN KEY (base_year_id) REFERENCES financial_periods(id)
            )
        """,
        
        "fcff_components": """
            CREATE TABLE IF NOT EXISTS fcff_components (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dcf_calc_id INTEGER NOT NULL,
                fiscal_year INTEGER,
                ebit REAL,
                tax_rate REAL,
                nopat REAL,  -- Net Operating Profit After Tax
                depreciation REAL,
                amortization REAL,
                capex REAL,
                change_in_nwc REAL,
                fcff REAL,
                FOREIGN KEY (dcf_calc_id) REFERENCES dcf_calculations(id)
            )
        """
    }
    
    # Mapping of common XBRL tags to standardized line items
    XBRL_TAG_MAPPING = {
        # Income Statement
        "Revenues": ["Revenues", "NetRevenues", "TotalNetRevenues"],
        "CostOfRevenue": ["CostOfRevenue", "CostOfGoodsAndServicesSold"],
        "GrossProfit": ["GrossProfit"],
        "OperatingExpenses": ["OperatingExpenses", "SG&A"],
        "OperatingIncome": ["OperatingIncomeLoss", "OperatingIncome"],
        "InterestExpense": ["InterestExpense"],
        "OtherIncome": ["OtherIncomeExpenseNet"],
        "IncomeTaxProvision": ["IncomeTaxExpenseBenefit"],
        "NetIncome": ["NetIncomeLoss", "NetIncome"],
        
        # Balance Sheet - Assets
        "Cash": ["Cash", "CashAndCashEquivalents"],
        "AccountsReceivable": ["AccountsReceivable", "AccountsReceivableNetCurrent"],
        "Inventory": ["InventoryNetCurrent"],
        "CurrentAssets": ["AssetsCurrent"],
        "LongTermAssets": ["AssetsNonCurrent"],
        "PPE": ["PropertyPlantAndEquipmentGross", "PropertyPlantAndEquipmentNet"],
        "Goodwill": ["Goodwill"],
        "IntangibleAssets": ["IntangibleAssetsNetOtherThanGoodwill"],
        "TotalAssets": ["Assets", "AssetsTotal"],
        
        # Balance Sheet - Liabilities
        "AccountsPayable": ["AccountsPayable"],
        "CurrentLiabilities": ["LiabilitiesCurrent"],
        "LongTermDebt": ["LongTermBorrowings", "LongTermDebt"],
        "TotalLiabilities": ["Liabilities"],
        "TotalStockholdersEquity": ["StockholdersEquity"],
        
        # Cash Flow Statement
        "OperatingCashFlow": ["NetCashProvidedByUsedInOperatingActivities"],
        "CapitalExpenditure": ["PaymentsForAcquisitionsOfProductiveAssets"],
        "Depreciation": ["DepreciationDepletionAndAmortization"],
        "DepreciationAndAmortization": ["DepreciationAndAmortization"],
    }
    
    @classmethod
    def initialize_database(cls):
        """Create database and all tables"""
        cls.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        try:
            for table_name, create_statement in cls.CREATE_STATEMENTS.items():
                cursor.execute(create_statement)
                print(f"✓ Created table: {table_name}")
            
            conn.commit()
            print("\n✓ Database initialized successfully")
        except sqlite3.Error as e:
            print(f"✗ Database initialization error: {e}")
        finally:
            conn.close()
    
    @classmethod
    def get_connection(cls):
        """Get database connection"""
        cls.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(cls.DB_PATH)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    @classmethod
    def drop_all_tables(cls):
        """WARNING: Drop all tables (for testing/reset only)"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        tables = [
            "fcff_components", "dcf_calculations", "validation_log",
            "shares_outstanding", "cash_flow_statement", "balance_sheet",
            "income_statement", "financial_periods", "companies"
        ]
        
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
        
        conn.commit()
        conn.close()
        print("✓ All tables dropped")


if __name__ == "__main__":
    FinancialDatabaseSchema.initialize_database()
