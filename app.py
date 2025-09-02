# app.py
# Final Version: Significantly larger plot with no borders on the defect markers.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- 1. Page Configuration ---
st.set_page_config(page_title="Large Quad Panel Map", layout="wide")

# --- 2. Hardcoded Sample Data ---
NUM_DEFECTS = 1000
GRID_SIZE_X = 20
GRID_SIZE_Y = 20

defect_types = ['Nick', 'Short', 'Missing Feature', 'Pad Violation', 'Other']

df = pd.DataFrame({
    'UNIT_INDEX_X': np.random.randint(0, GRID_SIZE_X, size=NUM_DEFECTS),
    'UNIT_INDEX_Y': np.random.randint(0, GRID_SIZE_Y, size=NUM_DEFECTS),
    'DEFECT_TYPE': np.random.choice(defect_types, size=NUM_DEFECTS)
})

defect_style_map = {
    'Nick': 'magenta', 'Short': 'deeppink', 'Missing Feature': 'lime',
    'Pad Violation': 'white', 'Other': 'red'
}
PANEL_COLOR = '#8B4513'
BORDER_COLOR = '#556B2F'

# --- 3. Transform Coordinates to Create Gaps ---
PANEL_SIZE = 10
GAP_SIZE = 1

def transform_coords(df):
    plot_x = df['UNIT_INDEX_Y'] % PANEL_SIZE
    plot_y = df['UNIT_INDEX_X'] % PANEL_SIZE
    plot_y = plot_y + np.where(df['UNIT_INDEX_X'] >= PANEL_SIZE, PANEL_SIZE + GAP_SIZE, 0)
    plot_x = plot_x + np.where(df['UNIT_INDEX_Y'] >= PANEL_SIZE, PANEL_SIZE + GAP_SIZE, 0)
    df['plot_x'] = plot_x + np.random.uniform(0.1, 0.9, size=len(df))
    df['plot_y'] = plot_y + np.random.uniform(0.1, 0.9, size=len(df))
    return df

df = transform_coords(df)

# --- 4. Create a Single Plotly Figure ---
fig = go.Figure()

# Add all defects to the figure
for dtype, color in defect_style_map.items():
    dff = df[df['DEFECT_TYPE'] == dtype]
    if not dff.empty:
        fig.add_trace(go.Scatter(
            x=dff['plot_x'], y=dff['plot_y'], mode='markers',
            # --- THIS IS THE FIX for the dot borders ---
            marker=dict(color=color, size=6, line=dict(width=0)), # Set line width to 0
            # ---------------------------------------------
            name=dtype, showlegend=False
        ))

# --- 5. Manually Draw the Panels and Grids ---
shapes = []
panel_coords = [
    (0, 0), (0, PANEL_SIZE + GAP_SIZE),
    (PANEL_SIZE + GAP_SIZE, 0), (PANEL_SIZE + GAP_SIZE, PANEL_SIZE + GAP_SIZE)
]

for x_start, y_start in panel_coords:
    for i in range(1, PANEL_SIZE):
        shapes.append(dict(type='line', x0=x_start+i, y0=y_start, x1=x_start+i, y1=y_start+PANEL_SIZE-0.01, line=dict(color="black", width=0.5)))
        shapes.append(dict(type='line', x0=x_start, y0=y_start+i, x1=x_start+PANEL_SIZE-0.01, y1=y_start+i, line=dict(color="black", width=0.5)))

# --- 6. Style the Final Layout ---
total_size = 2 * PANEL_SIZE + GAP_SIZE
# --- THIS IS THE FIX for the overall size ---
# Increased width and height significantly
fig.update_layout(
    width=1200, height=1200,
    # ----------------------------------------
    plot_bgcolor=PANEL_COLOR,
    paper_bgcolor=BORDER_COLOR,
    xaxis=dict(range=[-0.5, total_size-0.5], showticklabels=False, showgrid=False, zeroline=False),
    yaxis=dict(range=[-0.5, total_size-0.5], showticklabels=False, showgrid=False, zeroline=False),
    shapes=shapes,
    margin=dict(l=20, r=20, t=20, b=20),
    showlegend=False,
    yaxis_scaleanchor='x'
)

# --- 7. Display the plot in Streamlit ---
st.plotly_chart(fig)
