"""
DCF Valuation Platform - Root Entry Point
The Mountain Path - World of Finance
Routes to streamlit_app/app.py for Streamlit Cloud

This file is required by Streamlit Cloud as the main entry point.
It imports and runs the actual application from streamlit_app/app.py
"""

# This tells Streamlit Cloud where the app is
import sys
from pathlib import Path

# Import everything from streamlit_app.app
from streamlit_app.app import *
