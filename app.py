# app.py
# FINAL ATTEMPT: Simplest possible data loading logic.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Defect-Viz", layout="wide")
st.title("Interactive Panel Defect Map")
uploaded_file = st.sidebar.file_uploader("Upload Defect Excel File", type=["xlsx"])

@st.cache_data
def load_data(uploaded_file):
    try:
        # STRATEGY: Read the file with NO header and skip the title row.
        # Then, manually assign the column names we know are correct.
        df = pd.read_excel(uploaded_file, header=None, skiprows=1)

        # The first 9 columns are what we care about.
        df = df.iloc[:, :9]
        
        # Manually assign the correct column names.
        df.columns = [
            'RAW_ID_TYPE', 'X_COORDINATES', 'Y_COORDINATES',
            'UNIT_INDEX_X', 'UNIT_INDEX_Y', 'MODALITY_1', 'MODALITY_2', 
            'ENHANCED_IMAGE', 'EXTRA_COL' # Assign names to all read columns
        ]
        
        # Clean the combined ID and Type column
        df.dropna(subset=['RAW_ID_TYPE'], inplace=True)
        split_data = df['RAW_ID_TYPE'].astype(str).str.split(n=1, expand=True)
        df['DEFECT_ID'] = pd.to_numeric(split_data[0], errors='coerce')
        df['DEFECT_TYPE'] = split_data[1]

        # Final cleaning
        df.dropna(subset=['DEFECT_ID'], inplace=True)
        df['DEFECT_ID'] = df['DEFECT_ID'].astype(int)
        for col in ['UNIT_INDEX_X', 'UNIT_INDEX_Y']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        return df

    except Exception as e:
        st.error(f"Error reading the Excel file. Please ensure it's not password-protected. Error: {e}")
        return None

if uploaded_file:
    df = load_data(uploaded_file)
    if df is not None and not df.empty:
        # --- Display the plot (using the same logic as your Colab code) ---
        st.sidebar.metric("Defects Found", len(df))
        
        np.random.seed(42)
        df['plot_x'] = df['UNIT_INDEX_Y'] + np.random.uniform(0.15, 0.85, size=len(df))
        df['plot_y'] = df['UNIT_INDEX_X'] + np.random.uniform(0.15, 0.85, size=len(df))

        fig = go.Figure()
        defect_style_map = {
            'Nick': 'magenta', 'Short': 'red', 'Missing Feature': 'lime', 'Cut': 'cyan',
            'Fine Short': '#da70d6', 'Pad Violation': 'white', 'Island': 'orange',
            'Cut/Short': '#00bfff', 'Nick/Protrusion': 'yellow'
        }

        for dtype, color in defect_style_map.items():
            dff = df[df['DEFECT_TYPE'] == dtype]
            if not dff.empty:
                fig.add_trace(go.Scatter(x=dff['plot_x'], y=dff['plot_y'], mode='markers',
                    marker=dict(color=color, size=12, line=dict(width=1.5, color='Black')), name=dtype))

        grid_x, grid_y = int(df['UNIT_INDEX_X'].max()+1), int(df['UNIT_INDEX_Y'].max()+1)
        shapes = []
        for i in range(grid_y + 1): shapes.append(dict(type='line', x0=i-0.5, y0=-0.5, x1=i-0.5, y1=grid_x-0.5, line=dict(color='black', width=4)))
        for i in range(grid_x + 1): shapes.append(dict(type='line', x0=-0.5, y0=i-0.5, x1=grid_y-0.5, y1=i-0.5, line=dict(color='black', width=4)))
        
        fig.update_layout(plot_bgcolor='#F4A460', shapes=shapes, width=800, height=800, yaxis_scaleanchor='x')
        st.plotly_chart(fig)
else:
    st.info("Please upload a file to begin.")
