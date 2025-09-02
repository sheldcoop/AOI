# app/core/data_loader.py

import pandas as pd
from typing import Optional
import streamlit as st

# We no longer need to import column names from config, we will find them.

@st.cache_data
def load_and_clean_data(uploaded_file) -> Optional[pd.DataFrame]:
    """
    Loads data from the uploaded Excel file, intelligently finds the correct columns,
    cleans the data, and prepares it for visualization.
    """
    try:
        # Read the Excel file, skipping the red-titled first row.
        # Let pandas figure out the columns for now.
        df_raw = pd.read_excel(uploaded_file, header=None, skiprows=1)

        # --- Data Cleaning and Column Identification ---
        
        # The first column should contain the defect ID and type together.
        # Let's split it. Example: "1 Short" -> "1" and "Short"
        df_raw['DEFECT_ID'] = df_raw[0].astype(str).str.split().str[0]
        df_raw['DEFECT_TYPE'] = df_raw[0].astype(str).str.split().str[1:].str.join(' ')

        # Now, assign the other columns based on their position.
        # This matches your original file structure screenshot.
        df_raw.rename(columns={
            1: 'X_COORDINATES',
            2: 'Y_COORDINATES',
            3: 'UNIT_INDEX_X',
            4: 'UNIT_INDEX_Y'
        }, inplace=True)
        
        # Select only the columns we need
        df = df_raw[['DEFECT_ID', 'DEFECT_TYPE', 'X_COORDINATES', 'Y_COORDINATES', 'UNIT_INDEX_X', 'UNIT_INDEX_Y']].copy()

        # Convert DEFECT_ID to numeric, coercing errors to NaN
        df['DEFECT_ID'] = pd.to_numeric(df['DEFECT_ID'], errors='coerce')

        # Drop any rows where the DEFECT_ID could not be converted to a number.
        df.dropna(subset=['DEFECT_ID'], inplace=True)
        
        # Fill any missing essential numeric values with 0.
        fill_zero_cols = ["UNIT_INDEX_X", "UNIT_INDEX_Y", "X_COORDINATES", "Y_COORDINATES"]
        for col in fill_zero_cols:
            df[col].fillna(0, inplace=True)

        # Safely convert data types to integers now that data is clean.
        df["DEFECT_ID"] = df["DEFECT_ID"].astype(int)
        df["UNIT_INDEX_X"] = df["UNIT_INDEX_X"].astype(int)
        df["UNIT_INDEX_Y"] = df["UNIT_INDEX_Y"].astype(int)
        
        return df

    except Exception as e:
        st.error(f"Error processing Excel data: {e}")
        return None
