# app.py
# Final Version: Enforces a square aspect ratio for perfect symmetrical padding.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- 1. Page Configuration ---
st.set_page_config(page_title="Quad Panel Defect Map", layout="wide")

# --- 2. Hardcoded Sample Data ---
NUM_DEFECTS = 400
GRID_SIZE = 14
PANEL_SIZE = 7

defect_types = ['Nick', 'Short', 'Missing Feature', 'Pad Violation', 'Other']
df = pd.DataFrame({
    'UNIT_INDEX_X': np.random.randint(0, GRID_SIZE, size=NUM_DEFECTS),
    'UNIT_INDEX_Y': np.random.randint(0, GRID_SIZE, size=NUM_DEFECTS),
    'DEFECT_TYPE': np.random.choice(defect_types, size=NUM_DEFECTS)
})

defect_style_map = {
    'Nick': 'magenta', 'Short': 'deeppink', 'Missing Feature': 'lime',
    'Pad Violation': 'white', 'Other': 'red'
}
PANEL_COLOR = '#8B4513'
BG_COLOR = '#556B2F'

# --- 3. Transform Coordinates to Create Gaps ---
GAP_SIZE = 1

def transform_coords(df):
    plot_x = df['UNIT_INDEX_Y'] % PANEL_SIZE
    plot_y = df['UNIT_INDEX_X'] % PANEL_SIZE
    plot_y += np.where(df['UNIT_INDEX_X'] >= PANEL_SIZE, PANEL_SIZE + GAP_SIZE, 0)
    plot_x += np.where(df['UNIT_INDEX_Y'] >= PANEL_SIZE, PANEL_SIZE + GAP_SIZE, 0)
    df['plot_x'] = plot_x + np.random.uniform(0.1, 0.9, size=len(df))
    df['plot_y'] = plot_y + np.random.uniform(0.1, 0.9, size=len(df))
    return df

df = transform_coords(df)

# --- 4. Create a Single Plotly Figure ---
fig = go.Figure()

# Add defect traces
for dtype, color in defect_style_map.items():
    dff = df[df['DEFECT_TYPE'] == dtype]
    if not dff.empty:
        fig.add_trace(go.Scatter(
            x=dff['plot_x'], y=dff['plot_y'], mode='markers',
            marker=dict(color=color, size=8, line=dict(width=0)),
            name=dtype, showlegend=False
        ))

# --- 5. Manually Draw the Panels, Borders, and Grids ---
shapes = []
panel_coords = [
    (0, 0), (0, PANEL_SIZE + GAP_SIZE),
    (PANEL_SIZE + GAP_SIZE, 0), (PANEL_SIZE + GAP_SIZE, PANEL_SIZE + GAP_SIZE)
]
THIN_LINE_WIDTH = 1
THICK_LINE_WIDTH = 4

for x_start, y_start in panel_coords:
    shapes.append(dict(type='rect', x0=x_start-0.5, y0=y_start-0.5, x1=x_start+PANEL_SIZE-0.5, y1=y_start+PANEL_SIZE-0.5,
                      line=dict(color="black", width=THICK_LINE_WIDTH), fillcolor=PANEL_COLOR, layer='below'))
    for i in range(1, PANEL_SIZE):
        shapes.append(dict(type='line', x0=x_start+i-0.5, y0=y_start-0.5, x1=x_start+i-0.5, y1=y_start+PANEL_SIZE-0.5,
                          line=dict(color="black", width=THIN_LINE_WIDTH), layer='below'))
        shapes.append(dict(type='line', x0=x_start-0.5, y0=y_start+i-0.5, x1=x_start+PANEL_SIZE-0.5, y1=y_start+i-0.5,
                          line=dict(color="black", width=THIN_LINE_WIDTH), layer='below'))

# --- 6. Style the Final Layout with Symmetrical Padding ---
total_plot_width = PANEL_SIZE + GAP_SIZE
axis_start = -0.5 - (GAP_SIZE / 2)
axis_end = total_plot_width - 0.5 + (GAP_SIZE / 2)

fig.update_layout(
    # --- THIS IS THE FIX for perfect symmetry ---
    # We set width and height to be equal to enforce a square plot
    width=1000, 
    height=1000,
    # -----------------------------------------------
    plot_bgcolor=BG_COLOR,
    paper_bgcolor=BG_COLOR,
    xaxis=dict(range=[axis_start, axis_end], visible=False),
    yaxis=dict(range=[axis_start, axis_end], visible=False, scaleanchor='x', scaleratio=1),
    shapes=shapes,
    margin=dict(l=0, r=0, t=0, b=0),
    showlegend=False
)

# --- 7. Display the plot in Streamlit ---
st.plotly_chart(fig)
