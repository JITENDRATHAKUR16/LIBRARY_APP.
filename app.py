import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner

st.set_page_config(page_title="DIVINE LIBRARY", layout="centered")
st.title("📚 Divine Library Scanner")

# Scanner logic
st.write("Click the button below to start scanning:")
scanned_data = qrcode_scanner(key='scanner')

if scanned_data:
    st.success(f"✅ Scanned Successfully!")
    st.info(f"Book ID / Data: {scanned_data}")
else:
    st.warning("Awaiting scan... Please point camera at Barcode/QR.")
