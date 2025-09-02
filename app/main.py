# app/main.py
# This is the core logic of our application.

import streamlit as st
# Corrected, simpler imports because we are inside the 'app' folder
from core.data_loader import load_and_transform_data
from ui.plotter import create_defect_map

def main():
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
        with st.spinner("Reading and processing your Excel file..."):
            df_transformed = load_and_transform_data(uploaded_file)

        if df_transformed is not None:
            st.success(f"Successfully loaded and processed {len(df_transformed)} defects.")
            with st.spinner("Generating defect map..."):
                fig = create_defect_map(df_transformed)
                st.pyplot(fig)
                with st.expander("Show Processed Data Table"):
                    st.dataframe(df_transformed)
    else:
        st.info("Please upload your defect Excel file using the sidebar to begin.")

# This allows the script to be run directly if needed
if __name__ == "__main__":
    main()
