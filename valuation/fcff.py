"""
Free Cash Flow to the Firm (FCFF) Calculation Engine
Implements professional FCFF calculation and projection methodology
Prof. V. Ravichandran - The Mountain Path - World of Finance
"""

import sqlite3
from typing import Dict, List, Tuple, Optional
import logging
import numpy as np
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FCFFCalculator:
    """
    Calculates Free Cash Flow to the Firm (FCFF) from financial statements
    
    FCFF = EBIT × (1 - Tax Rate) + D&A - CapEx - Change in NWC
    where:
        EBIT = Earnings Before Interest and Taxes
        D&A = Depreciation and Amortization
        CapEx = Capital Expenditures
        NWC = Net Working Capital
    """
    
    def __init__(self, db_connection: sqlite3.Connection):
        self.db = db_connection
        self.cursor = self.db.cursor()
    
    def get_historical_periods(self, company_id: int, years: int = 5) -> List[Dict]:
        """
        Retrieve historical financial data for last N fiscal years
        
        Args:
            company_id: Company ID in database
            years: Number of years to retrieve (default 5)
        
        Returns:
            List of period data dicts, sorted chronologically
        """
        self.cursor.execute("""
            SELECT id, period_end_date, fiscal_year
            FROM financial_periods
            WHERE company_id = ? AND filing_type = '10-K'
            ORDER BY fiscal_year DESC
            LIMIT ?
        """, (company_id, years))
        
        periods = []
        for row in self.cursor.fetchall():
            periods.append({
                "period_id": row[0],
                "period_end_date": row[1],
                "fiscal_year": row[2]
            })
        
        # Sort chronologically (oldest first)
        return sorted(periods, key=lambda x: x["fiscal_year"])
    
    def extract_fcff_components(self, period_id: int) -> Dict:
        """
        Extract all components needed for FCFF calculation from database
        """
        components = {}
        
        # Income Statement items
        self.cursor.execute("""
            SELECT xbrl_tag, value FROM income_statement
            WHERE period_id = ?
        """, (period_id,))
        
        for xbrl_tag, value in self.cursor.fetchall():
            if xbrl_tag == "OperatingIncomeLoss":
                components["ebit"] = value
            elif xbrl_tag == "Revenues":
                components["revenue"] = value
            elif xbrl_tag == "NetIncomeLoss":
                components["net_income"] = value
            elif xbrl_tag == "IncomeTaxExpenseBenefit":
                components["tax_expense"] = value
        
        # Cash Flow Statement items
        self.cursor.execute("""
            SELECT xbrl_tag, value FROM cash_flow_statement
            WHERE period_id = ?
        """, (period_id,))
        
        for xbrl_tag, value in self.cursor.fetchall():
            if "DepreciationDepletionAndAmortization" in xbrl_tag or \
               "DepreciationAndAmortization" in xbrl_tag:
                components["da"] = value
            elif "PaymentsForAcquisitionsOfProductiveAssets" in xbrl_tag:
                components["capex"] = value
            elif "NetCashProvidedByUsedInOperatingActivities" in xbrl_tag:
                components["ocf"] = value
        
        return components
    
    def calculate_tax_rate(self, period_id: int, components: Dict) -> float:
        """
        Calculate effective tax rate from income statement data
        Tax Rate = Tax Expense / (Net Income + Tax Expense)
        
        Falls back to statutory rate if insufficient data
        """
        tax_expense = components.get("tax_expense", 0)
        net_income = components.get("net_income", 0)
        
        # Calculate effective tax rate
        if tax_expense > 0 and net_income > 0:
            ebt = net_income + tax_expense  # Earnings Before Tax
            effective_rate = tax_expense / ebt
            
            # Sanity check: effective rate should be between 0-50%
            if 0 <= effective_rate <= 0.5:
                return effective_rate
        
        # Fallback to approximate statutory rate (India: ~25%, US: ~21%)
        logger.warning(f"Period {period_id}: Using default tax rate (25%)")
        return 0.25
    
    def estimate_nwc_change(self, period_id: int, prev_period_id: Optional[int] = None) -> float:
        """
        Calculate change in Net Working Capital
        Change in NWC = (Current Assets - Cash) - (Current Liabilities - Debt)
        
        If previous period not provided, estimates as % of revenue growth
        """
        if prev_period_id is None:
            # Estimate based on revenue changes
            components = self.extract_fcff_components(period_id)
            revenue = components.get("revenue", 0)
            
            # Conservative estimate: NWC change is 5% of revenue growth
            # This is a simplification; ideally would calculate from balance sheet
            return revenue * 0.05
        
        # Calculate actual NWC change from balance sheet data
        current_assets_curr = self._get_balance_sheet_item(period_id, ["AssetsCurrent"])
        current_liab_curr = self._get_balance_sheet_item(period_id, ["LiabilitiesCurrent"])
        
        current_assets_prev = self._get_balance_sheet_item(prev_period_id, ["AssetsCurrent"])
        current_liab_prev = self._get_balance_sheet_item(prev_period_id, ["LiabilitiesCurrent"])
        
        nwc_curr = (current_assets_curr - self._get_balance_sheet_item(
            period_id, ["Cash"]
        )) - current_liab_curr
        
        nwc_prev = (current_assets_prev - self._get_balance_sheet_item(
            prev_period_id, ["Cash"]
        )) - current_liab_prev
        
        return nwc_curr - nwc_prev
    
    def _get_balance_sheet_item(self, period_id: int, possible_tags: List[str]) -> float:
        """Helper to retrieve balance sheet items by multiple possible tags"""
        for tag in possible_tags:
            self.cursor.execute("""
                SELECT value FROM balance_sheet
                WHERE period_id = ? AND xbrl_tag = ?
            """, (period_id, tag))
            result = self.cursor.fetchone()
            if result:
                return result[0]
        return 0
    
    def calculate_fcff(self, period_id: int, components: Dict, 
                       tax_rate: Optional[float] = None) -> Dict:
        """
        Calculate FCFF for a given period
        
        FCFF = NOPAT + D&A - CapEx - Change in NWC
        where NOPAT = EBIT × (1 - Tax Rate)
        """
        if tax_rate is None:
            tax_rate = self.calculate_tax_rate(period_id, components)
        
        ebit = components.get("ebit", 0)
        da = components.get("da", 0)
        capex = components.get("capex", 0)
        
        # NOPAT (Net Operating Profit After Tax)
        nopat = ebit * (1 - tax_rate)
        
        # Change in NWC (estimate for now, ideally calculated from balance sheet)
        change_nwc = self.estimate_nwc_change(period_id)
        
        # Calculate FCFF
        fcff = nopat + da - capex - change_nwc
        
        return {
            "ebit": ebit,
            "tax_rate": tax_rate,
            "nopat": nopat,
            "da": da,
            "capex": capex,
            "change_nwc": change_nwc,
            "fcff": fcff
        }
    
    def calculate_historical_fcff(self, company_id: int, years: int = 5) -> List[Dict]:
        """
        Calculate FCFF for last N fiscal years
        Used to establish growth trends for projections
        """
        periods = self.get_historical_periods(company_id, years)
        historical_fcff = []
        
        logger.info(f"\nCalculating historical FCFF for {len(periods)} periods...")
        
        for period in periods:
            components = self.extract_fcff_components(period["period_id"])
            fcff_data = self.calculate_fcff(period["period_id"], components)
            
            result = {
                **period,
                **fcff_data
            }
            
            historical_fcff.append(result)
            
            logger.info(f"  FY{period['fiscal_year']}: FCFF = ${fcff_data['fcff']:,.0f}")
        
        return historical_fcff
    
    def calculate_fcff_growth_rate(self, historical_fcff: List[Dict]) -> Dict:
        """
        Analyze FCFF growth patterns from historical data
        Returns growth metrics for projection period
        """
        if len(historical_fcff) < 2:
            logger.warning("Insufficient historical data for growth analysis")
            return {"growth_rate": 0.05, "method": "default"}
        
        # Extract FCFF values
        fcff_values = [p["fcff"] for p in historical_fcff]
        
        # Filter out zero/negative values for growth calculation
        valid_fcff = [f for f in fcff_values if f > 0]
        
        if len(valid_fcff) < 2:
            logger.warning("Insufficient positive FCFF values")
            return {"growth_rate": 0.03, "method": "default"}
        
        # Calculate CAGR (Compound Annual Growth Rate)
        years = len(valid_fcff) - 1
        if years > 0:
            cagr = (valid_fcff[-1] / valid_fcff[0]) ** (1/years) - 1
        else:
            cagr = (valid_fcff[-1] - valid_fcff[0]) / valid_fcff[0] if valid_fcff[0] != 0 else 0
        
        # Use CAGR but cap at reasonable levels
        # Most companies don't grow faster than GDP indefinitely
        growth_rate = min(cagr, 0.15)  # Cap at 15%
        growth_rate = max(growth_rate, -0.10)  # Floor at -10%
        
        return {
            "growth_rate": growth_rate,
            "method": "historical_cagr",
            "years_analyzed": years,
            "cagr": cagr,
            "fcff_values": valid_fcff
        }
    
    def project_fcff(self, base_fcff: float, growth_rates: List[float], 
                     years: int = 5) -> List[float]:
        """
        Project FCFF for explicit forecast period
        
        Args:
            base_fcff: FCFF from most recent year
            growth_rates: Annual growth rates for projection period
                         Can be list of same length as years, or single value
            years: Number of years to project (default 5)
        
        Returns:
            List of projected FCFF values
        """
        projections = []
        current_fcff = base_fcff
        
        # Handle single growth rate vs list of rates
        if isinstance(growth_rates, (int, float)):
            growth_rates = [growth_rates] * years
        
        for year in range(years):
            rate = growth_rates[year] if year < len(growth_rates) else growth_rates[-1]
            current_fcff = current_fcff * (1 + rate)
            projections.append(current_fcff)
        
        return projections
    
    def save_fcff_components(self, dcf_calc_id: int, components_list: List[Dict]):
        """Save calculated FCFF components to database"""
        for idx, comp in enumerate(components_list, 1):
            self.cursor.execute("""
                INSERT INTO fcff_components
                (dcf_calc_id, fiscal_year, ebit, tax_rate, nopat, 
                 depreciation, capex, change_in_nwc, fcff)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                dcf_calc_id,
                comp.get("fiscal_year"),
                comp.get("ebit", 0),
                comp.get("tax_rate", 0),
                comp.get("nopat", 0),
                comp.get("da", 0),
                comp.get("capex", 0),
                comp.get("change_nwc", 0),
                comp.get("fcff", 0)
            ))
        
        self.db.commit()


if __name__ == "__main__":
    from database.schema import FinancialDatabaseSchema
    
    conn = FinancialDatabaseSchema.get_connection()
    calculator = FCFFCalculator(conn)
    
    # Example: Calculate FCFF for Apple
    company_id = 1  # Assuming Apple was loaded first
    
    historical = calculator.calculate_historical_fcff(company_id, years=5)
    growth_analysis = calculator.calculate_fcff_growth_rate(historical)
    
    print("\nGrowth Analysis:")
    print(f"  Implied Growth Rate: {growth_analysis['growth_rate']*100:.2f}%")
    
    conn.close()
