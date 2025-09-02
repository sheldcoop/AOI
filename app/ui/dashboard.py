# app/ui/dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
from app.utils.config import DEFECT_STYLE_MAP, PLOT_BG_COLOR

def display_welcome_message():
    """Displays the initial welcome message and instructions."""
    st.header("Welcome to Defect-Viz")
    st.markdown(
        "An interactive tool for visualizing manufacturing panel defects. "
        "To begin, please **upload your defect Excel file** using the sidebar on the left."
    )
    st.info("Once your data is loaded, the interactive panel map will appear here.")

def create_panel_map(df: pd.DataFrame) -> go.Figure:
    """Creates the interactive Plotly figure for the panel map."""
    
    # Add jitter for better visualization of overlapping points
    np.random.seed(42)
    df['plot_x'] = df['UNIT_INDEX_Y'] + np.random.uniform(0.15, 0.85, size=len(df))
    df['plot_y'] = df['UNIT_INDEX_X'] + np.random.uniform(0.15, 0.85, size=len(df))

    fig = go.Figure()

    # Add a trace for each defect type for a clean legend
    for dtype, color in DEFECT_STYLE_MAP.items():
        dff = df[df['DEFECT_TYPE'] == dtype]
        if not dff.empty:
            fig.add_trace(go.Scatter(
                x=dff['plot_x'], y=dff['plot_y'],
                mode='markers',
                marker=dict(color=color, size=12, line=dict(width=1.5, color='Black')),
                name=dtype,
                # We pass the original DataFrame index to identify the point on click
                customdata=dff.index,
                hoverinfo='none'
            ))

    # Determine grid size from data
    grid_size_x = int(df['UNIT_INDEX_X'].max() + 1)
    grid_size_y = int(df['UNIT_INDEX_Y'].max() + 1)
    
    # Create thick grid lines
    shapes = []
    for i in range(grid_size_y + 1):
        shapes.append(dict(type='line', x0=i-0.5, y0=-0.5, x1=i-0.5, y1=grid_size_x-0.5, line=dict(color='black', width=4)))
    for i in range(grid_size_x + 1):
        shapes.append(dict(type='line', x0=-0.5, y0=i-0.5, x1=grid_size_y-0.5, y1=i-0.5, line=dict(color='black', width=4)))

    fig.update_layout(
        title_text='Interactive Panel Defect Map (Click a defect to view details)',
        xaxis_title='Unit Column Index (Y)',
        yaxis_title='Unit Row Index (X)',
        plot_bgcolor=PLOT_BG_COLOR,
        shapes=shapes,
        width=800, height=800,
        xaxis=dict(range=[-1, grid_size_y], tickvals=np.arange(0, grid_size_y)),
        yaxis=dict(range=[-1, grid_size_x], tickvals=np.arange(0, grid_size_x)),
        yaxis_scaleanchor='x',
        legend_title_text='Defect Types'
    )
    return fig

def display_dashboard(df: pd.DataFrame):
    """Builds the main dashboard layout with the plot and details panel."""
    
    # Create the plot
    fig = create_panel_map(df)
    
    # Create a two-column layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Display the plot and capture click events
        selected_points = plotly_events(fig, click_event=True, key="plot_click")
    
    with col2:
        st.subheader("Selected Defect Details")
        # This is where the image and data will be displayed
        details_placeholder = st.empty()

    # Handle the click event
    if selected_points:
        # Get the index of the first clicked point
        point_index = selected_points[0]['customdata']
        defect_info = df.loc[point_index]

        with details_placeholder.container():
            st.markdown(f"**Defect ID:** `{defect_info['DEFECT_ID']}`")
            st.markdown(f"**Defect Type:** `{defect_info['DEFECT_TYPE']}`")
            st.markdown(f"**Unit (Row, Col):** `({defect_info['UNIT_INDEX_X']}, {defect_info['UNIT_INDEX_Y']})`")
            st.markdown(f"**Coordinates (X, Y):** `({defect_info['X_COORDINATES']}, {defect_info['Y_COORDINATES']})`")
            st.markdown("---")
            
            # Display both modality images
            if 'image_path_mod1' in df.columns and os.path.exists(defect_info['image_path_mod1']):
                st.image(defect_info['image_path_mod1'], caption="Modality 1")
            
            if 'image_path_mod2' in df.columns and os.path.exists(defect_info['image_path_mod2']):
                st.image(defect_info['image_path_mod2'], caption="Modality 2")
    else:
        details_placeholder.info("Click on a defect in the map to see its details and images.")
