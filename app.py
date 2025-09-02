# app.py
# Version 3: Added robust column name cleaning.

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
@st.cache_data
def load_and_clean_data(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file, header=1)

        # --- THIS IS THE FIX ---
        # Clean up the column names read from the Excel file.
        # 1. Strip whitespace from start/end of each column name.
        # 2. Replace spaces and special characters with underscores.
        df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace(r'[^A-Za-z0-9_]', '', regex=True)
        # ---------------------

        required_cols = ['DEFECT_ID', 'DEFECT_TYPE', 'X_COORDINATES', 'Y_COORDINATES', 'UNIT_INDEX_X', 'UNIT_INDEX_Y']
        if not all(col in df.columns for col in required_cols):
            missing = [col for col in required_cols if col not in df.columns]
            st.error(f"After cleaning, the following required columns are still missing: {missing}")
            return None
        
        df = df[required_cols].copy()
        df.dropna(subset=['DEFECT_ID'], inplace=True)
        
        for col in ['UNIT_INDEX_X', 'UNIT_INDEX_Y', 'X_COORDINATES', 'Y_COORDINATES']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        df['DEFECT_ID'] = df['DEFECT_ID'].astype(int)
        df['UNIT_INDEX_X'] = df['UNIT_INDEX_X'].astype(int)
        df['UNIT_INDEX_Y'] = df['UNIT_INDEX_Y'].astype(int)
            
        return df.reset_index(drop=True)
    except Exception as e:
        st.error(f"Error processing Excel data. Error: {e}")
        return None

# --- 3. MAIN APPLICATION ---
st.set_page_config(page_title="Defect-Viz", layout="wide")
st.sidebar.title("Defect-Viz Control Panel")
uploaded_file = st.sidebar.file_uploader("Upload Defect Excel File", type=["xlsx"])
st.title("Interactive Panel Defect Map")

if uploaded_file is None:
    st.info("Please upload your defect Excel file using the sidebar to begin.")
else:
    df = load_and_clean_data(uploaded_file)
    if df is not None and not df.empty:
        # --- Display Summary & Plot ---
        st.sidebar.header("Data Summary")
        st.sidebar.metric("Total Defects Found", len(df))
        panel_dims = f"{df['UNIT_INDEX_X'].max() + 1} Rows x {df['UNIT_INDEX_Y'].max() + 1} Cols"
        st.sidebar.metric("Panel Dimensions", panel_dims)
        st.sidebar.dataframe(df["DEFECT_TYPE"].value_counts())

        np.random.seed(42)
        df['plot_x'] = df['UNIT_INDEX_Y'] + np.random.uniform(0.15, 0.85, size=len(df))
        df['plot_y'] = df['UNIT_INDEX_X'] + np.random.uniform(0.15, 0.85, size=len(df))
        
        fig = go.Figure()
        # Add traces for each defect type...
        for dtype, color in DEFECT_STYLE_MAP.items():
            dff = df[df['DEFECT_TYPE'].astype(str) == dtype]
            if not dff.empty:
                fig.add_trace(go.Scatter(x=dff['plot_x'], y=dff['plot_y'], mode='markers',
                    marker=dict(color=color, size=12, line=dict(width=1.5, color='Black')), name=dtype,
                    hoverinfo='text', hovertext=[f"ID: {row['DEFECT_ID']}<br>Type: {row['DEFECT_TYPE']}" for i, row in dff.iterrows()]))

        # Style the grid...
        grid_x, grid_y = int(df['UNIT_INDEX_X'].max()+1), int(df['UNIT_INDEX_Y'].max()+1)
        shapes = []
        for i in range(grid_y + 1): shapes.append(dict(type='line', x0=i-0.5, y0=-0.5, x1=i-0.5, y1=grid_x-0.5, line=dict(color='black', width=4)))
        for i in range(grid_x + 1): shapes.append(dict(type='line', x0=-0.5, y0=i-0.5, x1=grid_y-0.5, y1=i-0.5, line=dict(color='black', width=4)))
        
        fig.update_layout(plot_bgcolor=PLOT_BG_COLOR, shapes=shapes, width=800, height=800,
            xaxis=dict(range=[-0.5, grid_y-0.5]), yaxis=dict(range=[-0.5, grid_x-0.5]),
            yaxis_scaleanchor='x', legend_title_text='Defect Types')
        
        st.plotly_chart(fig)
    else:
        st.error("Could not process the uploaded Excel file.")
