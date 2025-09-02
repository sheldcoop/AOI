# app.py
# A simple, static Streamlit app to display a defect map.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- 1. Page Configuration ---
st.set_page_config(page_title="Defect Panel Map", layout="centered")
st.title("Interactive Panel Defect Map")

# --- 2. Hardcoded Sample Data ---
# We create some sample data to ensure the plot is populated.
NUM_DEFECTS = 80
GRID_SIZE_X = 7
GRID_SIZE_Y = 7

defect_types = [
    'Nick', 'Short', 'Missing Feature', 'Cut', 'Fine Short',
    'Pad Violation', 'Island', 'Cut/Short', 'Nick/Protrusion'
]

df = pd.DataFrame({
    'UNIT_INDEX_X': np.random.randint(0, GRID_SIZE_X, size=NUM_DEFECTS),
    'UNIT_INDEX_Y': np.random.randint(0, GRID_SIZE_Y, size=NUM_DEFECTS),
    'DEFECT_TYPE': np.random.choice(defect_types, size=NUM_DEFECTS)
})

# --- 3. Create the Plotly Visualization ---
fig = go.Figure()

# Define the styles for the plot
defect_style_map = {
    'Nick': 'magenta', 'Short': 'red', 'Missing Feature': 'lime', 'Cut': 'cyan',
    'Fine Short': '#DDA0DD', 'Pad Violation': 'white', 'Island': 'orange',
    'Cut/Short': '#00BFFF', 'Nick/Protrusion': 'yellow'
}
PLOT_BG_COLOR = '#F4A460' # SandyBrown color

# Add jittered coordinates so points in the same cell don't overlap
np.random.seed(42)
df['plot_x'] = df['UNIT_INDEX_Y'] + np.random.uniform(0.15, 0.85, size=len(df))
df['plot_y'] = df['UNIT_INDEX_X'] + np.random.uniform(0.15, 0.85, size=len(df))

# Add a trace for each defect type
for dtype, color in defect_style_map.items():
    dff = df[df['DEFECT_TYPE'] == dtype]
    if not dff.empty:
        fig.add_trace(go.Scatter(
            x=dff['plot_x'], y=dff['plot_y'], mode='markers',
            marker=dict(color=color, size=12, line=dict(width=1.5, color='Black')),
            name=dtype,
        ))

# Add thick grid lines
shapes = []
for i in range(GRID_SIZE_Y + 1):
    shapes.append(dict(type='line', x0=i-0.5, y0=-0.5, x1=i-0.5, y1=GRID_SIZE_X-0.5, line=dict(color='black', width=4)))
for i in range(GRID_SIZE_X + 1):
    shapes.append(dict(type='line', x0=-0.5, y0=i-0.5, x1=GRID_SIZE_Y-0.5, y1=i-0.5, line=dict(color='black', width=4)))

# Style the layout to match your image
fig.update_layout(
    xaxis_title='Unit Column Index (Y)',
    yaxis_title='Unit Row Index (X)',
    plot_bgcolor=PLOT_BG_COLOR,
    shapes=shapes,
    width=800, 
    height=800,
    xaxis=dict(range=[-1, GRID_SIZE_Y], tickvals=np.arange(0, GRID_SIZE_Y)),
    yaxis=dict(range=[-1, GRID_SIZE_X], tickvals=np.arange(0, GRID_SIZE_X)),
    legend_title_text='Defect Types',
    yaxis_scaleanchor='x'
)

# --- 4. Display the plot in Streamlit ---
st.plotly_chart(fig)
