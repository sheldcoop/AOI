# app.py
# Final version using Matplotlib to replicate the target visual style.

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# --- 1. Page Configuration ---
st.set_page_config(page_title="Defect Panel Map", layout="wide")

# --- 2. Hardcoded Sample Data ---
# We use more defects to simulate the dense look of the target image
NUM_DEFECTS = 2000
GRID_SIZE_X = 14
GRID_SIZE_Y = 14
PANEL_SIZE = 7

# Defect types and colors from the target image
defect_style_map = {
    'Cluster': 'magenta',
    'Spot_Lime': 'lime',
    'Spot_Red': 'red',
    'Spot_Gray': 'gray',
    'Special_Cyan': 'cyan',
    'Special_White': 'white'
}
defect_types = list(defect_style_map.keys())
# Create a weighted probability for defects to simulate the dense pink clusters
probabilities = [0.6, 0.1, 0.1, 0.1, 0.05, 0.05]

df = pd.DataFrame({
    'UNIT_INDEX_X': np.random.randint(0, GRID_SIZE_X, size=NUM_DEFECTS),
    'UNIT_INDEX_Y': np.random.randint(0, GRID_SIZE_Y, size=NUM_DEFECTS),
    'DEFECT_TYPE': np.random.choice(defect_types, size=NUM_DEFECTS, p=probabilities)
})

# Add jittered coordinates directly, without gaps for now
df['plot_x'] = df['UNIT_INDEX_Y'] + np.random.rand(NUM_DEFECTS)
df['plot_y'] = df['UNIT_INDEX_X'] + np.random.rand(NUM_DEFECTS)

# --- 3. Create the Matplotlib Visualization ---
st.header("Static Defect Map (Matplotlib)")

# Create a figure and axes object with a specific size and background color
fig, ax = plt.subplots(figsize=(4, 3))
fig.patch.set_facecolor('#364521') # Dark olive green from your target

# --- 4. Manually Draw the Panels and Grids ---
PANEL_COLOR = '#8B4513' # Brown
GAP_SIZE = 1.0 # The gap between panels

panel_coords = [
    (0, 0),                           # Bottom-Left
    (PANEL_SIZE + GAP_SIZE, 0),       # Bottom-Right
    (0, PANEL_SIZE + GAP_SIZE),       # Top-Left
    (PANEL_SIZE + GAP_SIZE, PANEL_SIZE + GAP_SIZE) # Top-Right
]

for x_start, y_start in panel_coords:
    # Draw the brown panel background
    panel = Rectangle((x_start, y_start), PANEL_SIZE, PANEL_SIZE,
                      linewidth=0, facecolor=PANEL_COLOR, zorder=1)
    ax.add_patch(panel)
    
    # Draw the thin grid lines
    for i in range(1, PANEL_SIZE):
        ax.plot([x_start + i, x_start + i], [y_start, y_start + PANEL_SIZE], color='black', linewidth=0.5, zorder=2)
        ax.plot([x_start, x_start + PANEL_SIZE], [y_start + i, y_start + i], color='black', linewidth=0.5, zorder=2)

# --- 5. Plot the Defects as Small Dots ---
for dtype, color in defect_style_map.items():
    dff = df[df['DEFECT_TYPE'] == dtype]
    
    # Transform coordinates to plot on the correct panel
    plot_x = dff['UNIT_INDEX_Y'] % PANEL_SIZE + np.where(dff['UNIT_INDEX_Y'] >= PANEL_SIZE, PANEL_SIZE + GAP_SIZE, 0) + np.random.rand(len(dff))
    plot_y = dff['UNIT_INDEX_X'] % PANEL_SIZE + np.where(dff['UNIT_INDEX_X'] >= PANEL_SIZE, PANEL_SIZE + GAP_SIZE, 0) + np.random.rand(len(dff))

    # Use a small 's' value for pixel-like dots
    ax.scatter(plot_x, plot_y, color=color, s=5, zorder=3)


# --- 6. Final Styling ---
# Define the total area covered by the panels
total_size = 2 * PANEL_SIZE + GAP_SIZE

# Draw the outer cyan border
border = Rectangle((0, 0), total_size, total_size,
                   linewidth=2, edgecolor='cyan', facecolor='none', zorder=4)
ax.add_patch(border)

# Set axis limits and aspect ratio
ax.set_xlim(-1, total_size + 1)
ax.set_ylim(-1, total_size + 1)
ax.set_aspect('equal', adjustable='box')
ax.axis('off') # Turn off the axis labels and ticks

# --- 7. Display the plot in Streamlit ---
st.pyplot(fig)
