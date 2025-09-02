# app/core/data_loader.py

import pandas as pd
from typing import Optional
import streamlit as st

@st.cache_data
def load_and_clean_data(uploaded_file) -> Optional[pd.DataFrame]:
    """
    Loads data from the uploaded Excel file using the second row as the header.
    """
    try:
        # --- THE NEW, SIMPLER LOGIC ---
        # header=1 tells pandas to use the SECOND row (index 1) as the column names.
        df_raw = pd.read_excel(uploaded_file, header=1)

        # --- Data Cleaning ---
        # Drop rows where DEFECT_ID is not a valid number
        df_raw.dropna(subset=['DEFECT_ID'], inplace=True)

        # Fill any missing essential numeric values with 0
        fill_zero_cols = ["UNIT_INDEX_X", "UNIT_INDEX_Y", "X_COORDINATES", "Y_COORDINATES"]
        for col in fill_zero_cols:
            if col in df_raw.columns:
                df_raw[col].fillna(0, inplace=True)

        # Convert types safely
        df_raw["DEFECT_ID"] = df_raw["DEFECT_ID"].astype(int)
        df_raw["UNIT_INDEX_X"] = df_raw["UNIT_INDEX_X"].astype(int)
        df_raw["UNIT_INDEX_Y"] = df_raw["UNIT_INDEX_Y"].astype(int)

        # Select only the columns we need, in case there are extra ones
        final_cols = ["DEFECT_ID", "DEFECT_TYPE", "X_COORDINATES", 
                      "Y_COORDINATES", "UNIT_INDEX_X", "UNIT_INDEX_Y"]
        df = df_raw[final_cols].copy()
        
        return df

    except Exception as e:
        st.error(f"Error processing Excel data: {e}")
        return None
