import streamlit as st
from streamlit_qr_barcode_scanner import streamlit_qr_barcode_scanner

st.set_page_config(page_title="DIVINE LIBRARY", layout="wide")

st.title("📚 Divine Library Barcode Scanner")

# Scanner component
st.subheader("Scan Barcode below:")
data = streamlit_qr_barcode_scanner()

if data:
    st.success(f"Scanned Data: {data}")
    # Yahan aap apna database logic add kar sakte hain
    st.write("Is book ki details fetch ho rahi hain...")
else:
    st.info("Camera open karein aur barcode dikhayein.")

st.markdown("---")
st.caption("Powered by Streamlit")
