# app.py
# Final Version: Creates a 2x2 grid of panels with a visible gap,
# mimicking the target image exactly.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- 1. Page Configuration ---
st.set_page_config(page_title="Quad Panel Map", layout="centered")

# --- 2. Hardcoded Sample Data ---
# We will create defects across a 20x20 unit area to populate all quadrants
NUM_DEFECTS = 1000
GRID_SIZE_X = 20
GRID_SIZE_Y = 20

defect_types = ['Nick', 'Short', 'Missing Feature', 'Pad Violation', 'Other']

df = pd.DataFrame({
    'UNIT_INDEX_X': np.random.randint(0, GRID_SIZE_X, size=NUM_DEFECTS),
    'UNIT_INDEX_Y': np.random.randint(0, GRID_SIZE_Y, size=NUM_DEFECTS),
    'DEFECT_TYPE': np.random.choice(defect_types, size=NUM_DEFECTS)
})

# Define styles to match the target image
defect_style_map = {
    'Nick': 'magenta',
    'Short': 'deeppink',
    'Missing Feature': 'lime',
    'Pad Violation': 'white',
    'Other': 'red'
}
PANEL_COLOR = '#8B4513'  # SaddleBrown
BORDER_COLOR = '#556B2F' # DarkOliveGreen
GAP_COLOR = '#556B2F'    # DarkOliveGreen
BORDER_WIDTH = 5

# --- 3. Transform Coordinates to Create Gaps ---
PANEL_SIZE = 10  # Each quadrant is a 10x10 panel
GAP_SIZE = 1     # The size of the gap between panels

# Function to calculate the final plot coordinates
def transform_coords(df):
    plot_x = df['UNIT_INDEX_Y'] % PANEL_SIZE
    plot_y = df['UNIT_INDEX_X'] % PANEL_SIZE
    
    # Add offset for the top panels
    plot_y = plot_y + np.where(df['UNIT_INDEX_X'] >= PANEL_SIZE, PANEL_SIZE + GAP_SIZE, 0)
    # Add offset for the right panels
    plot_x = plot_x + np.where(df['UNIT_INDEX_Y'] >= PANEL_SIZE, PANEL_SIZE + GAP_SIZE, 0)
    
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
            marker=dict(color=color, size=6, line=dict(width=0.5, color='Black')),
            name=dtype, showlegend=False
        ))

# --- 5. Manually Draw the Panels and Grids ---
shapes = []
# Define the 4 panel boundaries
panel_coords = [
    (0, 0), (0, PANEL_SIZE + GAP_SIZE),
    (PANEL_SIZE + GAP_SIZE, 0), (PANEL_SIZE + GAP_SIZE, PANEL_SIZE + GAP_SIZE)
]

# Draw the thin inner grid lines for each panel
for x_start, y_start in panel_coords:
    for i in range(1, PANEL_SIZE):
        # Vertical lines
        shapes.append(dict(type='line', x0=x_start+i, y0=y_start, x1=x_start+i, y1=y_start+PANEL_SIZE-0.01, line=dict(color="black", width=0.5)))
        # Horizontal lines
        shapes.append(dict(type='line', x0=x_start, y0=y_start+i, x1=x_start+PANEL_SIZE-0.01, y1=y_start+i, line=dict(color="black", width=0.5)))

# --- 6. Style the Final Layout ---
total_size = 2 * PANEL_SIZE + GAP_SIZE
fig.update_layout(
    width=800, height=800,
    plot_bgcolor=PANEL_COLOR,
    paper_bgcolor=BORDER_COLOR, # Use paper background for the outer border
    xaxis=dict(range=[-0.5, total_size-0.5], showticklabels=False, showgrid=False, zeroline=False),
    yaxis=dict(range=[-0.5, total_size-0.5], showticklabels=False, showgrid=False, zeroline=False),
    shapes=shapes,
    margin=dict(l=20, r=20, t=20, b=20), # Margin for the outer border
    showlegend=False,
    yaxis_scaleanchor='x'
)

# --- 7. Display the plot in Streamlit ---
st.plotly_chart(fig)
