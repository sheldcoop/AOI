# defect_app/data_loader.py
import streamlit as st
import pandas as pd

@st.cache_data
def load_defect_data(uploaded_file):
    try:
        # The successful strategy: no header, skip the title row.
        df = pd.read_excel(uploaded_file, header=None, skiprows=1)
        
        # Keep only the columns we need.
        df = df.iloc[:, :6]
        df.columns = [
            'RAW_DEFECT_INFO', 'X_COORDINATES', 'Y_COORDINATES', 
            'UNIT_INDEX_X', 'UNIT_INDEX_Y', 'MODALITY_1_IMG'
        ]
        
        # Split the first column and clean the data.
        df.dropna(subset=['RAW_DEFECT_INFO'], inplace=True)
        split_data = df['RAW_DEFECT_INFO'].astype(str).str.split(n=1, expand=True)
        df['DEFECT_ID'] = pd.to_numeric(split_data[0], errors='coerce')
        df['DEFECT_TYPE'] = split_data[1].str.strip()

        df.dropna(subset=['DEFECT_ID'], inplace=True)
        
        for col in ['UNIT_INDEX_X', 'UNIT_INDEX_Y']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        for col in ['DEFECT_ID', 'UNIT_INDEX_X', 'UNIT_INDEX_Y']:
            df[col] = df[col].astype(int)

        return df.reset_index(drop=True)
    except Exception as e:
        st.error(f"Error processing the data within the Excel file: {e}")
        return None
