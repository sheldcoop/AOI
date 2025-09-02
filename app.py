# app.py
# A robust, single-file Streamlit application using a logical data-finding approach.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

# --- CORE LOGIC: Find the header row and load the data correctly ---
@st.cache_data
def load_defect_data(uploaded_file):
    try:
        # Load the uploaded file into a BytesIO object to be read multiple times
        file_bytes = BytesIO(uploaded_file.getvalue())

        # 1. Find the header row by scanning the first few rows
        header_row_index = None
        for i in range(5): # Check the first 5 rows
            df_peek = pd.read_excel(file_bytes, header=i, nrows=1)
            # Reset the buffer so the next read starts from the beginning
            file_bytes.seek(0)
            if 'DEFECT_ID' in df_peek.columns:
                header_row_index = i
                break
        
        if header_row_index is None:
            st.error("Could not find the 'DEFECT_ID' header row in the first 5 rows of the Excel file.")
            return None

        # 2. Read the Excel file using the located header row
        df = pd.read_excel(file_bytes, header=header_row_index)

        # 3. Clean and process the data
        required_cols = ['DEFECT_ID', 'DEFECT_TYPE', 'X_COORDINATES', 'Y_COORDINATES', 'UNIT_INDEX_X', 'UNIT_INDEX_Y']
        if not all(col in df.columns for col in required_cols):
            missing = [col for col in required_cols if col not in df.columns]
            st.error(f"File is missing required columns: {missing}")
            return None
            
        df = df[required_cols].copy()
        df.dropna(subset=['DEFECT_ID'], inplace=True)
        
        # In your file, ID and Type are sometimes merged. Let's handle that.
        # If the DEFECT_TYPE column is mostly empty, it means the info is in the DEFECT_ID column.
        if df['DEFECT_TYPE'].isnull().mean() > 0.9:
            split_data = df['DEFECT_ID'].astype(str).str.split(n=1, expand=True)
            df['DEFECT_ID'] = pd.to_numeric(split_data[0], errors='coerce')
            df['DEFECT_TYPE'] = split_data[1].str.strip()
            df.dropna(subset=['DEFECT_ID'], inplace=True)

        for col in ['UNIT_INDEX_X', 'UNIT_INDEX_Y']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        for col in ['DEFECT_ID', 'UNIT_INDEX_X', 'UNIT_INDEX_Y']:
            df[col] = df[col].astype(int)

        return df.reset_index(drop=True)

    except Exception as e:
        st.error(f"A critical error occurred while processing the Excel file: {e}")
        return None

# --- UI AND PLOTTING ---
st.set_page_config(layout="wide")
st.title("Interactive Panel Defect Map")
uploaded_file = st.sidebar.file_uploader("Upload Defect Excel File")

if uploaded_file:
    df = load_defect_data(uploaded_file)
    
    if df is not None and not df.empty:
        st.sidebar.metric("Total Defects Found", len(df))
        
        fig = go.Figure()
        # ... (plotting logic is the same as before)
        defect_style_map = {
            'Nick': 'magenta', 'Short': 'red', 'Missing Feature': 'lime', 'Cut': 'cyan',
            'Fine Short': '#da70d6', 'Pad Violation': 'white', 'Island': 'orange',
            'Cut/Short': '#00bfff', 'Nick/Protrusion': 'yellow'
        }
        for dtype, color in defect_style_map.items():
            dff = df[df['DEFECT_TYPE'] == dtype]
            if not dff.empty:
                fig.add_trace(go.Scatter(x=dff['UNIT_INDEX_Y'], y=dff['UNIT_INDEX_X'], mode='markers',
                    marker=dict(color=color, size=12, line=dict(width=1.5, color='Black')), name=dtype))
        
        grid_x, grid_y = int(df['UNIT_INDEX_X'].max()+1), int(df['UNIT_INDEX_Y'].max()+1)
        shapes = []
        for i in range(grid_y + 1): shapes.append(dict(type='line', x0=i-0.5, y0=-0.5, x1=i-0.5, y1=grid_x-0.5, line=dict(color='black', width=4)))
        for i in range(grid_x + 1): shapes.append(dict(type='line', x0=-0.5, y0=i-0.5, x1=grid_y-0.5, y1=i-0.5, line=dict(color='black', width=4)))
        
        fig.update_layout(plot_bgcolor='#F4A460', shapes=shapes, width=800, height=800, yaxis_scaleanchor='x')
        st.plotly_chart(fig)
else:
    st.info("Please upload an Excel file to begin.")
