import streamlit as st
from streamlit_qr_barcode_scanner import streamlit_qr_barcode_scanner

st.title("📚 Divine Library Scanner")
data = streamlit_qr_barcode_scanner()

if data:
    st.success(f"Scanned: {data}")
