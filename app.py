# app.py
# Final Version: Creates a single 14x14 grid with thick central quadrant lines.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- 1. Page Configuration ---
st.set_page_config(page_title="Quadrant Defect Map", layout="wide")
st.title("Quadrant Panel Defect Map")

# --- 2. Hardcoded Sample Data for a 14x14 Panel ---
NUM_DEFECTS = 300
GRID_SIZE = 14 # 14 rows and 14 columns (indices 0-13)

defect_types = [
    'Nick', 'Short', 'Missing Feature', 'Cut', 'Fine Short',
    'Pad Violation', 'Island', 'Cut/Short', 'Nick/Protrusion'
]

df = pd.DataFrame({
    'UNIT_INDEX_X': np.random.randint(0, GRID_SIZE, size=NUM_DEFECTS),
    'UNIT_INDEX_Y': np.random.randint(0, GRID_SIZE, size=NUM_DEFECTS),
    'DEFECT_TYPE': np.random.choice(defect_types, size=NUM_DEFECTS)
})

defect_style_map = {
    'Nick': 'magenta', 'Short': 'red', 'Missing Feature': 'lime', 'Cut': 'cyan',
    'Fine Short': '#DDA0DD', 'Pad Violation': 'white', 'Island': 'orange',
    'Cut/Short': '#00BFFF', 'Nick/Protrusion': 'yellow'
}
PLOT_BG_COLOR = '#8B4513' # SaddleBrown, to match your target image

# Add jittered coordinates for plotting
np.random.seed(42)
df['plot_x'] = df['UNIT_INDEX_Y'] + np.random.uniform(0.15, 0.85, size=len(df))
df['plot_y'] = df['UNIT_INDEX_X'] + np.random.uniform(0.15, 0.85, size=len(df))

# --- 3. Create a Single Plotly Figure ---
fig = go.Figure()

# Add all defects to the single figure
for dtype, color in defect_style_map.items():
    dff = df[df['DEFECT_TYPE'] == dtype]
    if not dff.empty:
        fig.add_trace(go.Scatter(
            x=dff['plot_x'], y=dff['plot_y'], mode='markers',
            marker=dict(color=color, size=10, line=dict(width=1, color='Black')),
            name=dtype,
        ))

# --- 4. Draw Grid with Variable Thickness Lines ---
shapes = []
THIN_LINE_WIDTH = 2
THICK_LINE_WIDTH = 5

# Draw all horizontal and vertical lines
for i in range(GRID_SIZE + 1):
    # Determine line thickness
    h_width = THICK_LINE_WIDTH if i in [0, 7, 14] else THIN_LINE_WIDTH
    v_width = THICK_LINE_WIDTH if i in [0, 7, 14] else THIN_LINE_WIDTH
    
    # Horizontal lines
    shapes.append(dict(type='line', x0=-0.5, y0=i-0.5, x1=GRID_SIZE-0.5, y1=i-0.5,
                      line=dict(color="Black", width=h_width), layer='below'))
    # Vertical lines
    shapes.append(dict(type='line', x0=i-0.5, y0=-0.5, x1=i-0.5, y1=GRID_SIZE-0.5,
                      line=dict(color="Black", width=v_width), layer='below'))

# --- 5. Style the Final Layout ---
fig.update_layout(
    plot_bgcolor=PLOT_BG_COLOR,
    shapes=shapes,
    width=900, 
    height=900,
    xaxis_title='Unit Column Index (Y)',
    yaxis_title='Unit Row Index (X)',
    # Set axis ranges to perfectly frame the grid
    xaxis=dict(range=[-0.5, GRID_SIZE-0.5], tickvals=np.arange(0, GRID_SIZE), showgrid=False),
    yaxis=dict(range=[-0.5, GRID_SIZE-0.5], tickvals=np.arange(0, GRID_SIZE), showgrid=False),
    legend_title_text='Defect Types',
    yaxis_scaleanchor='x'
)

# --- 6. Display the plot in Streamlit ---
st.plotly_chart(fig)
