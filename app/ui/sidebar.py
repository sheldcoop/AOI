# app/ui/sidebar.py

import streamlit as st
import pandas as pd

def build_sidebar():
    """
    Builds the sidebar interface for the Streamlit app.
    Handles the file upload and displays summary statistics.

    Returns:
        The uploaded file object if a file is uploaded, otherwise None.
    """
    st.sidebar.title("Defect-Viz Control Panel")
    st.sidebar.markdown("---")

    # --- File Uploader ---
    st.sidebar.header("1. Upload Data")
    uploaded_file = st.sidebar.file_uploader(
        "Select your Defect Excel File (.xlsx)",
        type=["xlsx"]
    )

    st.sidebar.markdown("---")
    return uploaded_file

def display_summary_stats(df: pd.DataFrame):
    """
    Displays summary statistics of the loaded defect data in the sidebar.

    Args:
        df: The cleaned pandas DataFrame containing defect data.
    """
    st.sidebar.header("2. Data Summary")

    # --- Key Metrics ---
    total_defects = len(df)
    unique_defect_types = df["DEFECT_TYPE"].nunique()
    
    # Calculate panel dimensions
    max_row_idx = df["UNIT_INDEX_X"].max()
    max_col_idx = df["UNIT_INDEX_Y"].max()
    panel_dims = f"{max_row_idx + 1} rows x {max_col_idx + 1} columns"

    st.sidebar.metric(label="Total Defects Found", value=total_defects)
    st.sidebar.metric(label="Panel Dimensions", value=panel_dims)
    st.sidebar.metric(label="Unique Defect Types", value=unique_defect_types)

    # --- Defect Type Distribution ---
    st.sidebar.subheader("Defect Distribution")
    defect_counts = df["DEFECT_TYPE"].value_counts()
    st.sidebar.dataframe(defect_counts)
