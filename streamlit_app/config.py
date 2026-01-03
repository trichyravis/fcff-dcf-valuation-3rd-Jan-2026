"""
Streamlit Configuration & Design System
The Mountain Path - World of Finance
Colors, fonts, and styling constants for consistent branding
"""

# Color Palette - Professional Financial Theme
COLORS = {
    "dark_blue": "#003366",      # RGB(0, 51, 102)
    "light_blue": "#ADD8E6",     # RGB(173, 216, 230)
    "gold": "#FFD700",           # RGB(255, 215, 0)
    "white": "#FFFFFF",
    "light_gray": "#F5F5F5",
    "dark_gray": "#333333",
    "success": "#2ECC71",
    "warning": "#F39C12",
    "danger": "#E74C3C",
    "neutral": "#95A5A6"
}

# Typography
FONTS = {
    "default": "Arial, sans-serif",
    "monospace": "Courier New, monospace"
}

# Sidebar Configuration
SIDEBAR = {
    "width": 250,
    "padding": 20
}

# Component Dimensions
DIMENSIONS = {
    "card_height": 120,
    "metric_width": 220,
    "border_radius": 8,
    "box_shadow": "0 2px 8px rgba(0, 0, 0, 0.1)"
}

# Spacing
SPACING = {
    "xs": 8,
    "sm": 12,
    "md": 16,
    "lg": 24,
    "xl": 32
}

# Text Styles
TEXT_SIZES = {
    "h1": 32,
    "h2": 24,
    "h3": 20,
    "body": 14,
    "small": 12,
    "caption": 10
}

# Financial Formatting
CURRENCY_SYMBOL = "$"
DECIMAL_PLACES = 2
THOUSANDS_SEPARATOR = ","

# Chart Configuration
CHART_CONFIG = {
    "theme": "streamlit",
    "colors": [COLORS["dark_blue"], COLORS["gold"], COLORS["light_blue"]],
    "use_container_width": True,
    "margin": {"t": 20, "r": 20, "b": 20, "l": 20}
}

# Application Branding
BRANDING = {
    "name": "The Mountain Path - DCF Valuation",
    "subtitle": "Professional Financial Analysis Platform",
    "author": "Prof. V. Ravichandran",
    "byline": "28+ Years Corporate Finance & Banking Experience\n10+ Years Academic Excellence",
    "logo_emoji": "⛰️"
}

# Feature Flags
FEATURES = {
    "enable_dark_mode": False,
    "enable_export": True,
    "enable_comparison": True,
    "enable_sensitivity_analysis": True
}

# Default Values
DEFAULTS = {
    "wacc": 0.08,
    "terminal_growth_rate": 0.025,
    "projection_years": 5,
    "tax_rate": 0.25
}

# Data Validation Rules
VALIDATION = {
    "max_wacc": 0.25,
    "min_wacc": 0.01,
    "max_terminal_gr": 0.05,
    "min_terminal_gr": 0.0,
    "max_shares": 10_000_000_000,
    "min_shares": 1
}
