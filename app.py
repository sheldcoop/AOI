# app.py
# Final Version: Pure Plotly, with perfect symmetrical padding.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
from PIL import Image, ImageDraw
import os
import shutil

# --- 1. Page Configuration & Global Styles ---
st.set_page_config(page_title="Quad Panel Defect Map", layout="wide")
st.title("Interactive Defect Map")
PANEL_COLOR = '#8B4513'
BG_COLOR = '#556B2F'
DEFECT_STYLE_MAP = {
    'Nick': 'magenta', 'Short': 'deeppink', 'Missing Feature': 'lime',
    'Pad Violation': 'white', 'Other': 'red'
}

# --- 2. Data and Image Fabrication ---
@st.cache_resource
def generate_data():
    NUM_DEFECTS = 100; GRID_SIZE = 14; IMAGE_FOLDER = "fabricated_images"
    df = pd.DataFrame({'DEFECT_ID': list(range(1, NUM_DEFECTS + 1)), 'DEFECT_TYPE': np.random.choice(list(DEFECT_STYLE_MAP.keys()), size=NUM_DEFECTS), 'UNIT_INDEX_X': np.random.randint(0, GRID_SIZE, size=NUM_DEFECTS), 'UNIT_INDEX_Y': np.random.randint(0, GRID_SIZE, size=NUM_DEFECTS)})
    if os.path.exists(IMAGE_FOLDER): shutil.rmtree(IMAGE_FOLDER)
    os.makedirs(IMAGE_FOLDER)
    image_paths_mod1, image_paths_mod2 = [], []
    for i in range(1, NUM_DEFECTS + 1):
        for mod, path_list in [(1, image_paths_mod1), (2, image_paths_mod2)]:
            img = Image.new('RGB', (200, 150), color=('darkblue' if mod == 1 else 'darkred')); draw = ImageDraw.Draw(img)
            draw.text((10, 10), f"IMAGE FOR\nDEFECT ID: {i}\nMODALITY: {mod}", fill='white'); path = os.path.join(IMAGE_FOLDER, f"img_{i:03d}_mod{mod}.png"); img.save(path); path_list.append(path)
    df['image_path_mod1'] = image_paths_mod1; df['image_path_mod2'] = image_paths_mod2
    return df

df = generate_data()

# --- 3. Transform Coordinates for Plotting ---
PANEL_SIZE = 7; GAP_SIZE = 1
df['plot_x'] = (df['UNIT_INDEX_Y'] % PANEL_SIZE) + np.where(df['UNIT_INDEX_Y'] >= PANEL_SIZE, PANEL_SIZE + GAP_SIZE, 0) + np.random.uniform(0.1, 0.9, size=len(df))
df['plot_y'] = (df['UNIT_INDEX_X'] % PANEL_SIZE) + np.where(df['UNIT_INDEX_X'] >= PANEL_SIZE, PANEL_SIZE + GAP_SIZE, 0) + np.random.uniform(0.1, 0.9, size=len(df))

col1, col2 = st.columns([3, 1])

with col1:
    fig = go.Figure()
    for dtype, color in DEFECT_STYLE_MAP.items():
        dff = df[df['DEFECT_TYPE'] == dtype]
        fig.add_trace(go.Scatter(x=dff['plot_x'], y=dff['plot_y'], mode='markers', marker=dict(color=color, size=5), name=dtype, customdata=dff.index, hoverinfo='none'))

    shapes = []
    panel_coords = [(0, 0), (0, PANEL_SIZE + GAP_SIZE), (PANEL_SIZE + GAP_SIZE, 0), (PANEL_SIZE + GAP_SIZE, PANEL_SIZE + GAP_SIZE)]
    for x_start, y_start in panel_coords:
        shapes.append(dict(type='rect', x0=x_start-0.5, y0=y_start-0.5, x1=x_start+PANEL_SIZE-0.5, y1=y_start+PANEL_SIZE-0.5, line=dict(width=0), fillcolor=PANEL_COLOR, layer='below'))
        shapes.append(dict(type='rect', x0=x_start-0.5, y0=y_start-0.5, x1=x_start+PANEL_SIZE-0.5, y1=y_start+PANEL_SIZE-0.5, line=dict(color="black", width=4), fillcolor='rgba(0,0,0,0)', layer='below'))
        for i in range(1, PANEL_SIZE):
            shapes.append(dict(type='line', x0=x_start+i-0.5, y0=y_start-0.5, x1=x_start+i-0.5, y1=y_start+PANEL_SIZE-0.5, line=dict(color="black", width=1), layer='below'))
            shapes.append(dict(type='line', x0=x_start-0.5, y0=y_start+i-0.5, x1=x_start+PANEL_SIZE-0.5, y1=y_start+i-0.5, line=dict(color="black", width=1), layer='below'))
    
    # --- THIS IS THE FIX ---
    fig.update_layout(
        width=600, # A wide container
        height=600, # A shorter container
        plot_bgcolor=BG_COLOR,
        paper_bgcolor=BG_COLOR,
        xaxis=dict(
            range=[-1.5, 16.5],
            domain=[0, 1], # Use full width for x-axis calculations
            visible=False
        ),
        yaxis=dict(
            range=[-1.5, 16.5],
            # This is the key: tell y-axis to only occupy a central square of the vertical space
            # which forces the plot to be square and centered.
            domain=[0.1, 0.9], 
            scaleanchor='x',
            scaleratio=1,
            visible=False
        ),
        shapes=shapes,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False
    )
    # ---------------------
    
    selected_points = plotly_events(fig, click_event=True, key="plot_click")

with col2:
    st.header("Defect Details")
    details_placeholder = st.empty()
    if selected_points:
        point_index = selected_points[0]['customdata']
        info = df.loc[point_index]
        with details_placeholder.container():
            st.markdown(f"**Defect ID:** `{info['DEFECT_ID']}`")
            st.image(info['image_path_mod1'], caption="Modality 1")
            st.image(info['image_path_mod2'], caption="Modality 2")
    else:
        details_placeholder.info("Click on a defect to see its details.")
