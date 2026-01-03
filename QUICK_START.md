"""
QUICK START GUIDE - 10 Minute Setup
The Mountain Path - DCF Valuation Platform
Prof. V. Ravichandran
"""

# ============================================================================
# QUICK START: Get Running in 10 Minutes
# ============================================================================

## STEP 1: Install Dependencies (2 minutes)

```bash
# Navigate to project directory
cd dcf_app

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install requirements
pip install -r requirements.txt
```

## STEP 2: Initialize Database (1 minute)

```bash
# In Python shell or create init_db.py:

from database.schema import FinancialDatabaseSchema

# Creates all tables
FinancialDatabaseSchema.initialize_database()
print("✓ Database initialized")
```

## STEP 3: Load Sample Data (5 minutes)

```python
from database.schema import FinancialDatabaseSchema
from extraction.sec_extractor import SECEDGARExtractor
import logging

logging.basicConfig(level=logging.INFO)

# Initialize
conn = FinancialDatabaseSchema.get_connection()
extractor = SECEDGARExtractor(conn)

# Load Apple's 10-K data
print("Loading Apple Inc...")
extractor.process_company_10k("AAPL", "0000320193", "Apple Inc.")

# Load Microsoft's 10-K data (optional)
print("Loading Microsoft...")
extractor.process_company_10k("MSFT", "0000789019", "Microsoft Corporation")

conn.close()
print("✓ Data loaded successfully")
```

## STEP 4: Run Streamlit App (2 minutes)

```bash
streamlit run streamlit_app/app.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## USING THE APPLICATION

### Once the app loads in your browser:

1. **Dashboard** (Default)
   - See overview of loaded data
   - Recent valuations summary

2. **Data Ingestion**
   - Add new companies from SEC EDGAR
   - View loaded companies and periods
   - Check database statistics

3. **Data Validation**
   - Run validation checks on loaded data
   - Review balance sheet tie-outs
   - Check data quality scores

4. **DCF Analysis**
   - Select company and base year
   - Input WACC and terminal growth rate
   - Run DCF valuation
   - View results and FCFF projections

5. **Settings**
   - Configure default assumptions
   - View database statistics
   - Clear cache if needed

---

## EXAMPLE WORKFLOW

### Load Microsoft 10-K Data

**On Data Ingestion Page:**
1. Enter:
   - Ticker: MSFT
   - CIK: 0000789019
   - Company: Microsoft Corporation
2. Click "Fetch & Load Data"
3. Wait for completion (~30 seconds)

### Validate Data

**On Data Validation Page:**
1. Select "MSFT - FY2023" from period selector
2. Click "Run Validation"
3. Review: Should see 100% quality score

### Run DCF Valuation

**On DCF Analysis Page:**
1. Select Company: "MSFT - Microsoft Corporation"
2. Select Base Year: "FY2023"
3. Set Assumptions:
   - WACC: 8.0%
   - Terminal Growth: 2.5%
   - Projection: 5 years
4. Click "Calculate Valuation"
5. Review results including intrinsic value per share

---

## TROUBLESHOOTING

### Problem: "Module not found" error
**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Problem: SEC connection fails
**Solution:**
- Check internet connection
- Verify CIK format (10 digits)
- Wait a few seconds and try again
- SEC may rate-limit requests

### Problem: "Database already exists"
**Solution:**
```python
# Use existing database, no need to reinitialize
# Or reset with:
FinancialDatabaseSchema.drop_all_tables()
FinancialDatabaseSchema.initialize_database()
```

### Problem: Streamlit app won't start
**Solution:**
```bash
# Try with verbose output
streamlit run --logger.level=debug streamlit_app/app.py

# Or check if port 8501 is in use
lsof -i :8501  # macOS/Linux
netstat -ano | findstr :8501  # Windows
```

---

## SAMPLE COMPANIES TO TRY

| Company | Ticker | CIK |
|---------|--------|-----|
| Apple Inc | AAPL | 0000320193 |
| Microsoft Corp | MSFT | 0000789019 |
| Amazon | AMZN | 0001018724 |
| Google/Alphabet | GOOGL | 0001652044 |
| Tesla | TSLA | 0001318605 |
| JPMorgan Chase | JPM | 0000047709 |
| Berkshire Hathaway | BRK.B | 0001067983 |
| Johnson & Johnson | JNJ | 0000200406 |
| Visa | V | 0001403161 |
| Mastercard | MA | 0001141391 |

---

## KEY CONCEPTS

### What is WACC?
Weighted Average Cost of Capital
- Required rate of return for the company
- Discount rate for future cash flows
- Typical range: 6-12% depending on risk

### What is Terminal Growth Rate?
- Perpetual growth rate assumed after explicit forecast period
- Typically 2-3% (GDP growth)
- Cannot exceed WACC mathematically

### What is FCFF?
Free Cash Flow to the Firm
- Cash available to all investors (debt and equity)
- Calculated from EBIT after tax, adjusted for non-cash items
- Used in DCF valuation as key metric

### What is Intrinsic Value?
- True economic value of a company based on DCF model
- Compare to current stock price for investment decision
- Upside/downside = (Intrinsic - Market Price) / Market Price

---

## NEXT STEPS AFTER RUNNING

1. **Load Multiple Companies**
   - Compare different industries
   - Analyze competitive positioning

2. **Run Sensitivity Analysis**
   - How does value change with WACC?
   - What terminal growth rate is implied?

3. **Historical Analysis**
   - Review 5-year FCFF trends
   - Identify structural changes

4. **Compare Valuations**
   - Save multiple scenarios
   - Bull/base/bear cases

5. **Export Results**
   - Create reports
   - Build presentations

---

## TECHNICAL NOTES

**Database Location:**
```
dcf_app/data/financial_database.db
```

**Application Logs:**
```
Check console output for debug information
Enable debug with: streamlit run --logger.level=debug
```

**SEC EDGAR Rate Limits:**
- ~50 requests per second
- Application handles delays automatically
- No API key required for public data

---

## PERFORMANCE TIPS

1. **First Run After Loading Data**
   - Validation can take 30-60 seconds
   - Subsequent runs use cache (fast)

2. **Database Size**
   - Apple with 10 years of data: ~2-3 MB
   - Not a concern for local SQLite

3. **Streamlit Cache**
   - Uses @st.cache_resource for database connection
   - Clear with Settings → "Clear Cache" if issues

---

## SUPPORT & RESOURCES

### Documentation
- README.md - Full reference guide
- Code comments - Detailed explanations
- Docstrings - Function documentation

### Learning Financial Concepts
- Investopedia: DCF Valuation
- Corporate Finance textbooks
- Academic finance courses

### Getting Help
1. Check README.md for detailed explanations
2. Review code comments in source files
3. Check SEC EDGAR website for company CIKs
4. Verify financial data in 10-K filings directly

---

## SUCCESS INDICATORS

When you've successfully set up:

✓ App loads without errors on http://localhost:8501
✓ Can load a company (Apple test recommended)
✓ Validation runs without errors
✓ DCF valuation completes successfully
✓ Intrinsic value calculated and displayed
✓ Results make economic sense

---

**Total Setup Time: ~10 minutes**
**Enjoyable financial analysis to follow!**

Prof. V. Ravichandran
The Mountain Path - World of Finance
