# app/data_loader.py
import pandas as pd
import streamlit as st

@st.cache_data
def load_defect_data(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file, header=None, skiprows=1)
        
        df_processed = pd.DataFrame()
        df_processed[['DEFECT_ID', 'DEFECT_TYPE']] = df[0].astype(str).str.split(n=1, expand=True)
        df_processed[['X_COORDINATES', 'Y_COORDINATES', 'UNIT_INDEX_X', 'UNIT_INDEX_Y']] = df.iloc[:, 1:5]

        df_processed['DEFECT_ID'] = pd.to_numeric(df_processed['DEFECT_ID'], errors='coerce')
        df_processed.dropna(subset=['DEFECT_ID'], inplace=True)
        
        for col in ['UNIT_INDEX_X', 'UNIT_INDEX_Y']:
            df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce').fillna(0)
        
        for col in ['DEFECT_ID', 'UNIT_INDEX_X', 'UNIT_INDEX_Y']:
            df_processed[col] = df_processed[col].astype(int)

        return df_processed.reset_index(drop=True)
    except Exception as e:
        st.error(f"Error processing Excel data: {e}")
        return pd.DataFrame() # Return empty dataframe on error
