import streamlit as st
from streamlit_qr_barcode_scanner import streamlit_qr_barcode_scanner

st.set_page_config(page_title="DIVINE LIBRARY", layout="centered")

st.title("📚 Divine Library Scanner")

# Barcode Scanner logic
data = streamlit_qr_barcode_scanner()

if data:
    st.success(f"✅ Scanned: {data}")
    st.write(f"Book details for {data} will appear here.")
else:
    st.info("Camera open karein aur barcode dikhayein.")
