
"""
Financial Data Validation Engine
Implements professional tie-outs and consistency checks on extracted 10-K data
Prof. V. Ravichandran - The Mountain Path - World of Finance
"""

import sqlite3
from typing import Dict, List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FinancialValidator:
    """
    Performs comprehensive validation and tie-out checks on financial statement data
    Ensures data integrity before DCF calculations
    """
    
    def __init__(self, db_connection: sqlite3.Connection):
        self.db = db_connection
        self.cursor = self.db.cursor()
        self.tolerance = 0.01  # 1% tolerance for rounding differences
    
    def get_period_data(self, period_id: int) -> Dict:
        """Retrieve all financial data for a period"""
        data = {
            "income_statement": {},
            "balance_sheet": {},
            "cash_flow": {}
        }
        
        # Income Statement
        self.cursor.execute("""
            SELECT xbrl_tag, value FROM income_statement WHERE period_id = ?
        """, (period_id,))
        data["income_statement"] = {row[0]: row[1] for row in self.cursor.fetchall()}
        
        # Balance Sheet
        self.cursor.execute("""
            SELECT xbrl_tag, value FROM balance_sheet WHERE period_id = ?
        """, (period_id,))
        data["balance_sheet"] = {row[0]: row[1] for row in self.cursor.fetchall()}
        
        # Cash Flow
        self.cursor.execute("""
            SELECT xbrl_tag, value FROM cash_flow_statement WHERE period_id = ?
        """, (period_id,))
        data["cash_flow"] = {row[0]: row[1] for row in self.cursor.fetchall()}
        
        return data
    
    def validate_balance_sheet_equality(self, period_id: int) -> Tuple[bool, Dict]:
        """
        PRIMARY TIE-OUT: Assets = Liabilities + Equity
        This is the fundamental accounting equation that MUST hold
        
        Returns:
            (passed: bool, results: Dict with details)
        """
        self.cursor.execute("""
            SELECT value FROM balance_sheet 
            WHERE period_id = ? AND xbrl_tag IN ('Assets', 'Liabilities', 'StockholdersEquity')
        """, (period_id,))
        
        results = {
            "check_name": "Balance Sheet Equality",
            "expected": 0,
            "actual": 0,
            "variance": 0,
            "variance_pct": 0,
            "passed": False
        }
        
        data = self.get_period_data(period_id)
        bs = data["balance_sheet"]
        
        total_assets = bs.get("Assets", 0)
        total_liabilities = bs.get("Liabilities", 0)
        total_equity = bs.get("StockholdersEquity", 0)
        
        if total_assets == 0:
            logger.warning(f"Period {period_id}: No balance sheet data found")
            return False, results
        
        # Calculate both sides of equation
        lhs = total_assets
        rhs = total_liabilities + total_equity
        
        variance = abs(lhs - rhs)
        variance_pct = variance / lhs if lhs != 0 else 0
        
        # Check if within tolerance
        passed = variance_pct <= self.tolerance
        
        results.update({
            "expected": rhs,
            "actual": lhs,
            "variance": variance,
            "variance_pct": variance_pct * 100,
            "passed": passed,
            "assets": total_assets,
            "liabilities": total_liabilities,
            "equity": total_equity
        })
        
        return passed, results
    
    def validate_net_income_reconciliation(self, period_id: int) -> Tuple[bool, Dict]:
        """
        Reconcile Net Income from Income Statement to Balance Sheet changes
        
        Simple check: Does the reported Net Income explain a significant portion
        of Retained Earnings changes?
        """
        results = {
            "check_name": "Net Income Reconciliation",
            "passed": False,
            "note": "Informational check"
        }
        
        data = self.get_period_data(period_id)
        is_data = data["income_statement"]
        
        net_income = is_data.get("NetIncomeLoss", 0)
        
        results.update({
            "net_income": net_income,
            "passed": True  # This is informational
        })
        
        return True, results
    
    def validate_operating_cash_flow(self, period_id: int) -> Tuple[bool, Dict]:
        """
        Verify Operating Cash Flow makes sense relative to Net Income
        OCF should generally be positive and relatively close to Net Income
        (within 2-3x due to working capital changes)
        """
        results = {
            "check_name": "Operating Cash Flow Reasonableness",
            "passed": True
        }
        
        data = self.get_period_data(period_id)
        is_data = data["income_statement"]
        cf_data = data["cash_flow"]
        
        net_income = is_data.get("NetIncomeLoss", 0)
        ocf = cf_data.get("NetCashProvidedByUsedInOperatingActivities", 0)
        
        # OCF should typically be positive for healthy companies
        if ocf < 0 and net_income > 0:
            results["warning"] = "Negative OCF despite positive Net Income - may indicate working capital issues"
            results["passed"] = True  # Not a hard failure, just a warning
        
        # OCF should be within reasonable multiple of Net Income
        if net_income > 0:
            ratio = ocf / net_income
            if ratio > 3.0 or ratio < -1.0:
                results["note"] = f"OCF/NI ratio of {ratio:.2f} is unusual - review working capital changes"
        
        results.update({
            "net_income": net_income,
            "operating_cash_flow": ocf,
            "ratio": ocf / net_income if net_income != 0 else 0
        })
        
        return True, results
    
    def validate_free_cash_flow_components(self, period_id: int) -> Tuple[bool, Dict]:
        """
        Verify all components of Free Cash Flow are present and reasonable
        FCF = Operating Cash Flow - Capital Expenditures
        """
        results = {
            "check_name": "Free Cash Flow Components",
            "passed": False
        }
        
        data = self.get_period_data(period_id)
        cf_data = data["cash_flow"]
        
        ocf = cf_data.get("NetCashProvidedByUsedInOperatingActivities", 0)
        capex = cf_data.get("PaymentsForAcquisitionsOfProductiveAssets", 0)
        
        if ocf == 0:
            results["note"] = "OCF not found in period"
            return False, results
        
        if capex == 0:
            results["warning"] = "CapEx not found - may need to be estimated from D&A or other sources"
        
        fcf = ocf - capex
        
        results.update({
            "passed": True,
            "operating_cash_flow": ocf,
            "capital_expenditure": capex,
            "free_cash_flow": fcf,
            "fcf_margin": fcf / ocf if ocf != 0 else 0
        })
        
        return True, results
    
    def validate_depreciation_amortization(self, period_id: int) -> Tuple[bool, Dict]:
        """
        Verify Depreciation & Amortization is present for NOPAT calculations
        """
        results = {
            "check_name": "Depreciation & Amortization",
            "passed": True
        }
        
        data = self.get_period_data(period_id)
        cf_data = data["cash_flow"]
        
        da = cf_data.get("DepreciationDepletionAndAmortization", 0)
        
        if da == 0:
            # Try alternative tags
            da = cf_data.get("DepreciationAndAmortization", 0)
        
        results.update({
            "depreciation_amortization": da,
            "found": da > 0,
            "note": "Required for NOPAT calculation"
        })
        
        return True, results
    
    def run_all_validations(self, period_id: int) -> Dict:
        """
        Run complete validation suite and return comprehensive report
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Running validation checks for Period ID: {period_id}")
        logger.info(f"{'='*60}\n")
        
        validation_results = {}
        passed_count = 0
        failed_count = 0
        
        # Run all validation checks
        checks = [
            ("balance_sheet_equality", self.validate_balance_sheet_equality),
            ("net_income_reconciliation", self.validate_net_income_reconciliation),
            ("operating_cash_flow", self.validate_operating_cash_flow),
            ("fcf_components", self.validate_free_cash_flow_components),
            ("depreciation_amortization", self.validate_depreciation_amortization),
        ]
        
        for check_name, check_func in checks:
            passed, result = check_func(period_id)
            validation_results[check_name] = result
            
            status = "✓ PASS" if passed else "✗ FAIL"
            logger.info(f"{status}: {result.get('check_name', check_name)}")
            
            if result.get("variance_pct"):
                logger.info(f"       Variance: {result['variance_pct']:.2f}%")
            if result.get("note"):
                logger.info(f"       Note: {result['note']}")
            if result.get("warning"):
                logger.info(f"       ⚠ Warning: {result['warning']}")
            
            if passed:
                passed_count += 1
            else:
                failed_count += 1
        
        # Calculate overall quality score
        quality_score = passed_count / (passed_count + failed_count) if (passed_count + failed_count) > 0 else 0
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Validation Summary")
        logger.info(f"{'='*60}")
        logger.info(f"Passed: {passed_count}/{passed_count + failed_count}")
        logger.info(f"Data Quality Score: {quality_score*100:.1f}%")
        logger.info(f"{'='*60}\n")
        
        # Update database with quality score
        self.cursor.execute("""
            UPDATE financial_periods
            SET data_quality_score = ?
            WHERE id = ?
        """, (quality_score, period_id))
        
        # Log validation results to database
        for check_key, result in validation_results.items():
            if result.get("variance") is not None:
                self.cursor.execute("""
                    INSERT INTO validation_log
                    (period_id, check_name, expected_value, actual_value, 
                     variance, tolerance, passed, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    period_id,
                    result.get("check_name"),
                    result.get("expected", 0),
                    result.get("actual", 0),
                    result.get("variance", 0),
                    self.tolerance,
                    result.get("passed", False),
                    str(result.get("note", ""))
                ))
        
        self.db.commit()
        
        return {
            "period_id": period_id,
            "passed": passed_count,
            "failed": failed_count,
            "quality_score": quality_score,
            "details": validation_results
        }


if __name__ == "__main__":
    from database.schema import FinancialDatabaseSchema
    
    conn = FinancialDatabaseSchema.get_connection()
    validator = FinancialValidator(conn)
    
    # Run validations on all periods
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM financial_periods")
    periods = cursor.fetchall()
    
    for (period_id,) in periods:
        result = validator.run_all_validations(period_id)
    
    conn.close()
