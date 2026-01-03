"""
Streamlit CSS Styling System
Custom styles for financial dashboard components
Prof. V. Ravichandran - The Mountain Path - World of Finance
"""

from streamlit_app.config import COLORS, SPACING, DIMENSIONS, TEXT_SIZES

def get_base_css():
    """Base CSS styling for all pages"""
    return f"""
    <style>
        /* General Styling */
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: {COLORS['dark_gray']};
            background-color: {COLORS['light_gray']};
        }}
        
        /* Page Container */
        .main {{
            padding: {SPACING['lg']}px;
        }}
        
        /* Typography */
        h1 {{
            color: {COLORS['dark_blue']};
            font-size: {TEXT_SIZES['h1']}px;
            font-weight: 700;
            margin-bottom: {SPACING['lg']}px;
            border-bottom: 3px solid {COLORS['gold']};
            padding-bottom: {SPACING['sm']}px;
        }}
        
        h2 {{
            color: {COLORS['dark_blue']};
            font-size: {TEXT_SIZES['h2']}px;
            font-weight: 600;
            margin-top: {SPACING['lg']}px;
            margin-bottom: {SPACING['md']}px;
        }}
        
        h3 {{
            color: {COLORS['dark_blue']};
            font-size: {TEXT_SIZES['h3']}px;
            font-weight: 600;
            margin-top: {SPACING['md']}px;
            margin-bottom: {SPACING['sm']}px;
        }}
        
        /* Cards and Containers */
        .metric-card {{
            background-color: {COLORS['white']};
            border-left: 4px solid {COLORS['dark_blue']};
            border-radius: {DIMENSIONS['border_radius']}px;
            padding: {SPACING['md']}px;
            margin-bottom: {SPACING['md']}px;
            box-shadow: {DIMENSIONS['box_shadow']};
            min-height: {DIMENSIONS['card_height']}px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        
        .metric-card.success {{
            border-left-color: {COLORS['success']};
        }}
        
        .metric-card.warning {{
            border-left-color: {COLORS['warning']};
        }}
        
        .metric-card.danger {{
            border-left-color: {COLORS['danger']};
        }}
        
        /* Metric Values */
        .metric-value {{
            font-size: {TEXT_SIZES['h2']}px;
            font-weight: 700;
            color: {COLORS['dark_blue']};
            margin: {SPACING['sm']}px 0;
        }}
        
        .metric-label {{
            font-size: {TEXT_SIZES['body']}px;
            color: {COLORS['neutral']};
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        /* Buttons */
        .stButton > button {{
            background-color: {COLORS['dark_blue']};
            color: {COLORS['white']};
            border: none;
            border-radius: {DIMENSIONS['border_radius']}px;
            padding: {SPACING['sm']}px {SPACING['md']}px;
            font-size: {TEXT_SIZES['body']}px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            background-color: {COLORS['light_blue']};
            color: {COLORS['dark_blue']};
            box-shadow: {DIMENSIONS['box_shadow']};
        }}
        
        /* Input Elements */
        .stNumberInput, .stSelectbox, .stSlider {{
            margin-bottom: {SPACING['md']}px;
        }}
        
        /* Tables */
        .streamlit-table {{
            border-collapse: collapse;
            width: 100%;
        }}
        
        .streamlit-table th {{
            background-color: {COLORS['dark_blue']};
            color: {COLORS['white']};
            padding: {SPACING['sm']}px;
            text-align: left;
            font-weight: 600;
        }}
        
        .streamlit-table td {{
            border-bottom: 1px solid {COLORS['light_gray']};
            padding: {SPACING['sm']}px;
        }}
        
        .streamlit-table tr:hover {{
            background-color: {COLORS['light_gray']};
        }}
        
        /* Alerts and Messages */
        .alert {{
            padding: {SPACING['md']}px;
            border-radius: {DIMENSIONS['border_radius']}px;
            margin-bottom: {SPACING['md']}px;
        }}
        
        .alert-success {{
            background-color: #E8F8F5;
            border-left: 4px solid {COLORS['success']};
        }}
        
        .alert-warning {{
            background-color: #FCF3CF;
            border-left: 4px solid {COLORS['warning']};
        }}
        
        .alert-danger {{
            background-color: #FADBD8;
            border-left: 4px solid {COLORS['danger']};
        }}
        
        /* Sidebar */
        .sidebar {{
            background-color: {COLORS['dark_blue']};
            color: {COLORS['white']};
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding-top: {SPACING['lg']}px;
            margin-top: {SPACING['xl']}px;
            border-top: 1px solid {COLORS['light_gray']};
            color: {COLORS['neutral']};
            font-size: {TEXT_SIZES['small']}px;
        }}
        
        /* Validation Messages */
        .validation-error {{
            color: {COLORS['danger']};
            font-weight: 600;
            margin-top: {SPACING['sm']}px;
        }}
        
        .validation-success {{
            color: {COLORS['success']};
            font-weight: 600;
            margin-top: {SPACING['sm']}px;
        }}
    </style>
    """

def get_metric_css(metric_type: str = "default"):
    """Get CSS for specific metric card type"""
    type_colors = {
        "success": COLORS["success"],
        "warning": COLORS["warning"],
        "danger": COLORS["danger"],
        "info": COLORS["dark_blue"],
        "default": COLORS["dark_blue"]
    }
    
    border_color = type_colors.get(metric_type, type_colors["default"])
    
    return f"""
    <style>
        .metric-{metric_type} {{
            border-left: 4px solid {border_color};
        }}
    </style>
    """

def get_chart_css():
    """CSS for chart containers"""
    return f"""
    <style>
        .chart-container {{
            background-color: {COLORS['white']};
            border-radius: {DIMENSIONS['border_radius']}px;
            padding: {SPACING['md']}px;
            margin-bottom: {SPACING['lg']}px;
            box-shadow: {DIMENSIONS['box_shadow']};
        }}
        
        .chart-title {{
            color: {COLORS['dark_blue']};
            font-size: {TEXT_SIZES['h3']}px;
            font-weight: 600;
            margin-bottom: {SPACING['md']}px;
        }}
    </style>
    """

def get_form_css():
    """CSS for form elements"""
    return f"""
    <style>
        .form-container {{
            background-color: {COLORS['white']};
            border-radius: {DIMENSIONS['border_radius']}px;
            padding: {SPACING['lg']}px;
            margin-bottom: {SPACING['lg']}px;
            box-shadow: {DIMENSIONS['box_shadow']};
        }}
        
        .form-section {{
            margin-bottom: {SPACING['lg']}px;
        }}
        
        .form-label {{
            color: {COLORS['dark_blue']};
            font-weight: 600;
            margin-bottom: {SPACING['sm']}px;
            display: block;
        }}
        
        .form-description {{
            color: {COLORS['neutral']};
            font-size: {TEXT_SIZES['small']}px;
            margin-top: {SPACING['xs']}px;
        }}
    </style>
    """

def apply_styles(streamlit):
    """Apply all CSS styles to Streamlit app"""
    streamlit.markdown(get_base_css(), unsafe_allow_html=True)
    streamlit.markdown(get_chart_css(), unsafe_allow_html=True)
    streamlit.markdown(get_form_css(), unsafe_allow_html=True)
