# app/utils/config.py

# Define the expected column names when reading the Excel file
# This now matches your screenshot exactly.
COLUMN_NAMES = [
    "DEFECT_ID", 
    "DEFECT_TYPE", 
    "X_COORDINATES", 
    "Y_COORDINATES", 
    "UNIT_INDEX_X", 
    "UNIT_INDEX_Y"
]

# Define the columns that must have a value for a row to be valid
REQUIRED_COLUMNS = ["DEFECT_ID", "UNIT_INDEX_X", "UNIT_INDEX_Y"]

# Define the color mapping for each defect type for the plot
DEFECT_STYLE_MAP = {
    'Nick': 'magenta', 'Short': 'red', 'Missing Feature': 'lime',
    'Cut': 'cyan', 'Fine Short': '#da70d6', 'Pad Violation': 'white',
    'Island': '#ff8c00', 'Cut/Short': '#00bfff', 'Nick/Protrusion': 'yellow',
    'Unknown': 'black' # Fallback for any unknown defect types
}

# Define the background color for the plot
PLOT_BG_COLOR = '#F4A460' # SandyBrown
