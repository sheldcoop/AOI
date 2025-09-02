# app.py
# A single-file Streamlit application for robust defect visualization.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
import zipfile
import os
import shutil
from typing import List, Optional, Dict

# --- 1. CONFIGURATION ---
# All settings are defined here at the top.
DEFECT_STYLE_MAP: Dict[str, str] = {
    'Nick': 'magenta', 'Short': 'red', 'Missing Feature': 'lime', 'Cut': 'cyan',
    'Fine Short': '#da70d6', 'Pad Violation': 'white', 'Island': '#ff8c00',
    'Cut/Short': '#00bfff', 'Nick/Protrusion': 'yellow', 'Unknown': 'black'
}
PLOT_BG_COLOR: str = '#F4A460'

# --- 2. CORE LOGIC FUNCTIONS ---
# These functions handle the data processing. They are cached for performance.

@st.cache_data
def load_and_clean_data(uploaded_file) -> Optional[pd.DataFrame]:
    """
    Loads and cleans data from the specific Excel file format, renaming columns for robustness.
    """
    try:
        # header=1 tells pandas to use the SECOND row (index 1) as the column names.
        df = pd.read_excel(uploaded_file, header=1)

        # --- THE NEW, ROBUST FIX ---
        # Rename the first 6 columns to our standard names, regardless of what they are in the file.
        # This avoids errors from spaces or typos in the Excel header.
        df.columns.values[0] = 'DEFECT_ID'
        df.columns.values[1] = 'DEFECT_TYPE'
        df.columns.values[2] = 'X_COORDINATES'
        df.columns.values[3] = 'Y_COORDINATES'
        df.columns.values[4] = 'UNIT_INDEX_X'
        df.columns.values[5] = 'UNIT_INDEX_Y'
        
        # Now proceed with cleaning using our standard names
        required_cols = ['DEFECT_ID', 'DEFECT_TYPE', 'X_COORDINATES', 'Y_COORDINATES', 'UNIT_INDEX_X', 'UNIT_INDEX_Y']
        df = df[required_cols]

        df.dropna(subset=['DEFECT_ID'], inplace=True)
        for col in ['UNIT_INDEX_X', 'UNIT_INDEX_Y', 'X_COORDINATES', 'Y_COORDINATES']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        for col in ['DEFECT_ID', 'UNIT_INDEX_X', 'UNIT_INDEX_Y']:
            df[col] = df[col].astype(int)
            
        return df.reset_index(drop=True)

    except Exception as e:
        st.error(f"Failed to process Excel data. Please check the file format. Error: {e}")
        return None

@st.cache_data
def load_and_clean_data(uploaded_file) -> Optional[pd.DataFrame]:
    """Loads and cleans data from the specific Excel file format."""
    try:
        # header=1 tells pandas to use the SECOND row (index 1) as the column names.
        df = pd.read_excel(uploaded_file, header=1)
        
        required_cols = ['DEFECT_ID', 'DEFECT_TYPE', 'X_COORDINATES', 'Y_COORDINATES', 'UNIT_INDEX_X', 'UNIT_INDEX_Y']
        # Check if all required columns exist
        if not all(col in df.columns for col in required_cols):
            st.error(f"Excel file is missing one of the required columns: {required_cols}")
            return None
            
        df = df[required_cols]

        df.dropna(subset=['DEFECT_ID'], inplace=True)
        for col in ['UNIT_INDEX_X', 'UNIT_INDEX_Y', 'X_COORDINATES', 'Y_COORDINATES']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        for col in ['DEFECT_ID', 'UNIT_INDEX_X', 'UNIT_INDEX_Y']:
            df[col] = df[col].astype(int)
            
        return df.reset_index(drop=True)

    except Exception as e:
        st.error(f"Failed to process Excel data. Please check the file format. Error: {e}")
        return None

# --- 3. MAIN APPLICATION ---
def main():
    st.set_page_config(page_title="Defect-Viz", layout="wide")

    # --- Sidebar ---
    st.sidebar.title("Defect-Viz Control Panel")
    uploaded_file = st.sidebar.file_uploader("Upload Defect Excel File", type=["xlsx"])

    # --- Main Panel ---
    if uploaded_file is None:
        st.header("Welcome to the Interactive Defect Visualizer")
        st.info("Please upload your defect Excel file using the sidebar to begin.")
    else:
        df = load_and_clean_data(uploaded_file)
        
        if df is not None and not df.empty:
            images = extract_images_from_excel(uploaded_file.getvalue())

            if len(images) >= len(df) * 2:
                df['image_path_mod1'] = images[::2][:len(df)]
                df['image_path_mod2'] = images[1::2][:len(df)]
            
            # --- Display Summary in Sidebar ---
            st.sidebar.header("Data Summary")
            st.sidebar.metric("Total Defects Found", len(df))
            panel_dims = f"{df['UNIT_INDEX_X'].max() + 1} Rows x {df['UNIT_INDEX_Y'].max() + 1} Cols"
            st.sidebar.metric("Panel Dimensions", panel_dims)
            st.sidebar.dataframe(df["DEFECT_TYPE"].value_counts())
            
            # --- Display Dashboard ---
            col1, col2 = st.columns([2, 1])

            with col1:
                np.random.seed(42)
                df['plot_x'] = df['UNIT_INDEX_Y'] + np.random.uniform(0.15, 0.85, size=len(df))
                df['plot_y'] = df['UNIT_INDEX_X'] + np.random.uniform(0.15, 0.85, size=len(df))
                
                fig = go.Figure()
                for dtype, color in DEFECT_STYLE_MAP.items():
                    dff = df[df['DEFECT_TYPE'].astype(str) == str(dtype)]
                    if not dff.empty:
                        fig.add_trace(go.Scatter(x=dff['plot_x'], y=dff['plot_y'], mode='markers',
                            marker=dict(color=color, size=12, line=dict(width=1.5, color='Black')),
                            name=dtype, customdata=dff.index, hoverinfo='none'))

                grid_x, grid_y = int(df['UNIT_INDEX_X'].max()+1), int(df['UNIT_INDEX_Y'].max()+1)
                shapes = []
                for i in range(grid_y + 1): shapes.append(dict(type='line', x0=i-0.5, y0=-0.5, x1=i-0.5, y1=grid_x-0.5, line=dict(color='black', width=4)))
                for i in range(grid_x + 1): shapes.append(dict(type='line', x0=-0.5, y0=i-0.5, x1=grid_y-0.5, y1=i-0.5, line=dict(color='black', width=4)))
                
                fig.update_layout(title_text='Interactive Panel Defect Map', plot_bgcolor=PLOT_BG_COLOR,
                    shapes=shapes, width=800, height=800, yaxis_scaleanchor='x')
                
                selected_points = plotly_events(fig, click_event=True, key="plot_click")
            
            with col2:
                st.subheader("Selected Defect Details")
                details_placeholder = st.empty()
                if selected_points:
                    point_index = selected_points[0]['customdata']
                    info = df.loc[point_index]
                    with details_placeholder.container():
                        st.markdown(f"**Defect ID:** `{info['DEFECT_ID']}`")
                        st.markdown(f"**Type:** `{info['DEFECT_TYPE']}`")
                        if 'image_path_mod1' in df.columns and os.path.exists(info['image_path_mod1']):
                            st.image(info['image_path_mod1'], caption="Modality 1")
                        if 'image_path_mod2' in df.columns and os.path.exists(info['image_path_mod2']):
                            st.image(info['image_path_mod2'], caption="Modality 2")
                else:
                    details_placeholder.info("Click on a defect in the map to see its details.")

if __name__ == "__main__":
    main()
