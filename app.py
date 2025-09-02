# app.py
# Version 2: Adding file upload and real data processing.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
DEFECT_STYLE_MAP = {
    'Nick': 'magenta', 'Short': 'red', 'Missing Feature': 'lime', 'Cut': 'cyan',
    'Fine Short': '#da70d6', 'Pad Violation': 'white', 'Island': '#ff8c00',
    'Cut/Short': '#00bfff', 'Nick/Protrusion': 'yellow', 'Unknown': 'black'
}
PLOT_BG_COLOR = '#F4A460'

# --- 2. CORE DATA LOADING FUNCTION ---
# This function will process the uploaded Excel file.
@st.cache_data
def load_and_clean_data(uploaded_file):
    try:
        # Use the second row (index 1) as the header.
        df = pd.read_excel(uploaded_file, header=1)
        
        required_cols = ['DEFECT_ID', 'DEFECT_TYPE', 'X_COORDINATES', 'Y_COORDINATES', 'UNIT_INDEX_X', 'UNIT_INDEX_Y']
        # Check if all required columns exist
        if not all(col in df.columns for col in required_cols):
            missing_cols = [col for col in required_cols if col not in df.columns]
            st.error(f"Excel file is missing required columns: {missing_cols}")
            return None
        
        df = df[required_cols].copy()
        df.dropna(subset=['DEFECT_ID'], inplace=True)
        
        for col in ['UNIT_INDEX_X', 'UNIT_INDEX_Y', 'X_COORDINATES', 'Y_COORDINATES']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        for col in ['DEFECT_ID', 'UNIT_INDEX_X', 'UNIT_INDEX_Y']:
            df[col] = df[col].astype(int)
            
        return df.reset_index(drop=True)
    except Exception as e:
        st.error(f"Error processing Excel data. Please check the file format. Error: {e}")
        return None

# --- 3. MAIN APPLICATION ---

# Configure the page
st.set_page_config(page_title="Defect-Viz", layout="wide")

# --- Sidebar ---
st.sidebar.title("Defect-Viz Control Panel")
uploaded_file = st.sidebar.file_uploader("Upload Defect Excel File", type=["xlsx"])

# --- Main Panel ---
st.title("Interactive Panel Defect Map")

if uploaded_file is None:
    # State 1: No file uploaded
    st.info("Please upload your defect Excel file using the sidebar to begin.")
else:
    # State 2: File has been uploaded
    df = load_and_clean_data(uploaded_file)
    
    if df is not None and not df.empty:
        # --- Display Summary in Sidebar ---
        st.sidebar.header("Data Summary")
        st.sidebar.metric("Total Defects Found", len(df))
        panel_dims = f"{df['UNIT_INDEX_X'].max() + 1} Rows x {df['UNIT_INDEX_Y'].max() + 1} Cols"
        st.sidebar.metric("Panel Dimensions", panel_dims)
        st.sidebar.dataframe(df["DEFECT_TYPE"].value_counts())

        # --- Display the Plot ---
        np.random.seed(42)
        df['plot_x'] = df['UNIT_INDEX_Y'] + np.random.uniform(0.15, 0.85, size=len(df))
        df['plot_y'] = df['UNIT_INDEX_X'] + np.random.uniform(0.15, 0.85, size=len(df))
        
        fig = go.Figure()
        for dtype, color in DEFECT_STYLE_MAP.items():
            dff = df[df['DEFECT_TYPE'].astype(str) == dtype]
            if not dff.empty:
                fig.add_trace(go.Scatter(
                    x=dff['plot_x'], y=dff['plot_y'], mode='markers',
                    marker=dict(color=color, size=12, line=dict(width=1.5, color='Black')),
                    name=dtype,
                    hoverinfo='text',
                    hovertext=[f"ID: {row['DEFECT_ID']}<br>Type: {row['DEFECT_TYPE']}" for index, row in dff.iterrows()]
                ))

        grid_x, grid_y = int(df['UNIT_INDEX_X'].max()+1), int(df['UNIT_INDEX_Y'].max()+1)
        shapes = []
        for i in range(grid_y + 1): shapes.append(dict(type='line', x0=i-0.5, y0=-0.5, x1=i-0.5, y1=grid_x-0.5, line=dict(color='black', width=4)))
        for i in range(grid_x + 1): shapes.append(dict(type='line', x0=-0.5, y0=i-0.5, x1=grid_y-0.5, y1=i-0.5, line=dict(color='black', width=4)))
        
        fig.update_layout(
            plot_bgcolor=PLOT_BG_COLOR, shapes=shapes, width=800, height=800,
            xaxis=dict(range=[-0.5, grid_y-0.5]), yaxis=dict(range=[-0.5, grid_x-0.5]),
            yaxis_scaleanchor='x', legend_title_text='Defect Types'
        )

        st.plotly_chart(fig)
    else:
        # This message shows if the file was uploaded but couldn't be processed
        st.error("Could not process the uploaded Excel file. Please ensure it has the correct format and data.")
