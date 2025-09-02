# app/core/data_loader.py

import pandas as pd
from typing import Optional
import streamlit as st  # <-- THIS IS THE FIX
from app.utils.config import COLUMN_NAMES, REQUIRED_COLUMNS

# Use Streamlit's cache to avoid re-loading and processing the same file
@st.cache_data
def load_and_clean_data(uploaded_file) -> Optional[pd.DataFrame]:
# ... (the rest of the file is correct) ...
    """
    Loads data from the uploaded Excel file, cleans it, and prepares it for visualization.
    
    Args:
        uploaded_file: The file-like object from a Streamlit upload.
        
    Returns:
        A cleaned pandas DataFrame or None if the file is invalid.
    """
    try:
        # Read the Excel file, skipping the red-titled first row (header=None, skiprows=1).
        # We provide our own column names based on the config.
        df_raw = pd.read_excel(uploaded_file, header=None, skiprows=1, 
                               names=COLUMN_NAMES + ["MODALITY_1_IMG", "MODALITY_2_IMG"])

        # --- Data Cleaning ---
        # 1. Keep only the necessary data columns. The image columns are placeholders.
        df = df_raw[COLUMN_NAMES].copy()

        # 2. Drop any rows where the DEFECT_ID is completely empty. This is our anchor.
        df.dropna(subset=["DEFECT_ID"], inplace=True)
        
        # 3. Fill any missing essential numeric values with 0.
        fill_zero_cols = ["UNIT_INDEX_X", "UNIT_INDEX_Y", "X_COORDINATES", "Y_COORDINATES"]
        for col in fill_zero_cols:
            if col in df.columns:
                df[col].fillna(0, inplace=True)

        # 4. Safely convert data types to integers now that NaNs are handled.
        df["DEFECT_ID"] = df["DEFECT_ID"].astype(int)
        df["UNIT_INDEX_X"] = df["UNIT_INDEX_X"].astype(int)
        df["UNIT_INDEX_Y"] = df["UNIT_INDEX_Y"].astype(int)
        
        return df

    except Exception as e:
        # If any error occurs during loading (e.g., wrong file format), return None.
        st.error(f"Error loading Excel file: {e}")
        return None
