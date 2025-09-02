# app/core/image_extractor.py

import zipfile
import os
import shutil
from typing import List
import streamlit as st

# Use Streamlit's cache to avoid re-extracting on every interaction
@st.cache_data
def extract_images_from_excel(uploaded_file_contents: bytes) -> List[str]:
    """
    Extracts all images from the bytes of an uploaded .xlsx file.
    Caches the result to avoid re-processing the same file.
    
    Args:
        uploaded_file_contents: The bytes from uploaded_file.getvalue().
        
    Returns:
        A sorted list of file paths to the extracted images.
    """
    EXTRACT_FOLDER = "temp_excel_contents"
    MEDIA_FOLDER = os.path.join(EXTRACT_FOLDER, 'xl', 'media')

    if os.path.exists(EXTRACT_FOLDER):
        shutil.rmtree(EXTRACT_FOLDER)
    os.makedirs(EXTRACT_FOLDER)
    
    temp_excel_path = os.path.join(EXTRACT_FOLDER, "temp.xlsx")
    with open(temp_excel_path, "wb") as f:
        f.write(uploaded_file_contents)

    try:
        with zipfile.ZipFile(temp_excel_path, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_FOLDER)
    except zipfile.BadZipFile:
        return []

    if os.path.exists(MEDIA_FOLDER):
        try:
            image_files = sorted(
                os.listdir(MEDIA_FOLDER),
                key=lambda f: int(''.join(filter(str.isdigit, f)))
            )
            return [os.path.join(MEDIA_FOLDER, f) for f in image_files]
        except (ValueError, TypeError):
            return sorted([os.path.join(MEDIA_FOLDER, f) for f in os.listdir(MEDIA_FOLDER)])

    return []
