# app/main.py

import streamlit as st
import pandas as pd

# Import our modular components
from app.core.data_loader import load_and_clean_data
from app.core.image_extractor import extract_images_from_excel
from app.ui.sidebar import build_sidebar, display_summary_stats
from app.ui.dashboard import display_dashboard, display_welcome_message

def main():
    """The main function that runs the Streamlit application."""
    
    # --- Page Configuration ---
    st.set_page_config(
        page_title="Defect-Viz Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # --- Build The UI ---
    uploaded_file = build_sidebar()
    
    # --- Main Logic ---
    if uploaded_file is not None:
        if "processed_data" not in st.session_state or st.session_state.get("uploaded_file_name") != uploaded_file.name:
            with st.spinner("Processing Excel file... Please wait."):
                df = load_and_clean_data(uploaded_file)
                
                if df is not None and not df.empty:
                    image_paths = extract_images_from_excel(uploaded_file.getvalue())

                    if len(image_paths) >= len(df) * 2:
                        df['image_path_mod1'] = image_paths[::2][:len(df)]
                        df['image_path_mod2'] = image_paths[1::2][:len(df)]
                    else:
                        st.warning(f"Data-Image Mismatch: Found {len(df)} defects but {len(image_paths)} images.")
                    
                    st.session_state.processed_data = df
                    st.session_state.uploaded_file_name = uploaded_file.name
                else:
                    st.error("Could not load defect data from the uploaded file. Please check the file format.")
                    if "processed_data" in st.session_state:
                        del st.session_state.processed_data
        
        if "processed_data" in st.session_state:
            df_processed = st.session_state.processed_data
            display_summary_stats(df_processed)
            display_dashboard(df_processed)

    else:
        display_welcome_message()

if __name__ == "__main__":
    main()
