"""
The Mountain Path - DCF Valuation Platform
Professional Financial Analysis Application
Prof. V. Ravichandran - 28+ Years Corporate Finance & Banking Experience
"""

# ============================================================================
# README: DCF VALUATION PLATFORM - COMPLETE IMPLEMENTATION GUIDE
# ============================================================================

## EXECUTIVE SUMMARY

This is a **production-grade Streamlit application** implementing a professional 
**Database-First architecture** for DCF (Discounted Cash Flow) valuation.

Key advantages over basic implementations:
- ✓ SEC EDGAR data as source of truth (not manual entry)
- ✓ Financial statement validation & tie-outs before calculations
- ✓ Multi-year historical analysis capability
- ✓ Fast query performance (no re-scraping)
- ✓ Proper data normalization and integrity

---

## ARCHITECTURE OVERVIEW

### 1. DATABASE LAYER (SQLite)
**File: database/schema.py**

```
companies
├── id, ticker, cik, company_name, sector
└── date_added, last_updated

financial_periods
├── company_id, period_end_date, fiscal_year
├── filing_type (10-K, 10-Q, 8-K)
└── data_quality_score

income_statement (normalized)
├── period_id, line_item, xbrl_tag, value

balance_sheet (normalized)
├── period_id, line_item, xbrl_tag, value

cash_flow_statement (normalized)
├── period_id, line_item, xbrl_tag, value, section

validation_log
├── period_id, check_name, expected, actual
├── variance, passed, check_date

dcf_calculations
├── company_id, base_year_id, projection_years
├── wacc, terminal_growth_rate
├── fcff_year_1 through fcff_year_5
├── enterprise_value, equity_value, price_per_share

fcff_components
├── dcf_calc_id, fiscal_year
├── ebit, tax_rate, nopat, da, capex
└── change_in_nwc, fcff
```

**Key Design Principles:**
- ✓ Normalized relational design (eliminates data redundancy)
- ✓ XBRL tag mapping (standardizes financial line items)
- ✓ Validation logging (audit trail of data quality)
- ✓ Multi-year support (enables historical analysis)

---

### 2. DATA EXTRACTION LAYER
**File: extraction/sec_extractor.py**

**Flow:**
1. Fetch Company Facts JSON from SEC EDGAR API
   - Direct access to source-of-truth financial data
   - Covers all available fiscal years automatically
   
2. Parse XBRL tags into standardized line items
   - Income Statement: Revenues, EBIT, NetIncome, etc.
   - Balance Sheet: Assets, Liabilities, Equity
   - Cash Flow: OCF, CapEx, D&A
   
3. Insert into normalized database tables
   - Eliminates manual data entry errors
   - Enables tie-outs before valuation

**Key Methods:**
```python
extractor.fetch_company_facts(cik)
  → Returns full Company Facts JSON from SEC
  
extractor.process_company_10k(ticker, cik, company_name)
  → Complete pipeline: fetch → parse → validate → insert
  
extractor.get_financial_facts_for_period(facts_json, period_end, filing_type)
  → Extract all facts for specific fiscal year
```

---

### 3. DATA VALIDATION LAYER
**File: validation/validator.py**

**Comprehensive Tie-Out Checks:**

1. **Balance Sheet Equality** (PRIMARY)
   ```
   Assets = Liabilities + Equity
   Tolerance: ±1%
   ```
   - Validates fundamental accounting equation
   - Catches data extraction errors

2. **Income Statement Reconciliation**
   - Verifies Net Income plausibility
   - Checks tax rate reasonableness

3. **Operating Cash Flow Validation**
   - OCF should be positive (healthy companies)
   - Reasonable ratio to Net Income (typically 0.5-2x)

4. **Free Cash Flow Components**
   ```
   FCF = OCF - CapEx
   ```
   - Verifies both OCF and CapEx present
   - Flags missing or unreasonable values

5. **Depreciation & Amortization**
   - Required for NOPAT calculation
   - Must exist for valuation

**Quality Score:**
- 0-1 metric based on passed validation checks
- Stored in database for audit trail
- Informs downstream analysis

---

### 4. VALUATION CALCULATION LAYERS

#### A. FCFF Calculator (valuation/fcff.py)

**Historical FCFF Calculation:**
```
FCFF = NOPAT + D&A - CapEx - Change in NWC
where:
  NOPAT = EBIT × (1 - Tax Rate)
  EBIT = Operating Income
  D&A = Depreciation & Amortization
  CapEx = Capital Expenditures
  NWC = Net Working Capital
```

**Key Methods:**
```python
calc.calculate_historical_fcff(company_id, years=5)
  → Extracts 5 years of FCFF components from database
  → Returns list of dicts with all FCFF calculations
  
calc.calculate_fcff_growth_rate(historical_fcff)
  → Analyzes growth patterns using CAGR
  → Suggests reasonable growth rates for projections
  
calc.project_fcff(base_fcff, growth_rates, years=5)
  → Projects future FCFF for explicit forecast period
  → Supports multiple growth rate profiles
```

#### B. DCF Valuation Engine (valuation/dcf.py)

**Valuation Formula:**
```
Enterprise Value = PV(Explicit FCFF) + PV(Terminal Value)

where:
  PV(Explicit FCFF) = Σ [FCFF_t / (1 + WACC)^t] for t=1 to N
  
  PV(Terminal Value) = [FCFF_final × (1 + g)] / (WACC - g)
                       ÷ (1 + WACC)^N
                       
  Terminal Value = Gordon Growth Model
                   (perpetuity growth formula)
```

**Bridge to Equity Value:**
```
Enterprise Value
├─ Less: Total Debt
├─ Plus: Cash & Equivalents
└─ = Equity Value

Equity Value ÷ Shares Outstanding = Intrinsic Value Per Share
```

**Key Methods:**
```python
engine.perform_dcf_valuation(
    company_id, base_period_id, fcff_projections,
    wacc=0.08, terminal_growth_rate=0.025
)
  → Complete valuation pipeline
  → Returns full valuation results dictionary
  
engine.calculate_terminal_value_perpetuity_growth(
    final_fcff, terminal_growth_rate, wacc
)
  → Gordon Growth Model terminal value
  → Must have WACC > Terminal Growth Rate
  
engine.calculate_enterprise_value(pv_explicit, pv_terminal)
  → Combines explicit period and terminal value
```

---

### 5. STREAMLIT APPLICATION LAYER

#### Application Structure:
```
streamlit_app/
├── app.py                          # Main entry point
├── config.py                       # Design system & defaults
├── styles.py                       # CSS styling
├── components.py                   # Reusable UI components
└── pages/
    ├── 01_dashboard.py            # Overview dashboard
    ├── 02_data_ingestion.py       # Load SEC EDGAR data
    ├── 03_validation.py           # Run tie-outs
    ├── 04_dcf_analysis.py         # DCF valuation
    ├── 05_sensitivity.py          # Sensitivity analysis
    └── 06_settings.py             # Configuration
```

#### Key Streamlit Features:

**1. Multi-Page Navigation**
- Each page is independent but shares database connection
- Clean separation of concerns
- Professional sidebar navigation

**2. Component Library (components.py)**
```python
ComponentLibrary.hero_header(title, subtitle, emoji)
  → Bold page header with branding
  
ComponentLibrary.metric_card(label, value, unit, card_type)
  → Formatted KPI display cards
  
ComponentLibrary.financial_table(df, format_columns)
  → Professional financial statement formatting
  
ComponentLibrary.alert(message, alert_type)
  → Info/Warning/Success/Error notifications
```

**3. Design System (config.py + styles.py)**
- Consistent color palette (Dark Blue #003366, Gold #FFD700)
- Professional typography
- Spacing and layout standards
- CSS styling for custom components

---

## SETUP & INSTALLATION

### Step 1: Environment Setup
```bash
# Create project directory
mkdir dcf_app && cd dcf_app

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install streamlit pandas sqlite3 numpy plotly requests
pip install edgartools  # Optional: for advanced SEC data access
```

### Step 2: Initialize Database
```python
from database.schema import FinancialDatabaseSchema

FinancialDatabaseSchema.initialize_database()
```

### Step 3: Load Sample Data
```python
from database.schema import FinancialDatabaseSchema
from extraction.sec_extractor import SECEDGARExtractor

conn = FinancialDatabaseSchema.get_connection()
extractor = SECEDGARExtractor(conn)

# Load Apple's 10-K data
extractor.process_company_10k("AAPL", "0000320193", "Apple Inc.")

conn.close()
```

### Step 4: Run Streamlit App
```bash
streamlit run streamlit_app/app.py
```

---

## USAGE WORKFLOW

### Workflow 1: Load New Company Data
1. Go to **Data Ingestion** page
2. Enter: Ticker, CIK, Company Name
3. Click "Fetch & Load Data"
4. System automatically:
   - Fetches all 10-K filings from SEC
   - Extracts financial facts
   - Normalizes into database

### Workflow 2: Validate Data Quality
1. Go to **Data Validation** page
2. Select period to validate
3. Click "Run Validation"
4. Review:
   - Balance sheet tie-out
   - Cash flow reconciliation
   - Data quality score

### Workflow 3: Perform DCF Valuation
1. Go to **DCF Analysis** page
2. Select company and base year
3. Input assumptions:
   - WACC (typically 7-10%)
   - Terminal Growth Rate (typically 2-3%)
   - Projection period (typically 5 years)
4. Click "Calculate Valuation"
5. Review results:
   - Intrinsic value per share
   - Enterprise value
   - FCFF projections
   - Valuation bridge

---

## ADVANCED TOPICS

### Custom Growth Rate Models

**1. Declining Growth Model**
```python
# Start with high growth, declining to terminal rate
growth_rates = [
    growth_rate * (1 - (i / projection_years))
    for i in range(projection_years)
]
```

**2. Two-Stage Model**
```python
# High growth for first N years, then stable
growth_rates = [0.12]*3 + [0.04]*2
```

**3. Multi-Stage Model**
```python
# Different growth rates for different periods
growth_rates = [0.15, 0.12, 0.10, 0.06, 0.04]
```

### Sensitivity Analysis

**Two-Way Sensitivity:**
```python
sensitivity_matrix = engine.sensitivity_analysis(
    enterprise_value=100000000,
    net_debt=20000000,
    shares_outstanding=1000000,
    wacc_range=(0.06, 0.12),
    terminal_gr_range=(0.02, 0.04)
)
```

Creates matrix showing intrinsic value under different assumptions.

### Historical Analysis

**Analyze FCFF Trends:**
```python
historical = fcff_calc.calculate_historical_fcff(company_id, years=5)
growth = fcff_calc.calculate_fcff_growth_rate(historical)

# Returns:
# - FCFF for each year
# - Implied CAGR
# - Warnings about trend changes
```

---

## PROFESSIONAL FEATURES

### Data Quality Tracking
- Every period gets quality score (0-1)
- Validation log stores all checks
- Enables data audit trail

### Comprehensive Tie-Outs
- Balance sheet equality check
- Income statement reconciliation
- Cash flow validation
- Working capital analysis

### Multi-Year Historical Analysis
- Load 5+ years of 10-K data
- Calculate growth trends
- Identify structural changes
- Inform projection assumptions

### Database Persistence
- All data stored locally
- No re-scraping on each calculation
- Fast query performance
- Enable scenario comparison

---

## KEY FINANCIAL FORMULAS

### Free Cash Flow to the Firm (FCFF)
```
FCFF = EBIT(1-T) + DA - CapEx - ΔNWC
```
- EBIT: Earnings Before Interest & Taxes
- T: Tax rate
- DA: Depreciation & Amortization (add back non-cash)
- CapEx: Capital expenditures (cash outflow)
- ΔNWC: Change in net working capital

### Terminal Value
```
TV = FCFF(final) × (1+g) / (WACC - g)
```
- Represents value of cash flows beyond forecast period
- Must use perpetual growth rate (typically 2-3%)
- WACC must exceed growth rate mathematically

### Enterprise Value
```
EV = PV(Explicit Period FCFF) + PV(Terminal Value)
```
- Sum of present value of all future FCFF
- Represents value of operations

### Equity Value Bridge
```
EV - Net Debt = Equity Value
Equity Value / Shares Outstanding = Price per Share
```

---

## COMMON ISSUES & SOLUTIONS

### Issue 1: SEC Connection Fails
**Solution:**
- Check internet connectivity
- Verify CIK format (10 digits with leading zeros)
- Wait and retry (SEC may rate-limit)

### Issue 2: No Balance Sheet Data
**Solution:**
- Ensure period was successfully loaded
- Check validation log for data quality issues
- May need to manually verify SEC filing

### Issue 3: WACC ≤ Terminal Growth Rate Error
**Solution:**
- Increase WACC (discount rate too low)
- Decrease terminal growth rate (growth assumption too high)
- Mathematically: WACC must be > Terminal Growth Rate

### Issue 4: Unreasonable Valuations
**Solution:**
- Check FCFF calculations
- Verify terminal growth rate (2-3% typical)
- Review historical FCFF trends
- Validate source data quality

---

## BEST PRACTICES

### 1. Data Validation First
✓ Always run validation before using data for valuations
✓ Check quality score >= 90%
✓ Review variance explanations

### 2. Conservative Assumptions
✓ Terminal growth rate: 2-3% (GDP growth)
✓ WACC: Reflects company risk (7-10% typical)
✓ Projection period: 5 years standard

### 3. Historical Analysis
✓ Analyze 5+ years of FCFF trends
✓ Identify one-time items
✓ Understand business cycles

### 4. Sensitivity Analysis
✓ Always run sensitivity to assumptions
✓ Present bull/base/bear scenarios
✓ Document key value drivers

### 5. Documentation
✓ Record all assumptions
✓ Keep audit trail of validations
✓ Save key results to database

---

## TECHNICAL STACK

**Backend:**
- Python 3.8+
- SQLite3 (database)
- Pandas (data manipulation)
- NumPy (numerical computing)

**Frontend:**
- Streamlit (web framework)
- Plotly (interactive charts)

**Data Source:**
- SEC EDGAR API (xbrl/companyfacts)
- Direct XBRL data extraction

---

## FILE STRUCTURE

```
dcf_app/
├── database/
│   └── schema.py                    # Database schema & initialization
├── extraction/
│   └── sec_extractor.py            # SEC EDGAR data extraction
├── validation/
│   └── validator.py                # Financial statement validation
├── valuation/
│   ├── fcff.py                     # FCFF calculation
│   └── dcf.py                      # DCF valuation engine
├── streamlit_app/
│   ├── app.py                      # Main Streamlit entry point
│   ├── config.py                   # Design system config
│   ├── styles.py                   # CSS styling
│   ├── components.py               # Reusable components
│   └── pages/
│       ├── 01_dashboard.py
│       ├── 02_data_ingestion.py
│       ├── 03_validation.py
│       ├── 04_dcf_analysis.py
│       ├── 05_sensitivity.py
│       └── 06_settings.py
├── data/
│   └── financial_database.db       # SQLite database
└── README.md                        # This file
```

---

## NEXT STEPS

1. **Setup Environment** - Install dependencies
2. **Initialize Database** - Create schema
3. **Load Data** - Add companies via SEC EDGAR
4. **Validate Data** - Run tie-outs
5. **Run Valuations** - Perform DCF calculations
6. **Analyze Results** - Review assumptions and outputs

---

## AUTHOR

Prof. V. Ravichandran
- 28+ Years Corporate Finance & Banking Experience
- 10+ Years Academic Excellence
- Specialized in Financial Risk Management & Modeling

---

## LICENSE & USAGE

This is professional-grade educational software created for finance students,
instructors, and professionals learning DCF valuation methodology.

---

**Last Updated:** January 2026
**Version:** 1.0 (Production Ready)
