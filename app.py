import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Basic Setup
st.set_page_config(page_title="DIVINE LIBRARY", layout="wide")

# Connection (Sirf Read karne ke liye)
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        # Sheet ka data read karein
        return conn.read(ttl="0")
    except:
        return pd.DataFrame(columns=["Book Name", "Status", "Location", "Book ID"])

df = load_data()

# --- SEARCH & STATS SECTION ---
st.title("📚 Divine Library System")

# Stats (Hamesha dikhenge)
c1, c2, c3 = st.columns(3)
c1.metric("Total Books", len(df))
c2.metric("Issued", len(df[df['Status'] == "Issued"]))
c3.metric("Available", len(df[df['Status'] == "Available"]))

st.divider()

# Search Bar
search = st.text_input("Search Books...").strip().lower()
if search:
    # Search logic yahan rahega...
    st.dataframe(df[df['Book Name'].str.contains(search, case=False, na=False)])

# --- ADMIN SECTION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.sidebar.title("🔐 Admin Panel")
if not st.session_state.logged_in:
    pwd = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if pwd == st.secrets["password"]:
            st.session_state.logged_in = True
            st.rerun()
else:
    st.sidebar.success("Admin Active")
    
    # SOLUTION: Kyunki writing block hai, hum Admin ko direct Google Sheet ka button denge
    st.markdown("### ⚙️ Admin Actions")
    st.info("Kyunki Google security high hai, niche diye button se Sheet mein data add karein. Wo yahan turant update ho jayega.")
    
    sheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    st.link_button("✍️ Open Sheet to Add/Edit Data", sheet_url)
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
