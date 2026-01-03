import streamlit as st

def render():
    st.title("📥 Data Ingestion")
    st.write("Load company data from SEC EDGAR")
    st.text_input("Company Ticker")
    if st.button("Load Data"):
        st.success("Data loaded")
