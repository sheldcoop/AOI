# app.py
# DEBUGGING VERSION: To inspect the actual column names from the Excel file.

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excel Column Inspector", layout="wide")
st.title("Excel Header Debugging Tool")

uploaded_file = st.file_uploader("Upload your Excel File to see its column headers", type=["xlsx"])

if uploaded_file is not None:
    st.header("Inspecting File...")
    try:
        # Read the file using the second row as the header
        df = pd.read_excel(uploaded_file, header=1)
        
        st.subheader("1. Raw Column Headers (as read by Pandas)")
        st.write("These are the exact column names found in your file. Note any extra spaces or unexpected characters.")
        st.code(list(df.columns))

        # --- Let's try cleaning them ---
        st.subheader("2. Cleaned Column Headers")
        st.write("This is what the column names look like after our cleaning function.")
        
        cleaned_columns = df.columns.str.strip().str.replace(' ', '_').str.replace(r'[^A-Za-z0-9_]', '', regex=True)
        st.code(list(cleaned_columns))

        # --- Let's see the first few rows of data ---
        st.subheader("3. DataFrame Preview (first 5 rows)")
        st.write("This shows how pandas has interpreted your data.")
        st.dataframe(df.head())

    except Exception as e:
        st.error(f"An error occurred while trying to read the Excel file: {e}")
