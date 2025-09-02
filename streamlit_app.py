# streamlit_app.py
# Main entry point for the Defect Panel Visualizer application.

import streamlit as st
from streamlit_plotly_events import plotly_events
# Use absolute imports from the 'app' package
from app.core.data_loader import load_and_transform_data
from app.ui.plotter import create_defect_map

def main():
    """
    Main function to run the Streamlit application.
    """
    # --- 1. Page Configuration ---
    st.set_page_config(
        page_title="Defect Panel Visualizer",
        layout="wide"
    )

    # --- 2. Application Title ---
    st.title("Defect Panel Map Visualizer")
    st.markdown("Hover over a defect to see its type and ID. Click on a defect to see its full details below the map.")

    # --- 3. Sidebar for File Upload ---
    st.sidebar.title("Control Panel")
    uploaded_file = st.sidebar.file_uploader(
        "Upload your Defect Excel File",
        type=["xlsx"]
    )

    # --- 4. Main Application Logic ---
    if uploaded_file is not None:
        # We need to reset the index to ensure the 'pointNumber' from the click event
        # corresponds directly to the DataFrame's integer location.
        df_transformed = load_and_transform_data(uploaded_file)

        if df_transformed is not None and not df_transformed.empty:
            df_transformed = df_transformed.reset_index(drop=True)
            st.success(f"Successfully loaded and processed {len(df_transformed)} defects.")

            # Create two columns for the layout
            col1, col2 = st.columns([2, 1])

            with col1:
                with st.spinner("Generating defect map..."):
                    fig = create_defect_map(df_transformed)
                    # Use plotly_events to make the chart interactive
                    selected_points = plotly_events(fig, click_event=True, key="defect_map")

            with col2:
                st.subheader("Selected Defect Details")
                if selected_points:
                    # Get the index of the first clicked point
                    point_index = selected_points[0]['pointNumber']
                    # Retrieve the full data for that defect
                    selected_defect_data = df_transformed.iloc[point_index]
                    st.write(selected_defect_data)
                else:
                    st.info("Click on a defect point on the map to see its details here.")

            with st.expander("Show Full Processed Data Table"):
                st.dataframe(df_transformed)
        else:
            st.warning("No data could be processed from the uploaded file.")
    else:
        st.info("Please upload your defect Excel file using the sidebar to begin.")

# This allows the script to be run directly
if __name__ == "__main__":
    main()
