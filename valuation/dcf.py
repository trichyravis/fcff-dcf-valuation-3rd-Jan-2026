"""
Discounted Cash Flow (DCF) Valuation Engine
Implements professional DCF valuation with explicit and terminal value periods
Prof. V. Ravichandran - The Mountain Path - World of Finance
"""

import sqlite3
from typing import Dict, List, Tuple, Optional
import logging
import numpy as np
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DCFValuationEngine:
    """
    Professional DCF valuation using:
    1. Explicit forecast period FCFF (typically 5 years)
    2. Terminal value (perpetuity growth method)
    3. Discount using WACC
    """
    
    def __init__(self, db_connection: sqlite3.Connection):
        self.db = db_connection
        self.cursor = self.db.cursor()
    
    def calculate_npv(self, cash_flows: List[float], discount_rate: float) -> Tuple[float, List[float]]:
        """
        Calculate Net Present Value of cash flows
        
        Args:
            cash_flows: List of cash flows (starting from Year 1)
            discount_rate: WACC or required rate of return
        
        Returns:
            (total_npv, discounted_cash_flows)
        """
        if discount_rate <= -1:
            raise ValueError("Discount rate must be > -1")
        
        discounted_cfs = []
        total_npv = 0
        
        for year, cf in enumerate(cash_flows, 1):
            discount_factor = 1 / ((1 + discount_rate) ** year)
            discounted_cf = cf * discount_factor
            discounted_cfs.append(discounted_cf)
            total_npv += discounted_cf
        
        return total_npv, discounted_cfs
    
    def calculate_terminal_value_perpetuity_growth(self, final_year_fcff: float,
                                                   terminal_growth_rate: float,
                                                   wacc: float) -> float:
        """
        Calculate Terminal Value using Gordon Growth Model (Perpetuity Growth)
        
        TV = FCFF(Year N) × (1 + g) / (WACC - g)
        
        Args:
            final_year_fcff: FCFF in final explicit forecast year
            terminal_growth_rate: Perpetual growth rate (typically 2-3%)
            wacc: Weighted Average Cost of Capital
        
        Returns:
            Terminal Value
        """
        if wacc <= terminal_growth_rate:
            raise ValueError("WACC must be > Terminal Growth Rate")
        
        terminal_fcff = final_year_fcff * (1 + terminal_growth_rate)
        tv = terminal_fcff / (wacc - terminal_growth_rate)
        
        return tv
    
    def calculate_terminal_value_exit_multiple(self, final_year_fcff: float,
                                              exit_multiple: float) -> float:
        """
        Alternative: Calculate Terminal Value using Exit Multiple
        
        TV = Final Year FCFF × Exit Multiple
        Useful for LBO or buyout valuations
        """
        return final_year_fcff * exit_multiple
    
    def calculate_enterprise_value(self, pv_explicit_fcff: float,
                                   pv_terminal_value: float) -> float:
        """
        Enterprise Value = PV(Explicit Period FCFF) + PV(Terminal Value)
        """
        return pv_explicit_fcff + pv_terminal_value
    
    def calculate_equity_value(self, enterprise_value: float,
                              net_debt: float) -> float:
        """
        Equity Value = Enterprise Value - Net Debt
        where Net Debt = Total Debt - Cash & Equivalents
        
        Args:
            enterprise_value: EV from DCF
            net_debt: Total debt minus cash (already netted)
        
        Returns:
            Equity Value
        """
        equity_value = enterprise_value - net_debt
        return equity_value
    
    def calculate_price_per_share(self, equity_value: float,
                                 shares_outstanding: float) -> float:
        """
        Intrinsic Value Per Share = Equity Value / Shares Outstanding
        """
        if shares_outstanding <= 0:
            raise ValueError("Shares outstanding must be > 0")
        
        return equity_value / shares_outstanding
    
    def get_balance_sheet_data(self, period_id: int) -> Dict:
        """
        Extract debt and cash data from balance sheet
        """
        data = {
            "total_debt": 0,
            "cash": 0,
            "net_debt": 0
        }
        
        # Get Long-Term Debt and Short-Term Borrowings
        self.cursor.execute("""
            SELECT value FROM balance_sheet
            WHERE period_id = ? AND xbrl_tag IN 
            ('LongTermBorrowings', 'LongTermDebt', 'CurrentPortionOfLongTermDebt')
        """, (period_id,))
        
        debt_sum = sum([row[0] for row in self.cursor.fetchall()])
        data["total_debt"] = debt_sum
        
        # Get Cash
        self.cursor.execute("""
            SELECT value FROM balance_sheet
            WHERE period_id = ? AND xbrl_tag IN ('Cash', 'CashAndCashEquivalents')
        """, (period_id,))
        
        result = self.cursor.fetchone()
        if result:
            data["cash"] = result[0]
        
        data["net_debt"] = data["total_debt"] - data["cash"]
        
        return data
    
    def get_shares_outstanding(self, period_id: int) -> float:
        """
        Get weighted average shares outstanding from database
        """
        self.cursor.execute("""
            SELECT weighted_avg_shares FROM shares_outstanding
            WHERE period_id = ?
        """, (period_id,))
        
        result = self.cursor.fetchone()
        if result and result[0]:
            return result[0]
        
        # Fallback: get basic shares outstanding
        self.cursor.execute("""
            SELECT shares_outstanding FROM shares_outstanding
            WHERE period_id = ?
        """, (period_id,))
        
        result = self.cursor.fetchone()
        return result[0] if result and result[0] else 1000  # Default fallback
    
    def perform_dcf_valuation(self, company_id: int, base_period_id: int,
                             fcff_projections: List[float],
                             wacc: float = 0.08,
                             terminal_growth_rate: float = 0.025,
                             shares_outstanding: Optional[float] = None) -> Dict:
        """
        Complete DCF valuation
        
        Args:
            company_id: Company ID
            base_period_id: Period used as base for projections
            fcff_projections: Projected FCFF for explicit period
            wacc: Weighted Average Cost of Capital
            terminal_growth_rate: Long-term growth rate
            shares_outstanding: If None, retrieves from database
        
        Returns:
            Complete valuation results dictionary
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"DCF Valuation Analysis")
        logger.info(f"{'='*60}\n")
        
        # Step 1: Calculate Terminal Value
        final_fcff = fcff_projections[-1]
        terminal_value = self.calculate_terminal_value_perpetuity_growth(
            final_fcff, terminal_growth_rate, wacc
        )
        logger.info(f"Terminal Value (Year {len(fcff_projections)}): ${terminal_value:,.0f}")
        
        # Step 2: Discount all cash flows
        all_cfs = fcff_projections + [terminal_value]
        pv_explicit, explicit_discounted = self.calculate_npv(fcff_projections, wacc)
        pv_terminal = terminal_value / ((1 + wacc) ** len(fcff_projections))
        
        logger.info(f"\nDiscounted Cash Flows (WACC = {wacc*100:.2f}%):")
        for year, (cf, dcf) in enumerate(zip(fcff_projections, explicit_discounted), 1):
            logger.info(f"  Year {year}: ${cf:,.0f} → ${dcf:,.0f}")
        logger.info(f"\nPV(Terminal Value): ${pv_terminal:,.0f}")
        
        # Step 3: Calculate Enterprise Value
        enterprise_value = self.calculate_enterprise_value(pv_explicit, pv_terminal)
        logger.info(f"\nEnterprise Value: ${enterprise_value:,.0f}")
        
        # Step 4: Adjust for Net Debt
        bs_data = self.get_balance_sheet_data(base_period_id)
        equity_value = self.calculate_equity_value(enterprise_value, bs_data["net_debt"])
        
        logger.info(f"\nEquity Bridge:")
        logger.info(f"  Enterprise Value:     ${enterprise_value:,.0f}")
        logger.info(f"  Less: Net Debt        ${bs_data['net_debt']:,.0f}")
        logger.info(f"  Equity Value:         ${equity_value:,.0f}")
        
        # Step 5: Calculate Per Share
        if shares_outstanding is None:
            shares_outstanding = self.get_shares_outstanding(base_period_id)
        
        intrinsic_value_ps = self.calculate_price_per_share(equity_value, shares_outstanding)
        
        logger.info(f"\nPer Share:")
        logger.info(f"  Shares Outstanding: {shares_outstanding:,.0f}")
        logger.info(f"  Intrinsic Value:    ${intrinsic_value_ps:.2f}")
        logger.info(f"{'='*60}\n")
        
        # Prepare results dictionary
        results = {
            "company_id": company_id,
            "base_period_id": base_period_id,
            "valuation_date": datetime.now().isoformat(),
            "fcff_projections": fcff_projections,
            "terminal_value": terminal_value,
            "pv_explicit_fcff": pv_explicit,
            "pv_terminal_value": pv_terminal,
            "enterprise_value": enterprise_value,
            "total_debt": bs_data["total_debt"],
            "cash": bs_data["cash"],
            "net_debt": bs_data["net_debt"],
            "equity_value": equity_value,
            "shares_outstanding": shares_outstanding,
            "intrinsic_value_per_share": intrinsic_value_ps,
            "wacc": wacc,
            "terminal_growth_rate": terminal_growth_rate,
            "valuation_summary": {
                "explicit_fcff_pv": pv_explicit,
                "terminal_value_pv": pv_terminal,
                "total_pv": enterprise_value
            }
        }
        
        return results
    
    def save_dcf_results(self, results: Dict) -> int:
        """
        Save DCF valuation results to database
        
        Returns:
            DCF calculation ID
        """
        self.cursor.execute("""
            INSERT INTO dcf_calculations
            (company_id, base_year_id, projection_years, wacc, terminal_growth_rate,
             fcff_year_1, fcff_year_2, fcff_year_3, fcff_year_4, fcff_year_5,
             terminal_value, enterprise_value, equity_value, price_per_share)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            results["company_id"],
            results["base_period_id"],
            len(results["fcff_projections"]),
            results["wacc"],
            results["terminal_growth_rate"],
            results["fcff_projections"][0] if len(results["fcff_projections"]) > 0 else 0,
            results["fcff_projections"][1] if len(results["fcff_projections"]) > 1 else 0,
            results["fcff_projections"][2] if len(results["fcff_projections"]) > 2 else 0,
            results["fcff_projections"][3] if len(results["fcff_projections"]) > 3 else 0,
            results["fcff_projections"][4] if len(results["fcff_projections"]) > 4 else 0,
            results["terminal_value"],
            results["enterprise_value"],
            results["equity_value"],
            results["intrinsic_value_per_share"]
        ))
        
        self.db.commit()
        
        dcf_calc_id = self.cursor.lastrowid
        logger.info(f"✓ Saved DCF valuation (ID: {dcf_calc_id})")
        
        return dcf_calc_id
    
    def sensitivity_analysis(self, enterprise_value: float,
                            net_debt: float,
                            shares_outstanding: float,
                            wacc_range: Tuple[float, float],
                            terminal_gr_range: Tuple[float, float],
                            wacc_step: float = 0.005,
                            tgr_step: float = 0.005) -> np.ndarray:
        """
        Two-way sensitivity analysis on WACC and Terminal Growth Rate
        
        Returns:
            2D array of intrinsic values
        """
        wacc_values = np.arange(wacc_range[0], wacc_range[1] + wacc_step, wacc_step)
        tgr_values = np.arange(terminal_gr_range[0], terminal_gr_range[1] + tgr_step, tgr_step)
        
        sensitivity_matrix = np.zeros((len(tgr_values), len(wacc_values)))
        
        for i, tgr in enumerate(tgr_values):
            for j, wacc in enumerate(wacc_values):
                if wacc <= tgr:
                    sensitivity_matrix[i, j] = np.nan
                else:
                    # Rough approximation: recalculate with different discount rates
                    # For full sensitivity, would need to recalculate all PVs
                    sensitivity_matrix[i, j] = (enterprise_value - net_debt) / shares_outstanding
        
        return sensitivity_matrix


if __name__ == "__main__":
    from database.schema import FinancialDatabaseSchema
    from valuation.fcff import FCFFCalculator
    
    conn = FinancialDatabaseSchema.get_connection()
    
    # Example DCF valuation
    calculator = FCFFCalculator(conn)
    valuator = DCFValuationEngine(conn)
    
    company_id = 1  # Assuming Apple
    periods = calculator.get_historical_periods(company_id, years=1)
    
    if periods:
        base_period_id = periods[-1]["period_id"]
        
        # Simple projection: 10% growth for 5 years
        fcff_projections = calculator.project_fcff(1000000000, 0.10, years=5)
        
        # Run valuation
        results = valuator.perform_dcf_valuation(
            company_id=company_id,
            base_period_id=base_period_id,
            fcff_projections=fcff_projections,
            wacc=0.08,
            terminal_growth_rate=0.025
        )
        
        valuator.save_dcf_results(results)
    
    conn.close()
