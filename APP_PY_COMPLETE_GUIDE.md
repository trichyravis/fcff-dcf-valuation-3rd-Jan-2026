"""
MAIN APP.PY FILE - COMPLETE BREAKDOWN
The Mountain Path - DCF Valuation Platform
Prof. V. Ravichandran
"""

# ============================================================================
# 📄 MAIN APPLICATION FILE: streamlit_app/app.py
# ============================================================================

## FILE OVERVIEW

**Location**: `streamlit_app/app.py`
**Size**: 299 lines
**Purpose**: Main entry point for the Streamlit application
**Role**: Handles:
- Page configuration
- Professional UI styling
- Multi-page navigation
- Database initialization
- Sidebar design
- Application header/footer

---

## 📋 FILE STRUCTURE (Section by Section)

### SECTION 1: Module Header & Imports (Lines 1-18)

```python
"""
DCF Valuation Platform - Main Application
The Mountain Path - World of Finance
Multi-page Streamlit application for professional financial analysis
Prof. V. Ravichandran
"""

import streamlit as st
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from streamlit_app.config import BRANDING, COLORS, FEATURES
from streamlit_app.styles import apply_styles
from streamlit_app.components import ComponentLibrary
from database.schema import FinancialDatabaseSchema
```

**What it does:**
- ✅ Imports Streamlit framework
- ✅ Imports configuration (colors, branding, features)
- ✅ Imports styling system
- ✅ Imports database schema for initialization
- ✅ Sets up Python path for relative imports

---

### SECTION 2: Page Configuration (Lines 20-26)

```python
st.set_page_config(
    page_title=BRANDING["name"],
    page_icon=BRANDING["logo_emoji"],
    layout="wide",
    initial_sidebar_state="expanded"
)
```

**Configuration:**
- **page_title**: "The Mountain Path - DCF Valuation Platform"
- **page_icon**: 🏔️ (Mountain emoji)
- **layout**: "wide" (full-width layout, no sidebar space limit)
- **initial_sidebar_state**: "expanded" (sidebar open by default)

**Result:** Browser tab shows mountain emoji, full-width layout with sidebar open

---

### SECTION 3: Styling & Theme (Lines 28-29)

```python
apply_styles(st)
```

**What it does:**
- ✅ Applies CSS styling from `styles.py`
- ✅ Sets colors to dark blue, light blue, gold theme
- ✅ Configures fonts, spacing, component styling
- ✅ Makes all components look professional and consistent

---

### SECTION 4: Database Initialization (Lines 31-41)

```python
@st.cache_resource
def init_database():
    """Initialize database on first run"""
    FinancialDatabaseSchema.initialize_database()
    return FinancialDatabaseSchema.get_connection()

# Initialize session state
if "database_initialized" not in st.session_state:
    init_database()
    st.session_state.database_initialized = True
```

**What it does:**
- ✅ Creates database if it doesn't exist
- ✅ Creates 9 financial data tables
- ✅ Uses `@st.cache_resource` so it only runs once (performance)
- ✅ Tracks initialization in session state

**When it runs:** First time app loads (not on every refresh)

---

### SECTION 5: Session State Initialization (Lines 43-47)

```python
if "selected_company" not in st.session_state:
    st.session_state.selected_company = None

if "selected_period" not in st.session_state:
    st.session_state.selected_period = None
```

**What it does:**
- ✅ Initializes variables that persist across page reloads
- ✅ `selected_company`: Stores which company user selected
- ✅ `selected_period`: Stores which fiscal period user selected
- ✅ These values are shared across all pages

**Why needed:** Streamlit reruns entire script on every interaction. Session state keeps values persistent.

---

### SECTION 6: PROFESSIONAL SIDEBAR (Lines 49-179)

#### Part A: Sidebar Header (Lines 52-71)

```python
with st.sidebar:
    sidebar_header = f"""
    <div style='
        background: linear-gradient(135deg, {COLORS["dark_blue"]} 0%, {COLORS["dark_blue"]} 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    '>
        <div style='text-align: center; color: white;'>
            <div style='font-size: 32px; margin-bottom: 10px;'>{BRANDING["logo_emoji"]}</div>
            <div style='font-size: 14px; font-weight: 700; letter-spacing: 0.5px;'>
                THE MOUNTAIN PATH
            </div>
            <div style='font-size: 11px; margin-top: 5px; opacity: 0.9;'>
                WORLD OF FINANCE
            </div>
        </div>
    </div>
    """
    st.markdown(sidebar_header, unsafe_allow_html=True)
```

**Displays:**
```
┌─────────────────────────────┐
│         🏔️                  │
│     THE MOUNTAIN PATH       │
│     WORLD OF FINANCE        │
└─────────────────────────────┘
```

**Styling:**
- Dark blue gradient background
- White text
- Rounded corners
- Shadow effect
- Centered logo

---

#### Part B: Navigation Menu (Lines 73-98)

```python
st.markdown("""...""")  # Section label

pages = {
    "🏠 Dashboard": "pages/01_dashboard.py",
    "📥 Data Ingestion": "pages/02_data_ingestion.py",
    "✓ Data Validation": "pages/03_validation.py",
    "📊 DCF Analysis": "pages/04_dcf_analysis.py",
    "🔍 Sensitivity Analysis": "pages/05_sensitivity.py",
    "⚙️ Settings": "pages/06_settings.py"
}

page = st.radio("", options=list(pages.keys()), label_visibility="collapsed")
```

**Displays:**
```
📍 NAVIGATION
─────────────────
◉ 🏠 Dashboard
○ 📥 Data Ingestion
○ ✓ Data Validation
○ 📊 DCF Analysis
○ 🔍 Sensitivity Analysis
○ ⚙️ Settings
```

**Functionality:**
- ✅ 6 navigation buttons (radio selection)
- ✅ Emoji icons for visual identification
- ✅ User clicks to navigate between pages
- ✅ Selected page is routed at bottom of file

---

#### Part C: Professional Credentials (Lines 101-132)

```python
st.markdown("""...""")  # "👤 Professional" header

author_card = f"""
<div style='
    background: linear-gradient(135deg, {COLORS["light_blue"]} 0%, rgba(173,216,230,0.3) 100%);
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid {COLORS["gold"]};
    margin-bottom: 15px;
'>
    <div style='font-weight: 700; color: {COLORS["dark_blue"]}; margin-bottom: 5px; font-size: 13px;'>
        {BRANDING['author']}
    </div>
    <div style='font-size: 11px; color: #666; line-height: 1.5;'>
        {BRANDING['byline'].replace(chr(10), '<br/>')}
    </div>
</div>
"""
st.markdown(author_card, unsafe_allow_html=True)
```

**Displays:**
```
┌─────────────────────────────┐
│ Prof. V. Ravichandran       │
│ 28+ Years Corporate Finance │
│ 10+ Years Academic Excel.   │
└─────────────────────────────┘
```

**Design:**
- Light blue background
- Gold left border accent
- Author name in bold
- Credentials below
- Professional card styling

---

#### Part D: Features Status (Lines 136-155)

```python
st.markdown("""...""")  # "⚡ Features" header

for feature_name, enabled in FEATURES.items():
    status = "✓ Enabled" if enabled else "✗ Disabled"
    status_color = COLORS["success"] if enabled else COLORS["neutral"]
    feature_label = feature_name.replace("_", " ").title()
    st.caption(f"<span style='color: {status_color};'>{status}</span> — {feature_label}")
```

**Displays:**
```
⚡ FEATURES
──────────────────
✓ Enabled — SEC EDGAR Integration
✓ Enabled — Data Validation
✓ Enabled — DCF Analysis
```

**Functionality:**
- ✅ Reads from `FEATURES` dictionary in config.py
- ✅ Shows which features are enabled/disabled
- ✅ Green checkmark for enabled
- ✅ Red X for disabled

---

#### Part E: Sidebar Footer (Lines 159-179)

```python
sidebar_footer = f"""
<div style='
    text-align: center;
    padding: 15px;
    border-top: 1px solid {COLORS["light_gray"]};
    margin-top: 20px;
    color: #999;
    font-size: 11px;
'>
    <div style='margin-bottom: 8px;'>
        <strong style='color: {COLORS["dark_blue"]}; font-size: 12px;'>Version</strong><br/>
        1.0 Production Ready
    </div>
    <div style='font-size: 10px; opacity: 0.7;'>
        © 2026 Mountain Path Finance<br/>
        All Rights Reserved
    </div>
</div>
"""
```

**Displays:**
```
─────────────────────────────
        Version
   1.0 Production Ready

© 2026 Mountain Path Finance
    All Rights Reserved
```

---

### SECTION 7: MAIN CONTENT HEADER (Lines 181-212)

```python
main_header = f"""
<div style='
    background: linear-gradient(90deg, {COLORS["dark_blue"]} 0%, {COLORS["dark_blue"]} 70%, {COLORS["gold"]} 100%);
    padding: 30px 40px;
    border-radius: 12px;
    margin-bottom: 30px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    color: white;
'>
    <div style='display: flex; align-items: center; justify-content: space-between;'>
        <div>
            <div style='font-size: 12px; letter-spacing: 2px; text-transform: uppercase;'>
                🏛️ INSTITUTIONAL FINANCIAL ANALYSIS
            </div>
            <h1 style='margin: 0; font-size: 36px; font-weight: 700;'>
                {BRANDING["logo_emoji"]} {BRANDING["name"]}
            </h1>
            <div style='font-size: 13px; margin-top: 8px; opacity: 0.85;'>
                {BRANDING["subtitle"]}
            </div>
        </div>
        <div style='text-align: right; font-size: 11px;'>
            <div style='margin-bottom: 4px;'><strong>Prof. V. Ravichandran</strong></div>
            <div>28+ Years Corporate Finance</div>
            <div>10+ Years Academic Excellence</div>
        </div>
    </div>
</div>
"""
st.markdown(main_header, unsafe_allow_html=True)
```

**Displays:**
```
┌──────────────────────────────────────────────────────────────┐
│ 🏛️ INSTITUTIONAL FINANCIAL ANALYSIS                           │
│ 🏔️ The Mountain Path - DCF Valuation Platform                │
│ Professional DCF valuation using Streamlit                   │
│                      Prof. V. Ravichandran                    │
│                      28+ Years Corporate Finance              │
│                      10+ Years Academic Excellence            │
└──────────────────────────────────────────────────────────────┘
```

**Design:**
- Dark blue to gold gradient
- Large title (36px)
- Subtitle below
- Right-aligned author credentials
- Shadow and rounded corners

---

### SECTION 8: PAGE ROUTING (Lines 214-237)

```python
if page == "🏠 Dashboard":
    import pages.dashboard as dashboard_page
    dashboard_page.render()

elif page == "📥 Data Ingestion":
    import pages.data_ingestion as ingestion_page
    ingestion_page.render()

elif page == "✓ Data Validation":
    import pages.validation as validation_page
    validation_page.render()

elif page == "📊 DCF Analysis":
    import pages.dcf_analysis as dcf_page
    dcf_page.render()

elif page == "🔍 Sensitivity Analysis":
    import pages.sensitivity as sensitivity_page
    sensitivity_page.render()

elif page == "⚙️ Settings":
    import pages.settings as settings_page
    settings_page.render()
```

**How it works:**
1. User selects a page from navigation menu
2. Selected page stored in `page` variable
3. Based on selection, imports and runs that page's `render()` function
4. Only the selected page's content displays

**Example flow:**
```
User clicks "🏠 Dashboard"
    ↓
page = "🏠 Dashboard"
    ↓
Matches first if statement
    ↓
Imports pages.dashboard
    ↓
Calls dashboard_page.render()
    ↓
Dashboard content displays
```

---

### SECTION 9: PROFESSIONAL FOOTER (Lines 239-298)

```python
st.divider()  # Horizontal line separator

footer_html = f"""
<div style='
    background: linear-gradient(90deg, rgba(0,51,102,0.05) 0%, rgba(255,215,0,0.05) 100%);
    padding: 30px 40px;
    border-radius: 10px;
    margin-top: 40px;
    border-top: 3px solid {COLORS["gold"]};
    border-bottom: 1px solid {COLORS["light_blue"]};
'>
    <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 30px; text-align: center;'>
        <div>
            <div style='font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: {COLORS["dark_blue"]}; font-weight: 700; margin-bottom: 5px;'>
                APPLICATION
            </div>
            <div style='font-size: 12px; color: #666;'>
                The Mountain Path<br/>DCF Valuation Platform
            </div>
        </div>
        <div>
            <div style='font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: {COLORS["dark_blue"]}; font-weight: 700; margin-bottom: 5px;'>
                CREATOR
            </div>
            <div style='font-size: 12px; color: #666;'>
                Prof. V. Ravichandran<br/>
                <span style='font-size: 11px; color: #999;'>28+ Years Finance | 10+ Years Academic</span>
            </div>
        </div>
        <div>
            <div style='font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: {COLORS["dark_blue"]}; font-weight: 700; margin-bottom: 5px;'>
                VERSION
            </div>
            <div style='font-size: 12px; color: #666;'>
                1.0 Production Ready<br/>
                <span style='font-size: 11px; color: #999;'>January 2026</span>
            </div>
        </div>
    </div>
    <div style='
        text-align: center; 
        margin-top: 20px; 
        padding-top: 20px; 
        border-top: 1px solid {COLORS["light_blue"]};
        color: #999; 
        font-size: 10px;
    '>
        <strong style='color: {COLORS["dark_blue"]}; font-size: 11px;'>
            🏔️ The Mountain Path - World of Finance
        </strong><br/>
        Professional Financial Analysis Platform | © 2026 All Rights Reserved<br/>
        <span style='color: {COLORS["success"]}; margin-top: 5px; display: inline-block;'>
            ✓ Production Ready | Database-First Architecture | SEC EDGAR Integration
        </span>
    </div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
```

**Displays:**
```
──────────────────────────────────────────────────────────────
    APPLICATION          CREATOR              VERSION
    The Mountain Path    Prof. V. Ravichandran   1.0 Production
    DCF Valuation...     28+ Years Finance       Ready

🏔️ The Mountain Path - World of Finance
Professional Financial Analysis Platform | © 2026 All Rights Reserved
✓ Production Ready | Database-First Architecture | SEC EDGAR Integration
──────────────────────────────────────────────────────────────
```

**Design:**
- Three-column grid layout
- Gold top border, blue bottom border
- Subtle gradient background
- Professional footer styling
- Status badges

---

## 📊 FILE EXECUTION FLOW

```
1. Load app.py
   ↓
2. Import modules & config
   ↓
3. Set page configuration (wide layout, sidebar expanded)
   ↓
4. Apply CSS styling
   ↓
5. Initialize database (first run only)
   ↓
6. Render SIDEBAR:
   - Branded header (Mountain Path logo)
   - Navigation menu (6 pages)
   - Author credentials card
   - Features status
   - Footer with version
   ↓
7. Render MAIN HEADER:
   - Gradient background
   - Application title
   - Author info
   ↓
8. Route to selected page:
   - Dashboard / Data Ingestion / Validation / DCF Analysis / Sensitivity / Settings
   ↓
9. Render FOOTER:
   - Three-column info grid
   - Copyright and status badges
   ↓
10. App ready for interaction
```

---

## 🎨 DESIGN SYSTEM

### Colors Used:
- **dark_blue**: #003366 (Primary)
- **light_blue**: #ADD8E6 (Accent)
- **gold**: #FFD700 (Highlight)
- **light_gray**: #E8E8E8 (Divider)

### Typography:
- **Headings**: 36px, bold, uppercase
- **Labels**: 12-14px, uppercase, letter-spaced
- **Body**: 11-13px, regular
- **Captions**: 10-11px, light

### Layout:
- **Sidebar**: Fixed width, dark blue header
- **Main**: Full width, gradient header/footer
- **Pages**: Routed dynamically based on selection

---

## 🔧 KEY FEATURES

✅ **Professional Branding**
- Mountain Path logo and name
- Author credentials displayed
- Institutional color scheme
- Complete visual hierarchy

✅ **Multi-Page Navigation**
- 6 different pages
- Easy sidebar selection
- Smooth page transitions
- Active page indication

✅ **Database Integration**
- Automatic database initialization
- Cached initialization (performance)
- Session state persistence
- Company/period selection storage

✅ **Professional UI**
- Gradient headers and footers
- Styled cards and sections
- Responsive layout
- Shadow effects and borders

---

## 📝 CUSTOMIZATION GUIDE

### Change Application Name:
```python
# In config.py, modify BRANDING dictionary:
"name": "Your New Name"
```

### Change Colors:
```python
# In config.py, modify COLORS dictionary:
"dark_blue": "#003366"
"light_blue": "#ADD8E6"
"gold": "#FFD700"
```

### Add New Page:
```python
# 1. Create new page file: pages/07_mypage.py
# 2. Add to pages dict in app.py (line 88):
"📄 My Page": "pages/07_mypage.py"
# 3. Add routing (line 234):
elif page == "📄 My Page":
    import pages.mypage as mypage
    mypage.render()
```

### Change Sidebar Width:
```python
# Modify sidebar HTML in line 52-70
# Adjust padding, font-size, margins
```

---

## 🚀 HOW TO RUN

```bash
# Navigate to project root
cd dcf-valuation-platform

# Run the app
streamlit run streamlit_app/app.py

# App will open at http://localhost:8501
```

---

## 📌 IMPORTANT NOTES

1. **Session State**: Variables persist across page reloads, allowing multi-page workflows
2. **Database Caching**: `@st.cache_resource` ensures database is initialized only once
3. **Dynamic Routing**: Pages are imported and executed based on user selection
4. **Professional Design**: Color scheme and styling maintained through config files
5. **Responsive**: Full-width layout adapts to screen size

---

## 🎯 SUMMARY

The **app.py** file is the entry point that:
- ✅ Configures page layout and settings
- ✅ Creates professional sidebar with branding
- ✅ Initializes database and session state
- ✅ Routes to selected page
- ✅ Displays professional header and footer
- ✅ Manages multi-page application flow

It's a **master control file** that ties together all components of the DCF valuation platform.

---

**Status**: Production Ready ✅
**Lines**: 299
**Imports**: 6 modules
**Functions**: 1 (init_database)
**Quality**: Professional Grade

Prof. V. Ravichandran | The Mountain Path - World of Finance | January 2026
