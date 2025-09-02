# app.py
# Final Simplified Version: Uses the most robust plotting method possible.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- 1. Page Configuration & New Styling ---
st.set_page_config(page_title="Quad Panel Defect Map", layout="wide")
st.title("Interactive Defect Map")

# --- NEW STYLES ---
PANEL_FILL_COLOR = '#F4A460'   # Lighter Sandy Brown
PANEL_BORDER_COLOR = '#8B4513' # SaddleBrown
BG_COLOR = '#A0522D'           # Lighter background (Sienna)
THIN_LINE_WIDTH = 2
THICK_LINE_WIDTH = 4

DEFECT_STYLE_MAP = {
    'Nick': 'magenta', 'Short': 'deeppink', 'Missing Feature': 'lime',
    'Pad Violation': 'white', 'Island': 'orange',
    'Unknown': 'red'
}

# --- 2. Data Fabrication ---
NUM_DEFECTS = 400; GRID_SIZE = 14
valid_defect_types = list(DEFECT_STYLE_MAP.keys()); valid_defect_types.remove('Unknown')
df = pd.DataFrame({
    'DEFECT_ID': list(range(1, NUM_DEFECTS + 1)),
    'DEFECT_TYPE': np.random.choice(valid_defect_types, size=NUM_DEFECTS),
    'UNIT_INDEX_X': np.random.randint(0, GRID_SIZE, size=NUM_DEFECTS),
    'UNIT_INDEX_Y': np.random.randint(0, GRID_SIZE, size=NUM_DEFECTS)
})
# Intentionally add some errors
error_indices = np.random.choice(df.index, 5, replace=False)
df.loc[error_indices, 'DEFECT_TYPE'] = "System Error"

# --- 3. Transform Coordinates & Assign Colors ---
PANEL_SIZE = 7; GAP_SIZE = 1; PADDING = 1
df['plot_x'] = (df['UNIT_INDEX_Y'] % PANEL_SIZE) + np.where(df['UNIT_INDEX_Y'] >= PANEL_SIZE, PANEL_SIZE + GAP_SIZE + PADDING, PADDING) + np.random.uniform(0.1, 0.9, size=len(df))
df['plot_y'] = (df['UNIT_INDEX_X'] % PANEL_SIZE) + np.where(df['UNIT_INDEX_X'] >= PANEL_SIZE, PANEL_SIZE + GAP_SIZE + PADDING, PADDING) + np.random.uniform(0.1, 0.9, size=len(df))
# Create a color column with error handling
df['color'] = df['DEFECT_TYPE'].map(DEFECT_STYLE_MAP).fillna(DEFECT_STYLE_MAP['Unknown'])


# --- 4. Build the Plot (Simplified Method) ---
fig = go.Figure()

# --- THIS IS THE FIX ---
# Add all points in a single, robust trace.
fig.add_trace(go.Scatter(
    x=df['plot_x'],
    y=df['plot_y'],
    mode='markers',
    marker=dict(
        color=df['color'], # Pass the entire list of colors
        size=5,
        line=dict(width=0.5, color='black') # Add a thin border to dots
    ),
    hoverinfo='none' # We will add interactivity later if this works
))
# -----------------------

# Add shapes for panels and grids
shapes = []
panel_origins = [(PADDING, PADDING), (PADDING, PADDING + PANEL_SIZE + GAP_SIZE), (PADDING + PANEL_SIZE + GAP_SIZE, PADDING), (PADDING + PANEL_SIZE + GAP_SIZE, PADDING + PANEL_SIZE + GAP_SIZE)]
for x_start, y_start in panel_origins:
    shapes.append(dict(type='rect', x0=x_start, y0=y_start, x1=x_start+PANEL_SIZE, y1=y_start+PANEL_SIZE, line=dict(width=THICK_LINE_WIDTH, color=PANEL_BORDER_COLOR), fillcolor=PANEL_FILL_COLOR, layer='below'))
    for i in range(1, PANEL_SIZE):
        shapes.append(dict(type='line', x0=x_start+i, y0=y_start, x1=x_start+i, y1=y_start+PANEL_SIZE, line=dict(color="black", width=THIN_LINE_WIDTH), layer='below'))
        shapes.append(dict(type='line', x0=x_start, y0=y_start+i, x1=x_start+PANEL_SIZE, y1=y_start+i, line=dict(color="black", width=THIN_LINE_WIDTH), layer='below'))

# Style the layout
total_size = 2 * PADDING + 2 * PANEL_SIZE + GAP_SIZE
fig.update_layout(
    width=800, height=800,
    plot_bgcolor=BG_COLOR, paper_bgcolor=BG_COLOR,
    xaxis=dict(range=[0, total_size], visible=False),
    yaxis=dict(range=[0, total_size], visible=False, scaleanchor='x', scaleratio=1),
    shapes=shapes, margin=dict(l=0, r=0, t=40, b=0), showlegend=False
)

st.plotly_chart(fig)
