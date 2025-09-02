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
        # If a file is uploaded, process it.
        # We use a session state to avoid reprocessing on every interaction.
        if "processed_data" not in st.session_state:
            with st.spinner("Processing Excel file... Please wait."):
                # 1. Load and clean tabular data
                df = load_and_clean_data(uploaded_file)
                
                if df is not None and not df.empty:
                    # 2. Extract images
                    # Pass the file's raw bytes to the cached function
                    image_paths = extract_images_from_excel(uploaded_file.getvalue())

                    # 3. Correlate data with images
                    if len(image_paths) >= len(df) * 2:
                        df['image_path_mod1'] = image_paths[::2][:len(df)]
                        df['image_path_mod2'] = image_paths[1::2][:len(df)]
                    else:
                        st.warning(f"Data-Image Mismatch: Found {len(df)} defects but {len(image_paths)} images. Image display may be incorrect.")
                    
                    # Store the final, processed DataFrame in the session state
                    st.session_state.processed_data = df
                else:
                    st.error("Could not load defect data from the uploaded file. Please check the file format.")
                    # Ensure we don't try to display a dashboard with no data
                    if "processed_data" in st.session_state:
                        del st.session_state.processed_data
        
        # --- Display Content ---
        if "processed_data" in st.session_state:
            # Get the processed data from the session state
            df_processed = st.session_state.processed_data
            
            # Display summary stats in the sidebar
            display_summary_stats(df_processed)
            
            # Display the main dashboard
            display_dashboard(df_processed)

    else:
        # If no file is uploaded, show the welcome message.
        display_welcome_message()

if __name__ == "__main__":
    main()
