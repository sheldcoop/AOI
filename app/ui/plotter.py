# app/ui/plotter.py

import plotly.graph_objects as go
import pandas as pd
from itertools import cycle
# Import the centralized configuration
from app.config import PANEL_SIZE, GAP_SIZE, STYLE

def _create_dynamic_color_map(df: pd.DataFrame):
    """
    Generates a complete color map for all defect types present in the DataFrame.
    It uses the predefined map from the config and assigns new colors from the
    dynamic palette to any new defect types.
    """
    base_color_map = STYLE['defect_map'].copy()
    dynamic_palette = cycle(STYLE['dynamic_color_palette'])

    unique_defects = df['DEFECT_TYPE'].unique()

    final_color_map = {}
    for defect in unique_defects:
        if defect in base_color_map:
            final_color_map[defect] = base_color_map[defect]
        else:
            # If this new defect type has already been assigned a dynamic color, re-use it
            if defect not in final_color_map:
                 final_color_map[defect] = next(dynamic_palette)

    # If there are defects in the base map that are not in the data, add them for a consistent legend
    for defect, color in base_color_map.items():
        if defect not in final_color_map:
            final_color_map[defect] = color

    return final_color_map

def create_defect_map(df: pd.DataFrame):
    """
    Creates an interactive Plotly figure of the 2x2 defect map with dynamic colors.
    """
    TOTAL_SIZE = 2 * PANEL_SIZE + GAP_SIZE
    BG_COLOR, PANEL_COLOR, GRID_COLOR = STYLE['bg_color'], STYLE['panel_color'], STYLE['grid_color']

    # Generate the full color map for the current data
    color_map = _create_dynamic_color_map(df)
    df['color'] = df['DEFECT_TYPE'].map(color_map)

    fig = go.Figure()

    # --- Draw Panels and Grids ---
    shapes = []
    panel_origins = [(0, 0), (PANEL_SIZE + GAP_SIZE, 0), (0, PANEL_SIZE + GAP_SIZE), (PANEL_SIZE + GAP_SIZE, PANEL_SIZE + GAP_SIZE)]
    for x_start, y_start in panel_origins:
        shapes.append(go.layout.Shape(type="rect", x0=x_start, y0=y_start, x1=x_start + PANEL_SIZE, y1=y_start + PANEL_SIZE, fillcolor=PANEL_COLOR, line=dict(color=GRID_COLOR, width=3), layer="below"))
        for i in range(1, PANEL_SIZE):
            shapes.extend([
                go.layout.Shape(type="line", x0=x_start + i, y0=y_start, x1=x_start + i, y1=y_start + PANEL_SIZE, line=dict(color=GRID_COLOR, width=1), layer="below"),
                go.layout.Shape(type="line", x0=x_start, y0=y_start + i, x1=x_start + PANEL_SIZE, y1=y_start + i, line=dict(color=GRID_COLOR, width=1), layer="below")
            ])

    # --- Plot Defects (Single Trace) ---
    fig.add_trace(go.Scatter(
        x=df['plot_x'], y=df['plot_y'], mode='markers',
        marker=dict(color=df['color'], size=8, line=dict(width=1, color='black')),
        showlegend=False, customdata=df.to_numpy(),
        hovertemplate="<b>%{customdata[1]}</b><br>Defect ID: %{customdata[0]}<br>Click for details<extra></extra>"
    ))

    # --- Manually Create Legend ---
    # Sort the legend alphabetically for consistency
    sorted_legend_items = sorted(color_map.items())
    for dtype, color in sorted_legend_items:
        # Only add to legend if the defect type is present in the data or was in the original base map
        if dtype in df['DEFECT_TYPE'].unique() or dtype in STYLE['defect_map']:
             fig.add_trace(go.Scatter(
                x=[None], y=[None], mode='markers',
                marker=dict(color=color, size=10, line=dict(width=1, color='black')),
                name=dtype, showlegend=True
            ))

    # --- Final Layout Styling ---
    fig.update_layout(
        width=800, height=800,
        plot_bgcolor=BG_COLOR, paper_bgcolor=BG_COLOR,
        xaxis=dict(visible=False, range=[-1, TOTAL_SIZE + 1]),
        yaxis=dict(visible=False, range=[-1, TOTAL_SIZE + 1], scaleanchor="x", scaleratio=1),
        shapes=shapes,
        legend=dict(title="Defect Types", itemsizing='constant', bgcolor="rgba(255, 255, 255, 0.5)")
    )

    return fig
