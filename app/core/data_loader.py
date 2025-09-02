# app/core/data_loader.py

import pandas as pd
import numpy as np
import streamlit as st

# Use Streamlit's cache to avoid reprocessing the same file on every interaction.
@st.cache_data
def load_and_transform_data(uploaded_file):
    """
    Loads data from the uploaded Excel file, cleans it, and transforms it for a 2x2 grid plot.

    Args:
        uploaded_file: The file-like object from a Streamlit upload.

    Returns:
        A cleaned and transformed pandas DataFrame ready for plotting, or None if an error occurs.
    """
    COLUMN_NAMES = [
        "DEFECT_ID", "DEFECT_TYPE", "X_COORDINATES", 
        "Y_COORDINATES", "UNIT_INDEX_X", "UNIT_INDEX_Y"
    ]

    try:
        # Step 1: Read the Data
        df = pd.read_excel(
            uploaded_file,
            engine='openpyxl',
            header=None,
            skiprows=1,
            names=COLUMN_NAMES,
            usecols="A:F"
        )

        # Step 2: Clean the Data
        df['DEFECT_TYPE'] = df['DEFECT_TYPE'].str.strip()
        df.dropna(subset=['DEFECT_ID', 'UNIT_INDEX_X', 'UNIT_INDEX_Y'], inplace=True)
        
        # Ensure correct data types
        for col in ['DEFECT_ID', 'UNIT_INDEX_X', 'UNIT_INDEX_Y']:
            df[col] = df[col].astype(int)

        # Step 3: Transform Coordinates for 2x2 Gapped Plot
        PANEL_SIZE = 7
        GAP_SIZE = 1

        # Calculate the base position within a 7x7 panel
        plot_x_base = df['UNIT_INDEX_Y'] % PANEL_SIZE
        plot_y_base = df['UNIT_INDEX_X'] % PANEL_SIZE
        
        # Add an offset if the defect is in the top or right set of panels
        x_offset = np.where(df['UNIT_INDEX_Y'] >= PANEL_SIZE, PANEL_SIZE + GAP_SIZE, 0)
        y_offset = np.where(df['UNIT_INDEX_X'] >= PANEL_SIZE, PANEL_SIZE + GAP_SIZE, 0)
        
        # Final plot coordinates include base, offset, and random jitter for visualization
        df['plot_x'] = plot_x_base + x_offset + np.random.rand(len(df))
        df['plot_y'] = plot_y_base + y_offset + np.random.rand(len(df))

        return df

    except Exception as e:
        st.error(f"Failed to process the Excel file. Please ensure it has the correct format.")
        st.error(f"Error details: {e}")
        return None
