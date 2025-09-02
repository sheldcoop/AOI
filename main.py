# app.py
# The main entry point for the Defect-Viz Streamlit application.

import streamlit as st
from app.core.data_loader import load_and_transform_data
from app.ui.plotter import create_defect_map

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Defect Panel Visualizer",
    layout="wide"
)

# --- 2. Application Title ---
st.title("Defect Panel Map Visualizer")

# --- 3. Sidebar for File Upload ---
st.sidebar.title("Control Panel")
uploaded_file = st.sidebar.file_uploader(
    "Upload your Defect Excel File",
    type=["xlsx"]
)

# --- 4. Main Application Logic ---
if uploaded_file is not None:
    # If a file is uploaded, process it.
    with st.spinner("Reading and processing your Excel file..."):
        # Call our data loader to get the plot-ready DataFrame
        df_transformed = load_and_transform_data(uploaded_file)

    if df_transformed is not None:
        # If data processing was successful, create and display the plot.
        st.success(f"Successfully loaded and processed {len(df_transformed)} defects.")
        
        with st.spinner("Generating defect map..."):
            # Call our plotter to create the figure
            fig = create_defect_map(df_transformed)
            
            # Display the final plot
            st.pyplot(fig)

            # Display the raw data in an expandable section
            with st.expander("Show Processed Data Table"):
                st.dataframe(df_transformed)
else:
    # If no file is uploaded, show a welcome message.
    st.info("Please upload your defect Excel file using the sidebar to begin.")
