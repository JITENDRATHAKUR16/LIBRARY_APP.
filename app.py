import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner
import pandas as pd

st.set_page_config(page_title="DIVINE LIBRARY", layout="wide")

# --- CUSTOM CSS FOR INTERFACE ---
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Divine Library System")

# --- SIDEBAR (LOGIN) ---
st.sidebar.header("Admin Access")
password = st.sidebar.text_input("Admin Password dalo scan ke liye:", type="password")

# --- SEARCH MODE (For Everyone) ---
st.header("🔍 Manual Book Search")
search_query = st.text_input("Book ka naam ya Author likhen:", placeholder="Example: Bhagavad Gita")

if search_query:
    st.write(f"Searching for: **{search_query}**")
    # Yahan aapka search logic/table aayega
    # Sample Table:
    data = {
        "Book Name": ["Rich Dad Poor Dad", "The Alchemist"],
        "Status": ["Available", "Issued"],
        "Location": ["Shelf A-1", "Shelf B-3"]
    }
    df = pd.DataFrame(data)
    st.table(df)

st.divider()

# --- SCAN MODE (Only for Admin) ---
if password == "admin123":  # Aap apna password yahan badal sakte hain
    st.header("📲 Admin Scan Mode")
    st.success("Admin Login Successful! Camera loading...")
    
    scanned_data = qrcode_scanner(key='admin_scanner')
    
    if scanned_data:
        st.write(f"📊 **Scanned Result:** {scanned_data}")
        # Yahan book update karne ka option de sakte hain
        st.button("Update Book Status")
else:
    if password != "":
        st.sidebar.error("Galat Password!")
    st.info("💡 Scan karne ka option sirf Admin (Jitendra) ke liye hai. User sirf search kar sakte hain.")

st.divider()
st.caption("Divine Library App | Last Updated: Dec 2025")
