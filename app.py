# app.py
# Final version: Displays a two-panel defect map with correct visual layering.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- 1. Page Configuration ---
st.set_page_config(page_title="Dual Panel Defect Map", layout="wide")
st.title("Interactive Dual Panel Defect Map")

# --- 2. Hardcoded Sample Data for a Wider Panel ---
NUM_DEFECTS = 150
GRID_SIZE_X = 7  # 7 rows
GRID_SIZE_Y = 14 # 14 columns (0 through 13)

defect_types = [
    'Nick', 'Short', 'Missing Feature', 'Cut', 'Fine Short',
    'Pad Violation', 'Island', 'Cut/Short', 'Nick/Protrusion'
]

df = pd.DataFrame({
    'UNIT_INDEX_X': np.random.randint(0, GRID_SIZE_X, size=NUM_DEFECTS),
    'UNIT_INDEX_Y': np.random.randint(0, GRID_SIZE_Y, size=NUM_DEFECTS),
    'DEFECT_TYPE': np.random.choice(defect_types, size=NUM_DEFECTS)
})

# Define the styles for the plot
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

# --- 3. Create the Two-Column Layout ---
col1, col2 = st.columns(2)

# --- 4. Function to Create a Single Panel Plot ---
def create_panel_plot(dataframe, col_start, col_end, title):
    fig = go.Figure()
    
    # Filter the dataframe for the specified column range
    panel_df = dataframe[(dataframe['UNIT_INDEX_Y'] >= col_start) & (dataframe['UNIT_INDEX_Y'] < col_end)]
    
    # Add a trace for each defect type
    for dtype, color in defect_style_map.items():
        dff = panel_df[panel_df['DEFECT_TYPE'] == dtype]
        if not dff.empty:
            fig.add_trace(go.Scatter(
                x=dff['plot_x'], y=dff['plot_y'], mode='markers',
                marker=dict(color=color, size=12, line=dict(width=1.5, color='Black')),
                name=dtype, showlegend=(col_start==0) # Only show legend on the first plot
            ))

    # Add thick grid lines
    shapes = []
    num_cols = col_end - col_start
    for i in range(num_cols + 1):
        shapes.append(dict(type='line', x0=i+col_start-0.5, y0=-0.5, x1=i+col_start-0.5, y1=GRID_SIZE_X-0.5, line=dict(color='black', width=4)))
    for i in range(GRID_SIZE_X + 1):
        shapes.append(dict(type='line', x0=col_start-0.5, y0=i-0.5, x1=col_end-0.5, y1=i-0.5, line=dict(color='black', width=4)))

    # Style the layout
    fig.update_layout(
        title=title,
        xaxis_title='Unit Column Index (Y)',
        yaxis_title='Unit Row Index (X)' if col_start == 0 else '', # Only show Y axis title on first plot
        plot_bgcolor=PLOT_BG_COLOR,
        shapes=shapes,
        width=700, height=700,
        xaxis=dict(range=[col_start-0.5, col_end-0.5], tickvals=np.arange(col_start, col_end)),
        yaxis=dict(range=[-0.5, GRID_SIZE_X-0.5], tickvals=np.arange(0, GRID_SIZE_X)),
        legend_title_text='Defect Types',
        yaxis_scaleanchor='x',
        # --- THIS IS THE FIX for the layering issue ---
        shapes_layer='below' 
    )
    return fig

# --- 5. Display the Plots in the Columns ---
with col1:
    st.plotly_chart(create_panel_plot(df, 0, 7, "Panel 1 (Cols 0-6)"))

with col2:
    st.plotly_chart(create_panel_plot(df, 7, 14, "Panel 2 (Cols 7-13)"))
