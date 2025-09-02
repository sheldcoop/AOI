# app.py
# FINAL VERSION: Based on the debugging output.

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
DEFECT_STYLE_MAP: Dict[str, str] = {
    'Nick': 'magenta', 'Short': 'red', 'Missing Feature': 'lime', 'Cut': 'cyan',
    'Fine Short': '#da70d6', 'Pad Violation': 'white', 'Island': '#ff8c00',
    'Cut/Short': '#00bfff', 'Nick/Protrusion': 'yellow', 'Unknown': 'black'
}
PLOT_BG_COLOR: str = '#F4A460'

# --- 2. CORE LOGIC FUNCTIONS ---
@st.cache_data
def extract_images_from_excel(uploaded_file_contents: bytes) -> List[str]:
    EXTRACT_FOLDER = "temp_excel_contents"
    MEDIA_FOLDER = os.path.join(EXTRACT_FOLDER, 'xl', 'media')
    if os.path.exists(EXTRACT_FOLDER): shutil.rmtree(EXTRACT_FOLDER)
    os.makedirs(MEDIA_FOLDER)
    temp_excel_path = os.path.join(EXTRACT_FOLDER, "temp.xlsx")
    with open(temp_excel_path, "wb") as f: f.write(uploaded_file_contents)
    try:
        with zipfile.ZipFile(temp_excel_path, 'r') as zf: zf.extractall(EXTRACT_FOLDER)
    except Exception: return []
    if os.path.exists(MEDIA_FOLDER):
        try:
            files = sorted(os.listdir(MEDIA_FOLDER), key=lambda f: int(''.join(filter(str.isdigit, f))))
            return [os.path.join(MEDIA_FOLDER, f) for f in files]
        except Exception:
            return sorted([os.path.join(MEDIA_FOLDER, f) for f in os.listdir(MEDIA_FOLDER)])
    return []

@st.cache_data
def load_and_clean_data(uploaded_file) -> Optional[pd.DataFrame]:
    try:
        # --- THE FINAL, CORRECT WAY TO READ THIS FILE ---
        # 1. Tell pandas there is NO header.
        # 2. Skip the first row which contains the red titles.
        # 3. Read only the first 9 columns (A to I).
        df = pd.read_excel(uploaded_file, header=None, skiprows=1, usecols="A:I")

        # 4. Assign the correct column names ourselves.
        df.columns = [
            'DEFECT_ID', 'DEFECT_TYPE', 'X_COORDINATES', 'Y_COORDINATES',
            'UNIT_INDEX_X', 'UNIT_INDEX_Y', 'MODALITY_1', 'MODALITY_2', 'ENHANCED_IMAGE'
        ]

        # --- Data Cleaning ---
        df.dropna(subset=['DEFECT_ID'], inplace=True)
        for col in ['UNIT_INDEX_X', 'UNIT_INDEX_Y', 'X_COORDINATES', 'Y_COORDINATES']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Split the combined 'DEFECT_ID' column (e.g., "1 Short")
        split_data = df['DEFECT_ID'].astype(str).str.split(n=1, expand=True)
        df['DEFECT_ID'] = pd.to_numeric(split_data[0], errors='coerce')
        df['DEFECT_TYPE'] = split_data[1]

        df.dropna(subset=['DEFECT_ID'], inplace=True)

        for col in ['DEFECT_ID', 'UNIT_INDEX_X', 'UNIT_INDEX_Y']:
            df[col] = df[col].astype(int)
            
        return df.reset_index(drop=True)

    except Exception as e:
        st.error(f"Failed to process Excel data. Please check the file format. Error: {e}")
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
        images = extract_images_from_excel(uploaded_file.getvalue())
        if len(images) >= len(df) * 2:
            df['image_path_mod1'] = images[::2][:len(df)]
            df['image_path_mod2'] = images[1::2][:len(df)]
        
        st.sidebar.header("Data Summary")
        st.sidebar.metric("Total Defects Found", len(df))
        panel_dims = f"{df['UNIT_INDEX_X'].max() + 1} Rows x {df['UNIT_INDEX_Y'].max() + 1} Cols"
        st.sidebar.metric("Panel Dimensions", panel_dims)
        st.sidebar.dataframe(df["DEFECT_TYPE"].value_counts())
        
        col1, col2 = st.columns([2, 1])
        with col1:
            np.random.seed(42)
            df['plot_x'] = df['UNIT_INDEX_Y'] + np.random.uniform(0.15, 0.85, size=len(df))
            df['plot_y'] = df['UNIT_INDEX_X'] + np.random.uniform(0.15, 0.85, size=len(df))
            
            fig = go.Figure()
            for dtype, color in DEFECT_STYLE_MAP.items():
                dff = df[df['DEFECT_TYPE'].astype(str) == dtype]
                if not dff.empty:
                    fig.add_trace(go.Scatter(x=dff['plot_x'], y=dff['plot_y'], mode='markers',
                        marker=dict(color=color, size=12, line=dict(width=1.5, color='Black')),
                        name=dtype, customdata=dff.index, hoverinfo='none'))

            grid_x, grid_y = int(df['UNIT_INDEX_X'].max()+1), int(df['UNIT_INDEX_Y'].max()+1)
            shapes = []
            for i in range(grid_y + 1): shapes.append(dict(type='line', x0=i-0.5, y0=-0.5, x1=i-0.5, y1=grid_x-0.5, line=dict(color='black', width=4)))
            for i in range(grid_x + 1): shapes.append(dict(type='line', x0=-0.5, y0=i-0.5, x1=grid_y-0.5, y1=i-0.5, line=dict(color='black', width=4)))
            
            fig.update_layout(plot_bgcolor=PLOT_BG_COLOR, shapes=shapes, width=800, height=800,
                xaxis=dict(range=[-0.5, grid_y-0.5]), yaxis=dict(range=[-0.5, grid_x-0.5]),
                yaxis_scaleanchor='x', legend_title_text='Defect Types')
            
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
