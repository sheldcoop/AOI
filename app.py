# app.py
# Final Version: Creates a large 2x2 layout of four distinct, bordered 7x7 panels.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- 1. Page Configuration ---
st.set_page_config(page_title="Quad Panel Defect Map", layout="wide")

# --- 2. Hardcoded Sample Data ---
# Data is generated for a 14x14 area to populate all four 7x7 quadrants
NUM_DEFECTS = 400
GRID_SIZE = 14

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
PANEL_COLOR = '#8B4513'  # SaddleBrown
BG_COLOR = '#556B2F'     # DarkOliveGreen

# --- 3. Transform Coordinates to Create Gaps ---
PANEL_SIZE = 7   # Each quadrant is a 7x7 panel
GAP_SIZE = 1     # The size of the gap between panels

def transform_coords(df):
    plot_x = df['UNIT_INDEX_Y'] % PANEL_SIZE
    plot_y = df['UNIT_INDEX_X'] % PANEL_SIZE
    
    # Add offset for the top panels (rows >= 7)
    plot_y += np.where(df['UNIT_INDEX_X'] >= PANEL_SIZE, PANEL_SIZE + GAP_SIZE, 0)
    # Add offset for the right panels (cols >= 7)
    plot_x += np.where(df['UNIT_INDEX_Y'] >= PANEL_SIZE, PANEL_SIZE + GAP_SIZE, 0)
    
    # Add random jitter within the cell
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
            marker=dict(color=color, size=8, line=dict(width=0)), # No border on dots
            name=dtype, showlegend=False
        ))

# --- 5. Manually Draw the Panels, Borders, and Grids ---
shapes = []
# Define the 4 panel starting coordinates (top-left corner of each)
panel_coords = [
    (0, 0), (0, PANEL_SIZE + GAP_SIZE),
    (PANEL_SIZE + GAP_SIZE, 0), (PANEL_SIZE + GAP_SIZE, PANEL_SIZE + GAP_SIZE)
]

THIN_LINE_WIDTH = 1
THICK_LINE_WIDTH = 4

for x_start, y_start in panel_coords:
    # Draw the thick outer border for this panel
    shapes.append(dict(type='rect', x0=x_start-0.5, y0=y_start-0.5, x1=x_start+PANEL_SIZE-0.5, y1=y_start+PANEL_SIZE-0.5,
                      line=dict(color="black", width=THICK_LINE_WIDTH), fillcolor=PANEL_COLOR, layer='below'))
    
    # Draw the thin inner grid lines
    for i in range(1, PANEL_SIZE):
        # Vertical lines
        shapes.append(dict(type='line', x0=x_start+i-0.5, y0=y_start-0.5, x1=x_start+i-0.5, y1=y_start+PANEL_SIZE-0.5,
                          line=dict(color="black", width=THIN_LINE_WIDTH), layer='below'))
        # Horizontal lines
        shapes.append(dict(type='line', x0=x_start-0.5, y0=y_start+i-0.5, x1=x_start+PANEL_SIZE-0.5, y1=y_start+i-0.5,
                          line=dict(color="black", width=THIN_LINE_WIDTH), layer='below'))

# --- 6. Style the Final Layout ---
total_size = 2 * PANEL_SIZE + GAP_SIZE
fig.update_layout(
    width=1200, height=1200,
    plot_bgcolor=BG_COLOR,
    paper_bgcolor=BG_COLOR,
    xaxis=dict(range=[-1.5, total_size-0.5], visible=False),
    yaxis=dict(range=[-1.5, total_size-0.5], visible=False),
    shapes=shapes,
    margin=dict(l=10, r=10, t=10, b=10),
    showlegend=False,
    yaxis_scaleanchor='x'
)

# --- 7. Display the plot in Streamlit ---
st.plotly_chart(fig)
