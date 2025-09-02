# app.py
# A simple, single-file Streamlit app to display a fabricated defect map.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="Defect Panel Map", layout="centered")

st.title("Interactive Panel Defect Map")

# --- 1. Fabricate Defect Data ---
# This section is identical to your Colab code.
NUM_DEFECTS = 75 # Increased for a fuller-looking map
GRID_SIZE_X = 7  # 7 rows
GRID_SIZE_Y = 7  # 7 columns

defect_types = [
    'Nick', 'Short', 'Missing Feature', 'Cut', 'Fine Short',
    'Pad Violation', 'Island', 'Cut/Short', 'Nick/Protrusion'
]

fabricated_data = {
    'DEFECT_ID': list(range(1, NUM_DEFECTS + 1)),
    'UNIT_INDEX_X': np.random.randint(0, GRID_SIZE_X, size=NUM_DEFECTS),
    'UNIT_INDEX_Y': np.random.randint(0, GRID_SIZE_Y, size=NUM_DEFECTS),
    'DEFECT_TYPE': np.random.choice(defect_types, size=NUM_DEFECTS)
}
df = pd.DataFrame(fabricated_data)

# --- 2. Define Defect Styles ---
defect_style_map = {
    'Nick': 'magenta', 'Short': 'red', 'Missing Feature': 'lime', 'Cut': 'cyan',
    'Fine Short': '#DDA0DD', 'Pad Violation': 'white', 'Island': 'orange',
    'Cut/Short': '#00BFFF', 'Nick/Protrusion': 'yellow'
}

# --- 3. Add Jittered Coordinates for Plotting ---
np.random.seed(42)
df['plot_x'] = df['UNIT_INDEX_Y'] + np.random.uniform(0.15, 0.85, size=NUM_DEFECTS)
df['plot_y'] = df['UNIT_INDEX_X'] + np.random.uniform(0.15, 0.85, size=NUM_DEFECTS)

# --- 4. Create the Interactive Plotly Visualization ---
fig = go.Figure()

# Add a separate trace for each defect type for a clean legend
for dtype, color in defect_style_map.items():
    dff = df[df['DEFECT_TYPE'] == dtype]
    if not dff.empty:
        fig.add_trace(go.Scatter(
            x=dff['plot_x'], y=dff['plot_y'], mode='markers',
            marker=dict(color=color, size=12, line=dict(width=1.5, color='Black')),
            name=dtype,
            hoverinfo='text',
            hovertext=[f"ID: {row['DEFECT_ID']}<br>Type: {row['DEFECT_TYPE']}" for index, row in dff.iterrows()]
        ))

# --- 5. Add Grid Lines and Style the Layout ---
shapes = []
for i in range(GRID_SIZE_Y + 1):
    shapes.append(dict(type='line', x0=i-0.5, y0=-0.5, x1=i-0.5, y1=GRID_SIZE_X-0.5, line=dict(color='black', width=4)))
for i in range(GRID_SIZE_X + 1):
    shapes.append(dict(type='line', x0=-0.5, y0=i-0.5, x1=GRID_SIZE_Y-0.5, y1=i-0.5, line=dict(color='black', width=4)))

fig.update_layout(
    xaxis_title='Unit Column Index (Y)',
    yaxis_title='Unit Row Index (X)',
    plot_bgcolor='#F4A460', # SandyBrown color
    shapes=shapes,
    width=700, height=700,
    xaxis=dict(range=[-0.5, GRID_SIZE_Y-0.5], tickvals=np.arange(0, GRID_SIZE_Y), showgrid=False, zeroline=False),
    yaxis=dict(range=[-0.5, GRID_SIZE_X-0.5], tickvals=np.arange(0, GRID_SIZE_X), showgrid=False, zeroline=False),
    legend_title_text='Defect Types',
    yaxis_scaleanchor='x'
)

# --- 6. Display the plot in Streamlit ---
st.plotly_chart(fig)
