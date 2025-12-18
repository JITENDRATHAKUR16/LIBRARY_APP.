import streamlit as st
from streamlit_qr_barcode_scanner import streamlit_qr_barcode_scanner

st.set_page_config(page_title="DIVINE LIBRARY", layout="centered")

st.title("📚 Divine Library Scanner")
st.write("Scan any Book Barcode or QR Code below:")

# Scanner Component
# Ye component browser ka camera use karega
data = streamlit_qr_barcode_scanner()

if data:
    st.success(f"✅ Scanned Successfully!")
    st.info(f"Data Found: {data}")
    
    # Example logic for your library
    if st.button("Check Availability"):
        st.write(f"Searching database for Book ID: {data}...")
else:
    st.warning("Please allow camera access to scan.")

st.markdown("---")
st.caption("Developed for Divine Library")
