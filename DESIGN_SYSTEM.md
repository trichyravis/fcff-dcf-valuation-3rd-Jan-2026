"""
DESIGN SYSTEM & STYLING GUIDE
The Mountain Path - World of Finance
Prof. V. Ravichandran - Professional Financial Analysis Platform
"""

# ============================================================================
# COMPREHENSIVE DESIGN SYSTEM
# ============================================================================

## COLOR PALETTE

### Primary Colors
- **Dark Blue**: #003366 (RGB 0, 51, 102)
  - Used for: Headers, sidebars, primary text, emphasis elements
  - Authority and professional credibility
  
- **Light Blue**: #ADD8E6 (RGB 173, 216, 230)
  - Used for: Backgrounds, secondary elements, hover states
  - Balance and clarity
  
- **Gold**: #FFD700 (RGB 255, 215, 0)
  - Used for: Accents, borders, highlights, dividers
  - Excellence and achievement

### Secondary Colors
- **White**: #FFFFFF
  - Card backgrounds, main content area
  
- **Light Gray**: #F5F5F5
  - Page backgrounds, subtle separations
  
- **Dark Gray**: #333333
  - Body text, secondary text
  
- **Success**: #2ECC71
  - Validation passed, positive indicators
  
- **Warning**: #F39C12
  - Cautions, requires attention
  
- **Danger**: #E74C3C
  - Validation failed, errors
  
- **Neutral**: #95A5A6
  - Disabled states, secondary information

---

## TYPOGRAPHY

### Font Family
- **Default**: Arial, sans-serif
  - Professional, readable, universal support
  
- **Monospace**: Courier New, monospace
  - Code, financial values, data display

### Font Sizes
- **h1 (Headings)**: 32px
- **h2 (Page Titles)**: 24px
- **h3 (Section Headers)**: 20px
- **body (Default Text)**: 14px
- **small (Secondary Text)**: 12px
- **caption (Minimal Text)**: 10px

### Font Weights
- **Regular**: 400 (Body text)
- **Semi-Bold**: 600 (Section headers)
- **Bold**: 700 (Page titles, emphasis)

### Line Height
- **Normal**: 1.5 (Reading text)
- **Tight**: 1.2 (Headers)

---

## SPACING SYSTEM

```
xs (Extra Small):    8px   - Small gaps, icon spacing
sm (Small):         12px   - Component padding
md (Medium):        16px   - Standard padding
lg (Large):         24px   - Section spacing
xl (Extra Large):   32px   - Major section breaks
```

---

## COMPONENT STYLING

### SIDEBARS

**Overall Design:**
- Dark blue background gradient
- Professional logo/branding at top
- Clear section headers (uppercase, letter-spaced)
- Navigation with emojis for visual scanning
- Author card with gradient background
- Footer with version and copyright

**Structure:**
```
┌─────────────────────────────────┐
│  THE MOUNTAIN PATH              │
│  WORLD OF FINANCE               │
│  [Logo Emoji]                   │
└─────────────────────────────────┘
┌─────────────────────────────────┐
│ 📍 NAVIGATION                   │
│ • 🏠 Dashboard                  │
│ • 📥 Data Ingestion             │
│ • ✓ Data Validation             │
│ • 📊 DCF Analysis               │
│ • 🔍 Sensitivity                │
│ • ⚙️ Settings                   │
└─────────────────────────────────┘
┌─────────────────────────────────┐
│ 👤 PROFESSIONAL                 │
│                                 │
│ Prof. V. Ravichandran           │
│ 28+ Years Corporate Finance     │
│ 10+ Years Academic Excellence   │
└─────────────────────────────────┘
┌─────────────────────────────────┐
│ ⚡ FEATURES                     │
│ ✓ Enabled — Feature One         │
│ ✓ Enabled — Feature Two         │
│ ✗ Disabled — Feature Three      │
└─────────────────────────────────┘
┌─────────────────────────────────┐
│ Version 1.0 Production Ready    │
│ © 2026 Mountain Path Finance    │
└─────────────────────────────────┘
```

### HEADERS

**Main Application Header:**
- Gradient background (Dark Blue → Gold)
- Large bold title with emoji
- Subtitle text
- Right-aligned author credentials
- Professional spacing and shadow

**Page Headers:**
- Gradient background (Dark Blue → Light Blue)
- Page title (h2 size)
- Left border accent (Gold)
- Icon indicating page purpose
- Clean, professional appearance

**Example Page Header:**
```
📊 VALUATION ANALYSIS
DCF Analysis
[Left border: Gold accent]
```

### FOOTERS

**Main Application Footer:**
- Grid layout (3 columns)
- Application info, Creator info, Version info
- Centered, professional typography
- Border-top divider
- Copyright and credentials
- Bottom border accent (Light Blue)

**Per-Page Footer:**
- Simplified footer on each page
- Platform name + Page name
- Author attribution
- Copyright year
- Consistent styling across pages

### METRIC CARDS

**Design:**
- White background
- Left border (4px, colored by type)
- Rounded corners (8px)
- Box shadow (subtle)
- Centered content

**Color Types:**
- **success** (Green border): Positive indicators
- **warning** (Orange border): Cautions
- **danger** (Red border): Failures
- **info/default** (Dark Blue border): Information

**Content Layout:**
```
┌─────────────────────────┐
│ LABEL (uppercase)       │
│ VALUE (large, bold)     │
│ [Optional delta %]      │
└─────────────────────────┘
```

### ALERTS

**Design:**
- Colored left border (4px)
- Background color matching alert type
- Rounded corners
- Icon prefix
- Clear, readable message

**Types:**
- **Success** (Green): Green border, light green background
- **Warning** (Orange): Orange border, light orange background
- **Danger** (Red): Red border, light red background
- **Info** (Blue): Blue border, light blue background

---

## LAYOUT PATTERNS

### Page Structure
```
┌─────────────────────────────────────────────┐
│  SIDEBAR                  MAIN CONTENT      │
│                                             │
│  [Logo]                 [MAIN HEADER]       │
│  [Nav]                  [Page Content]      │
│  [Author]               [Sections]          │
│  [Features]             [Components]        │
│  [Footer]               [MAIN FOOTER]       │
└─────────────────────────────────────────────┘
```

### Section Styling
```
SECTION TITLE
[h3 header with uppercase label]

Content arranged in:
- Single column (default)
- Two columns (for comparisons)
- Three columns (for metrics)
- Responsive to screen size
```

### Card Grid
```
Card 1    Card 2    Card 3
[m-b]     [m-b]     [m-b]

Card 4    Card 5    Card 6
[m-b]     [m-b]     [m-b]
```

---

## INTERACTIVE ELEMENTS

### Buttons
**Primary (Type: "primary")**
- Dark blue background
- White text
- Rounded corners (8px)
- Hover: Light blue background, dark blue text
- Shadow on hover

**Secondary (Default)**
- Light background
- Dark text
- Outline style
- Hover: Darker background

**Width Options:**
- `use_container_width=True`: Full width
- Default: Natural width

### Input Elements
**Text Inputs**
- Border: Light blue on focus
- Padding: Standard (md)
- Rounded corners

**Sliders**
- Primary color: Dark blue
- Range: Min to Max clearly marked
- Percentage or custom format

**Selectboxes & Radios**
- Standard Streamlit styling
- Dark blue accents
- Clear labels and help text

### Tables
**Header Row**
- Dark blue background
- White text
- Semi-bold font weight
- Standard padding

**Data Rows**
- White background
- Alternating light gray on hover
- Left-aligned text
- Standard padding

**Borders**
- Collapse style
- Bottom borders between rows
- Clean, minimal appearance

---

## NAVIGATION PATTERNS

### Sidebar Navigation
- Icon + Label format
- Full width selection
- Clear active state indication
- Organized into logical sections

### Breadcrumb Style
- Used at top of pages
- Format: "Home > Section > Page"
- Optional, shown when nested

### Tabs
- Use Streamlit's native st.tabs()
- Related content grouped together
- One tab active at a time
- Clear visual indication of active tab

---

## CONSISTENCY GUIDELINES

### Always Use
- Consistent color palette (5 main colors)
- Standard spacing (8px base unit)
- Professional typography (Arial, 14px body)
- Dark blue for primary actions
- Gold for accents and highlights
- Left-aligned text (except headers)

### Avoid
- Extra fonts (stick to Arial + Courier)
- Inconsistent spacing
- Dark blue and gold overuse
- Multiple emphasis techniques
- Clashing color combinations

### Responsive Design
- Single column on mobile
- 2-3 columns on tablet/desktop
- Use Streamlit's `st.columns()` for layout
- Avoid fixed pixel widths

---

## ACCESSIBILITY

### Color Contrast
- Text on backgrounds: >= 4.5:1 contrast ratio
- Dark gray on white: ✓ High contrast
- Dark blue on light blue: ✓ Sufficient
- All text readable on all backgrounds

### Font Sizes
- Minimum 12px for readable body text
- Headings clear and distinct
- Enough spacing between lines

### Interactive Elements
- Buttons clearly identifiable
- Hover states visible
- Form labels descriptive
- Error messages clear

---

## PRACTICAL EXAMPLES

### Example 1: Dashboard Card
```
┌──────────────────────────────────┐
│ ● Company Count                  │
│                                  │
│                45                │
│                                  │
│ [← left border: dark blue]       │
└──────────────────────────────────┘
```

### Example 2: Page Header
```
[Dark Blue → Light Blue gradient]
📊 Valuation Analysis
DCF Analysis
[Gold left border accent]
```

### Example 3: Navigation Item
```
🏠 Dashboard
[Full width, responsive]
[Dark blue when active, light when inactive]
```

### Example 4: Alert Message
```
┌──────────────────────────────────┐
│ ✓ Successfully loaded 10-K data  │
│ [Green left border]              │
│ [Light green background]         │
└──────────────────────────────────┘
```

---

## CSS CLASSES & STYLING

### Main Classes (from styles.py)
- `.metric-card` — Metric display cards
- `.metric-card.success` — Success variant
- `.metric-card.warning` — Warning variant
- `.metric-card.danger` — Error variant
- `.chart-container` — Chart wrappers
- `.form-container` — Form sections
- `.alert` — Alert messages
- `.streamlit-table` — Data tables

### Component Styling (components.py)
- `ComponentLibrary.hero_header()` — Main header
- `ComponentLibrary.metric_card()` — Metric cards
- `ComponentLibrary.alert()` — Alerts
- `ComponentLibrary.financial_table()` — Tables
- `ComponentLibrary.form_section()` — Form groups

---

## IMPLEMENTATION CHECKLIST

When creating new pages or components:

✓ Use consistent color palette
✓ Apply proper spacing (8px base unit)
✓ Include professional header (gradient + title)
✓ Use appropriate metric cards for data
✓ Add footer with branding
✓ Implement alerts for user feedback
✓ Use dark blue for primary actions
✓ Add gold accents for emphasis
✓ Ensure responsive layout
✓ Test on different screen sizes
✓ Verify accessibility (contrast, size)
✓ Match sidebar navigation style
✓ Use consistent typography
✓ Follow button styling guide
✓ Include appropriate comments

---

## MAINTENANCE

### Adding New Pages
1. Create `pages/XX_new_page.py`
2. Include professional header (copy template)
3. Add page footer (copy template)
4. Use ComponentLibrary for consistency
5. Import COLORS from config.py
6. Test styling on different screens

### Updating Design
1. Update COLORS dict in config.py
2. Update CSS in styles.py
3. Update component templates in components.py
4. Test all pages
5. Document changes

### Consistent Updates
- All headers follow same gradient pattern
- All footers follow same layout
- All sidebars follow same structure
- All alerts follow same styling
- All cards follow same design

---

## DESIGN PHILOSOPHY

**Professional Financial Application**

The design system reflects institutional-grade financial software:
- Authority through dark blue
- Excellence through gold accents
- Clarity through professional typography
- Trustworthiness through consistent styling
- Accessibility through proper contrast and sizing

**Not Trendy, Not Cluttered**

- Timeless color palette
- Minimal decoration
- Focus on content
- Clear information hierarchy
- Professional aesthetic

**Branding Integration**

- "The Mountain Path" prominently displayed
- Prof. V. Ravichandran attribution throughout
- "World of Finance" tagline visible
- Consistent logo placement
- Professional credentials visible

---

**Design System Version**: 1.0  
**Last Updated**: January 2026  
**Created by**: Prof. V. Ravichandran  
**Status**: Production Ready
