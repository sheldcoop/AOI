# app.py
# FINAL DEBUGGING SCRIPT - This will crash and show the real error.

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Debug Mode", layout="wide")
st.title("Excel Data Loading Debugger")

uploaded_file = st.file_uploader("Upload your Excel File to see the full processing error", type=["xlsx"])

if uploaded_file is not None:
    st.info("Attempting to load data... The app WILL crash if an error occurs. Please screenshot the red error box.")

    # NO try...except block. We want to see the raw error.
    
    # We will use the loading strategy that we believe is correct.
    # header=None tells pandas there are no column names in the file.
    # skiprows=1 tells it to skip your red title row.
    df = pd.read_excel(uploaded_file, header=None, skiprows=1)
    
    # If the app gets here, it means the file was read successfully.
    st.success("SUCCESS! The file was read without crashing.")
    st.dataframe(df.head())
