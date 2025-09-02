# app/config.py
# Centralized configuration for the Defect Panel Visualizer

# --- Data Loading Configuration ---
# Specifies the column names to be used when reading the Excel file.
# This assumes the Excel file has columns in the order:
# DEFECT_ID, DEFECT_TYPE, X_COORDINATES, Y_COORDINATES, UNIT_INDEX_X, UNIT_INDEX_Y
COLUMN_NAMES = [
    "DEFECT_ID",
    "DEFECT_TYPE",
    "X_COORDINATES",
    "Y_COORDINATES",
    "UNIT_INDEX_X",
    "UNIT_INDEX_Y"
]

# --- View Configurations ---
# Defines the geometric parameters for different visualization modes.
VIEW_CONFIG = {
    "Original 2x2": {
        "panel_size": 7,
        "gap_size": 1,
        "title": "Original View (2x2 of 7x7 Panels)"
    },
    "14x14 Grid": {
        "panel_size": 6,
        "gap_size": 2,
        "title": "14x14 View (4x 6x6 Panels with 2-Unit Gap)"
    }
}

# --- Styling Configuration ---
# Colors and styles for the Plotly chart.
STYLE = {
    'bg_color': '#F4A460',      # SandyBrown, background of the plot
    'panel_color': '#8B4513',   # Brown, background of the panels
    'grid_color': 'black',      # Color of the grid lines

    # Mapping of known defect types to specific colors.
    # A defect type not in this map will be assigned a default color.
    'defect_map': {
        'Nick': 'magenta',
        'Short': 'red',
        'Missing Feature': 'lime',
        'Cut': 'cyan',
        'Fine Short': '#DDA0DD',
        'Pad Violation': 'white',
        'Island': 'orange',
        'Cut/Short': '#00BFFF',
        'Nick/Protrusion': 'yellow'
    },

    # Default color for any defect type not found in the defect_map.
    'default_defect_color': 'grey',

    # A list of fallback colors to be used for new, un-mapped defect types.
    # These will be assigned sequentially to any new defect type encountered.
    'dynamic_color_palette': [
        '#FF6347',  # Tomato
        '#4682B4',  # SteelBlue
        '#32CD32',  # LimeGreen
        '#FFD700',  # Gold
        '#6A5ACD',  # SlateBlue
        '#40E0D0',  # Turquoise
        '#EE82EE',  # Violet
        '#F5DEB3',  # Wheat
    ]
}
