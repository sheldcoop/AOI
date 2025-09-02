# app/ui/plotter.py

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd

def create_defect_map(df: pd.DataFrame):
    """
    Creates a static Matplotlib figure of the 2x2 defect map.

    Args:
        df (pd.DataFrame): The pre-cleaned and transformed DataFrame.

    Returns:
        A Matplotlib figure object.
    """
    PANEL_SIZE = 7
    GAP_SIZE = 1
    
    # Define styling based on our final design
    BG_COLOR = '#F4A460'      # SandyBrown
    PANEL_COLOR = '#8B4513'   # Brown
    defect_style_map = {
        'Nick': 'magenta', 'Short': 'red', 'Missing Feature': 'lime', 'Cut': 'cyan',
        'Fine Short': '#DDA0DD', 'Pad Violation': 'white', 'Island': 'orange',
        'Cut/Short': '#00BFFF', 'Nick/Protrusion': 'yellow'
    }

    # Create a figure and axes object
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    # --- Draw the Four Panels and Grids ---
    panel_origins = [
        (0, 0),                                     # Bottom-Left
        (PANEL_SIZE + GAP_SIZE, 0),                 # Bottom-Right
        (0, PANEL_SIZE + GAP_SIZE),                 # Top-Left
        (PANEL_SIZE + GAP_SIZE, PANEL_SIZE + GAP_SIZE) # Top-Right
    ]

    for x_start, y_start in panel_origins:
        # Draw panel background with border
        panel = Rectangle((x_start, y_start), PANEL_SIZE, PANEL_SIZE, 
                          linewidth=3, edgecolor='black', facecolor=PANEL_COLOR, zorder=1)
        ax.add_patch(panel)
        # Draw thin inner grid lines
        for i in range(1, PANEL_SIZE):
            ax.plot([x_start + i, x_start + i], [y_start, y_start + PANEL_SIZE], color='black', linewidth=1, zorder=2)
            ax.plot([x_start, x_start + PANEL_SIZE], [y_start + i, y_start + i], color='black', linewidth=1, zorder=2)

    # --- Plot the Defects ---
    for dtype, color in defect_style_map.items():
        dff = df[df['DEFECT_TYPE'] == dtype]
        if not dff.empty:
            ax.scatter(dff['plot_x'], dff['plot_y'], color=color, s=25, zorder=3, 
                       edgecolors='black', linewidths=0.5)

    # --- Final Styling to Remove Ticks/Labels ---
    total_size = 2 * PANEL_SIZE + GAP_SIZE
    ax.set_xlim(-1, total_size + 1)
    ax.set_ylim(-1, total_size + 1)
    ax.set_aspect('equal', adjustable='box')
    
    # Turn off all axis ticks, labels, and spines for a clean look
    ax.axis('off')

    return fig
