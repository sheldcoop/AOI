# defect_app/plotter.py
import plotly.graph_objects as go
import numpy as np

def create_defect_map(df):
    fig = go.Figure()
    defect_style_map = {
        'Nick': 'magenta', 'Short': 'red', 'Missing Feature': 'lime', 'Cut': 'cyan',
        'Fine Short': '#da70d6', 'Pad Violation': 'white', 'Island': 'orange',
        'Cut/Short': '#00bfff', 'Nick/Protrusion': 'yellow'
    }
    
    # Add jittered coordinates for better visualization
    np.random.seed(42)
    df['plot_x'] = df['UNIT_INDEX_Y'] + np.random.uniform(0.15, 0.85, size=len(df))
    df['plot_y'] = df['UNIT_INDEX_X'] + np.random.uniform(0.15, 0.85, size=len(df))

    for dtype, color in defect_style_map.items():
        dff = df[df['DEFECT_TYPE'] == dtype]
        if not dff.empty:
            fig.add_trace(go.Scatter(x=dff['plot_x'], y=dff['plot_y'], mode='markers',
                marker=dict(color=color, size=12, line=dict(width=1.5, color='Black')), name=dtype))
    
    grid_x = int(df['UNIT_INDEX_X'].max() + 1)
    grid_y = int(df['UNIT_INDEX_Y'].max() + 1)
    shapes = []
    for i in range(grid_y + 1): shapes.append(dict(type='line', x0=i-0.5, y0=-0.5, x1=i-0.5, y1=grid_x-0.5, line=dict(color='black', width=4)))
    for i in range(grid_x + 1): shapes.append(dict(type='line', x0=-0.5, y0=i-0.5, x1=grid_y-0.5, y1=i-0.5, line=dict(color='black', width=4)))
    
    fig.update_layout(plot_bgcolor='#F4A460', shapes=shapes, width=800, height=800, yaxis_scaleanchor='x')
    return fig
