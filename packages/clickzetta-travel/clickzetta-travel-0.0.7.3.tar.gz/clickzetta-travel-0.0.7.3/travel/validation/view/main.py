import streamlit as st

st.set_page_config(
    page_title="Realtime Data Validation for XSY",
    layout="wide",
)

st.markdown(
    """
    ### Clickzetta real-time data validation tool.


    - XSY Validation Result Overview: XSY source table and destination table IDS validation overview.
    - XSY Schema Validation Result Overview: XSY source table and destination table schema check overview.
    - XSY Full Table Check: Check source table and destination table data line by line, and provide diagnosis logic.

"""
)