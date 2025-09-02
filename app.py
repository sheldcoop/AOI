# app.py
# Final Version: Creates a 2x2 grid of 7x7 panels.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. Page Configuration ---
st.set_page_config(page_title="Quad Panel Defect Map", layout="wide")
st.title("Interactive Quad Panel Defect Map")

# --- 2. Hardcoded Sample Data for a 14x14 Panel ---
NUM_DEFECTS = 300
GRID_SIZE_X = 14 # 14 rows (0-13)
GRID_SIZE_Y = 14 # 14 columns (0-13)

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

# Add jittered coordinates
np.random.seed(42)
df['plot_x'] = df['UNIT_INDEX_Y'] + np.random.uniform(0.15, 0.85, size=len(df))
df['plot_y'] = df['UNIT_INDEX_X'] + np.random.uniform(0.15, 0.85, size=len(df))

# --- 3. Create the 2x2 Subplot Figure ---
fig = make_subplots(rows=2, cols=2,
                    shared_xaxes=True, shared_yaxes=True,
                    horizontal_spacing=0.03, vertical_spacing=0.03)

# --- 4. Function to Add Traces and Shapes for one Panel ---
def add_panel_to_fig(fig, dataframe, row_start, col_start, subplot_row, subplot_col):
    # Filter data for this specific panel
    panel_df = dataframe[
        (dataframe['UNIT_INDEX_X'] >= row_start) & (dataframe['UNIT_INDEX_X'] < row_start + 7) &
        (dataframe['UNIT_INDEX_Y'] >= col_start) & (dataframe['UNIT_INDEX_Y'] < col_start + 7)
    ]

    # Add traces for defects
    for dtype, color in defect_style_map.items():
        dff = panel_df[panel_df['DEFECT_TYPE'] == dtype]
        if not dff.empty:
            fig.add_trace(go.Scatter(
                x=dff['plot_x'], y=dff['plot_y'], mode='markers',
                marker=dict(color=color, size=10, line=dict(width=1.5, color='Black')),
                name=dtype,
                legendgroup=dtype, # Group legends so they only appear once
                showlegend=(subplot_row==1 and subplot_col==1)
            ), row=subplot_row, col=subplot_col)

    # Add shapes for the grid
    for i in range(8): # 8 vertical lines for a 7-unit grid
        fig.add_shape(type="line", x0=i+col_start-0.5, y0=row_start-0.5, x1=i+col_start-0.5, y1=row_start+6.5,
                      line=dict(color="Black", width=3), row=subplot_row, col=subplot_col)
    for i in range(8): # 8 horizontal lines
        fig.add_shape(type="line", x0=col_start-0.5, y0=i+row_start-0.5, x1=col_start+6.5, y1=i+row_start-0.5,
                      line=dict(color="Black", width=3), row=subplot_row, col=subplot_col)

# --- 5. Add All Four Panels to the Figure ---
add_panel_to_fig(fig, df, 7, 0, subplot_row=1, subplot_col=1)   # Top-Left
add_panel_to_fig(fig, df, 7, 7, subplot_row=1, subplot_col=2)   # Top-Right
add_panel_to_fig(fig, df, 0, 0, subplot_row=2, subplot_col=1)   # Bottom-Left
add_panel_to_fig(fig, df, 0, 7, subplot_row=2, subplot_col=2)   # Bottom-Right

# --- 6. Update the Final Layout ---
fig.update_layout(
    plot_bgcolor=PLOT_BG_COLOR,
    width=1200, height=1200,
    legend_title_text='Defect Types',
    # --- THIS IS THE FIX for the white grid lines ---
    xaxis_showgrid=False, yaxis_showgrid=False,
    xaxis2_showgrid=False, yaxis2_showgrid=False,
    xaxis3_showgrid=False, yaxis3_showgrid=False,
    xaxis4_showgrid=False, yaxis4_showgrid=False
)

# Update axis properties for all subplots
fig.update_xaxes(tickvals=np.arange(0, 14), range=[-0.5, 13.5])
fig.update_yaxes(tickvals=np.arange(0, 14), range=[-0.5, 13.5], scaleanchor='x', scaleratio=1)

# --- 7. Display the plot in Streamlit ---
st.plotly_chart(fig, use_container_width=True)
