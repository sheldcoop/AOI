# app.py
import streamlit as st
from app.data_loader import load_defect_data
from app.plotter import create_defect_map

st.set_page_config(layout="wide")
st.title("Interactive Panel Defect Map")

uploaded_file = st.sidebar.file_uploader("Upload Defect Excel File")

if uploaded_file:
    df = load_defect_data(uploaded_file)
    
    if not df.empty:
        st.sidebar.metric("Total Defects Found", len(df))
        st.plotly_chart(create_defect_map(df))
    else:
        st.warning("Could not load defect data from the file.")
else:
    st.info("Please upload an Excel file to begin.")
