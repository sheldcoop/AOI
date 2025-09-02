# app.py
# Final version: Displays a single, wide plot with two gapped grids.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- 1. Page Configuration ---
st.set_page_config(page_title="Dual Panel Defect Map", layout="wide")
st.title("Interactive Dual Panel Defect Map")

# --- 2. Hardcoded Sample Data for a Wider Panel ---
NUM_DEFECTS = 150
GRID_SIZE_X = 7
GRID_SIZE_Y = 14

defect_types = [
    'Nick', 'Short', 'Missing Feature', 'Cut', 'Fine Short',
    'Pad Violation', 'Island', 'Cut/Short', 'Nick/Protrusion'
]

df = pd.DataFrame({
    'UNIT_INDEX_X': np.random.randint(0, GRID_SIZE_X, size=NUM_DEFECTS),
    'UNIT_INDEX_Y': np.random.randint(0, GRID_SIZE_Y, size=NUM_DEFECTS),
    'DEFECT_TYPE': np.random.choice(defect_types, size=NUM_DEFECTS)
})

defect_style_map = {
    'Nick': 'magenta', 'Short': 'red', 'Missing Feature': 'lime', 'Cut': 'cyan',
    'Fine Short': '#DDA0DD', 'Pad Violation': 'white', 'Island': 'orange',
    'Cut/Short': '#00BFFF', 'Nick/Protrusion': 'yellow'
}
PLOT_BG_COLOR = '#F4A460'

# Add jittered coordinates. We need to create a gap in the x-coordinates for the plot.
# Defects in the second panel (cols 7-13) get a +1 offset for their plot_x.
gap_size = 1
df['plot_x'] = df['UNIT_INDEX_Y'] + np.where(df['UNIT_INDEX_Y'] >= 7, gap_size, 0) + np.random.uniform(0.15, 0.85, size=len(df))
df['plot_y'] = df['UNIT_INDEX_X'] + np.random.uniform(0.15, 0.85, size=len(df))

# --- 3. Create a Single Plotly Figure ---
fig = go.Figure()

# Add all defects to the single figure
for dtype, color in defect_style_map.items():
    dff = df[df['DEFECT_TYPE'] == dtype]
    if not dff.empty:
        fig.add_trace(go.Scatter(
            x=dff['plot_x'], y=dff['plot_y'], mode='markers',
            marker=dict(color=color, size=12, line=dict(width=1.5, color='Black')),
            name=dtype,
        ))

# --- 4. Draw Both Grids with a Gap ---
shapes = []
# Grid 1 (Cols 0-6)
for i in range(7 + 1): # Vertical lines
    shapes.append(dict(type='line', x0=i-0.5, y0=-0.5, x1=i-0.5, y1=GRID_SIZE_X-0.5, line=dict(color='black', width=4), layer='below'))
for i in range(GRID_SIZE_X + 1): # Horizontal lines
    shapes.append(dict(type='line', x0=-0.5, y0=i-0.5, x1=6.5, y1=i-0.5, line=dict(color='black', width=4), layer='below'))

# Grid 2 (Cols 7-13)
for i in range(7 + 1): # Vertical lines
    shapes.append(dict(type='line', x0=i+7+gap_size-0.5, y0=-0.5, x1=i+7+gap_size-0.5, y1=GRID_SIZE_X-0.5, line=dict(color='black', width=4), layer='below'))
for i in range(GRID_SIZE_X + 1): # Horizontal lines
    shapes.append(dict(type='line', x0=7+gap_size-0.5, y0=i-0.5, x1=13+gap_size+0.5, y1=i-0.5, line=dict(color='black', width=4), layer='below'))
    
# --- 5. Style the Layout ---
fig.update_layout(
    plot_bgcolor=PLOT_BG_COLOR,
    shapes=shapes,
    width=1400, 
    height=800,
    xaxis_title='Unit Column Index (Y)',
    yaxis_title='Unit Row Index (X)',
    # Set the axis to show original labels despite the gap
    xaxis=dict(
        tickvals=np.concatenate([np.arange(0, 7), np.arange(7, 14)]) + np.where(np.arange(0, 14) >= 7, gap_size, 0) + 0.5,
        ticktext=np.arange(0, 14)
    ),
    yaxis=dict(range=[-0.5, GRID_SIZE_X-0.5], tickvals=np.arange(0, GRID_SIZE_X)),
    legend_title_text='Defect Types',
    yaxis_scaleanchor='x'
)

# --- 6. Display the plot in Streamlit ---
st.plotly_chart(fig, use_container_width=True)
