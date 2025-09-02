# app/core/data_loader.py

import pandas as pd
import numpy as np
import streamlit as st
# Import only the non-geometric configurations
from app.config import COLUMN_NAMES

# Use Streamlit's cache to avoid reprocessing the same file.
# Note: The function will now re-run if panel_size or gap_size changes.
@st.cache_data
def load_and_transform_data(uploaded_file, panel_size: int, gap_size: int):
    """
    Loads data from the uploaded Excel file, cleans it, and transforms it for a 2x2 grid plot.

    Args:
        uploaded_file: The file-like object from a Streamlit upload.
        panel_size (int): The size of one square panel.
        gap_size (int): The size of the gap between panels.

    Returns:
        A cleaned and transformed pandas DataFrame ready for plotting, or None if an error occurs.
    """
    try:
        # Step 1: Read the Data using column names from the config
        df = pd.read_excel(
            uploaded_file,
            engine='openpyxl',
            header=None,
            skiprows=1,
            names=COLUMN_NAMES,
            usecols=f"A:{chr(ord('A') + len(COLUMN_NAMES) - 1)}" # Dynamically set column range
        )

        # Step 2: Clean the Data
        df['DEFECT_TYPE'] = df['DEFECT_TYPE'].str.strip()
        df.dropna(subset=['DEFECT_ID', 'UNIT_INDEX_X', 'UNIT_INDEX_Y'], inplace=True)
        
        # Ensure correct data types
        for col in ['DEFECT_ID', 'UNIT_INDEX_X', 'UNIT_INDEX_Y']:
            df[col] = df[col].astype(int)

        # Step 3: Transform Coordinates for 2x2 Gapped Plot using passed arguments
        # Calculate the base position within a panel
        plot_x_base = df['UNIT_INDEX_Y'] % panel_size
        plot_y_base = df['UNIT_INDEX_X'] % panel_size
        
        # Add an offset if the defect is in the top or right set of panels
        x_offset = np.where(df['UNIT_INDEX_Y'] >= panel_size, panel_size + gap_size, 0)
        y_offset = np.where(df['UNIT_INDEX_X'] >= panel_size, panel_size + gap_size, 0)
        
        # Final plot coordinates include base, offset, and random jitter for visualization
        df['plot_x'] = plot_x_base + x_offset + np.random.rand(len(df))
        df['plot_y'] = plot_y_base + y_offset + np.random.rand(len(df))

        return df

    except Exception as e:
        st.error(f"Failed to process the Excel file. Please ensure it has the correct format.")
        st.error(f"Error details: {e}")
        return None
