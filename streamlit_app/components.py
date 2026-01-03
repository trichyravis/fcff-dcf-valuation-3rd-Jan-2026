"""
Reusable Streamlit Components
Financial dashboard components for consistent UI/UX
Prof. V. Ravichandran - The Mountain Path - World of Finance
"""

import streamlit as st
from streamlit_app.config import COLORS, SPACING, TEXT_SIZES
import pandas as pd
from typing import Dict, List, Optional, Any


class ComponentLibrary:
    """Collection of reusable UI components"""
    
    @staticmethod
    def hero_header(title: str, subtitle: str = "", emoji: str = ""):
        """
        Create a prominent hero header section
        """
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if emoji:
                st.markdown(f"<h1 style='font-size: 48px; margin: 0;'>{emoji}</h1>", 
                           unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
            if subtitle:
                st.markdown(f"<p style='color: #666; margin-top: -10px;'>{subtitle}</p>", 
                           unsafe_allow_html=True)
        
        st.divider()
    
    @staticmethod
    def metric_card(label: str, value: Any, unit: str = "", 
                   card_type: str = "default", delta: Optional[float] = None):
        """
        Display a metric card with value
        
        Args:
            label: Metric label
            value: Metric value
            unit: Unit of measurement
            card_type: 'default', 'success', 'warning', 'danger'
            delta: Optional percentage change
        """
        # Format value
        if isinstance(value, (int, float)):
            if unit == "$":
                formatted_value = f"${value:,.2f}" if isinstance(value, float) else f"${value:,}"
            elif unit == "%":
                formatted_value = f"{value:.2f}%"
            else:
                formatted_value = f"{value:,.2f}"
        else:
            formatted_value = str(value)
        
        # Color selection
        color_map = {
            "default": COLORS["dark_blue"],
            "success": COLORS["success"],
            "warning": COLORS["warning"],
            "danger": COLORS["danger"]
        }
        border_color = color_map.get(card_type, COLORS["dark_blue"])
        
        # Build HTML card
        delta_html = ""
        if delta is not None:
            delta_symbol = "↑" if delta > 0 else "↓"
            delta_color = COLORS["success"] if delta > 0 else COLORS["danger"]
            delta_html = f"<div style='color: {delta_color}; font-size: 12px; margin-top: 8px;'>{delta_symbol} {abs(delta):.2f}%</div>"
        
        card_html = f"""
        <div style='
            background-color: white;
            border-left: 4px solid {border_color};
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        '>
            <div style='color: #666; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;'>
                {label}
            </div>
            <div style='color: {border_color}; font-size: 28px; font-weight: 700;'>
                {formatted_value}
            </div>
            {delta_html}
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)
    
    @staticmethod
    def metrics_row(metrics: List[Dict]):
        """
        Display multiple metrics in a row
        
        Args:
            metrics: List of dicts with 'label', 'value', 'unit', 'type'
        """
        cols = st.columns(len(metrics))
        
        for col, metric in zip(cols, metrics):
            with col:
                ComponentLibrary.metric_card(
                    label=metric.get("label", ""),
                    value=metric.get("value", 0),
                    unit=metric.get("unit", ""),
                    card_type=metric.get("type", "default"),
                    delta=metric.get("delta")
                )
    
    @staticmethod
    def financial_table(df: pd.DataFrame, format_columns: Optional[Dict] = None):
        """
        Display a formatted financial table
        
        Args:
            df: DataFrame to display
            format_columns: Dict of column_name -> 'currency'|'percent'|'number'
        """
        if format_columns:
            # Apply formatting
            styled_df = df.style
            for col, fmt in format_columns.items():
                if col in df.columns:
                    if fmt == "currency":
                        styled_df = styled_df.format({col: "${:,.2f}"})
                    elif fmt == "percent":
                        styled_df = styled_df.format({col: "{:.2%}"})
                    elif fmt == "number":
                        styled_df = styled_df.format({col: "{:,.0f}"})
            
            st.dataframe(styled_df, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
    
    @staticmethod
    def form_section(title: str, description: str = ""):
        """
        Create a form section with title and optional description
        """
        st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
        if description:
            st.markdown(f"<small style='color: #666;'>{description}</small>", 
                       unsafe_allow_html=True)
        st.divider()
    
    @staticmethod
    def input_group(label: str, description: str = "", 
                   help_text: str = ""):
        """
        Create a labeled input group
        """
        if description:
            st.markdown(f"<p style='margin-bottom: 4px; color: #333;'><strong>{label}</strong></p>", 
                       unsafe_allow_html=True)
            st.markdown(f"<small style='color: #666;'>{description}</small>", 
                       unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='margin-bottom: 4px;'><strong>{label}</strong></p>", 
                       unsafe_allow_html=True)
    
    @staticmethod
    def alert(message: str, alert_type: str = "info", dismissible: bool = False):
        """
        Display an alert message
        
        Args:
            message: Alert message
            alert_type: 'success', 'warning', 'danger', 'info'
            dismissible: Whether alert can be dismissed
        """
        icon_map = {
            "success": "✓",
            "warning": "⚠",
            "danger": "✕",
            "info": "ℹ"
        }
        
        color_map = {
            "success": COLORS["success"],
            "warning": COLORS["warning"],
            "danger": COLORS["danger"],
            "info": COLORS["dark_blue"]
        }
        
        bg_color_map = {
            "success": "#E8F8F5",
            "warning": "#FCF3CF",
            "danger": "#FADBD8",
            "info": "#E8F4F8"
        }
        
        icon = icon_map.get(alert_type, "ℹ")
        border_color = color_map.get(alert_type, COLORS["dark_blue"])
        bg_color = bg_color_map.get(alert_type, "#E8F4F8")
        
        alert_html = f"""
        <div style='
            background-color: {bg_color};
            border-left: 4px solid {border_color};
            border-radius: 4px;
            padding: 12px 16px;
            margin-bottom: 12px;
        '>
            <span style='color: {border_color}; font-weight: 600; margin-right: 8px;'>{icon}</span>
            <span>{message}</span>
        </div>
        """
        
        st.markdown(alert_html, unsafe_allow_html=True)
    
    @staticmethod
    def page_header(page_name: str, breadcrumbs: List[str] = None):
        """
        Create page header with breadcrumbs
        """
        breadcrumb_text = " > ".join(breadcrumbs) if breadcrumbs else ""
        
        if breadcrumb_text:
            st.markdown(f"<small style='color: #666;'>{breadcrumb_text}</small>", 
                       unsafe_allow_html=True)
        
        st.markdown(f"<h2>{page_name}</h2>", unsafe_allow_html=True)
    
    @staticmethod
    def footer(content: str):
        """
        Display footer content
        """
        footer_html = f"""
        <div style='
            text-align: center;
            padding-top: 32px;
            margin-top: 32px;
            border-top: 1px solid #E0E0E0;
            color: #999;
            font-size: 12px;
        '>
            {content}
        </div>
        """
        st.markdown(footer_html, unsafe_allow_html=True)
    
    @staticmethod
    def tabs_container(tab_names: List[str]):
        """
        Create a tabs container
        
        Returns:
            Tuple of tab objects from st.tabs()
        """
        return st.tabs(tab_names)
    
    @staticmethod
    def comparison_metrics(title: str, metrics: List[Dict]):
        """
        Display metrics with comparison values
        
        Args:
            title: Section title
            metrics: List of dicts with label, current, previous, unit
        """
        st.subheader(title)
        
        cols = st.columns(len(metrics))
        
        for col, metric in zip(cols, metrics):
            with col:
                label = metric.get("label", "")
                current = metric.get("current", 0)
                previous = metric.get("previous", 0)
                unit = metric.get("unit", "")
                
                # Calculate change
                if previous != 0:
                    change = ((current - previous) / abs(previous)) * 100
                else:
                    change = 0
                
                st.metric(
                    label=label,
                    value=f"{current:,.0f}" if unit != "$" else f"${current:,.0f}",
                    delta=f"{change:.1f}%"
                )
    
    @staticmethod
    def validation_feedback(valid: bool, message: str):
        """
        Display validation feedback
        """
        if valid:
            ComponentLibrary.alert(message, alert_type="success")
        else:
            ComponentLibrary.alert(message, alert_type="danger")


# Shorthand functions for common components
def metric_card(label: str, value: Any, unit: str = "", card_type: str = "default"):
    """Shorthand for ComponentLibrary.metric_card"""
    ComponentLibrary.metric_card(label, value, unit, card_type)

def alert(message: str, alert_type: str = "info"):
    """Shorthand for ComponentLibrary.alert"""
    ComponentLibrary.alert(message, alert_type)

def hero_header(title: str, subtitle: str = "", emoji: str = ""):
    """Shorthand for ComponentLibrary.hero_header"""
    ComponentLibrary.hero_header(title, subtitle, emoji)
