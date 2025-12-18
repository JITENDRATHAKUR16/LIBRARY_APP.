import streamlit as st  # Yeh line sabse upar honi chahiye
from streamlit_gsheets import GSheetsConnection
from streamlit_qrcode_scanner import qrcode_scanner
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="DIVINE LIBRARY", layout="wide", initial_sidebar_state="collapsed")

# --- 1. GOOGLE SHEETS CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        # Sheet se fresh data uthane ke liye
        return conn.read(ttl="0")
    except:
        # Agar sheet khali hai toh default columns banaye
        return pd.DataFrame(columns=["Book Name", "Status", "Location", "Book ID"])

df = load_data()

# --- 2. HEADER SECTION (Responsive) ---
t1, t2 = st.columns(2)
with t1: st.markdown("##### 👤 JITENDRA THAKUR")
with t2: st.markdown("<h5 style='text-align: right;'>👤 KRISHNA SHARMA</h5>", unsafe_allow_html=True)

st.title("📚 Divine Library System")

# --- 3. LIVE STATS ---
c1, c2, c3 = st.columns(3)
c1.metric("Total Books", len(df))
c2.metric("Issued", len(df[df['Status'] == "Issued"]))
c3.metric("Available", len(df[df['Status'] == "Available"]))

st.divider()

# --- 4. SEARCH SECTION ---
search_query = st.text_input("Search (Type 'all', 'issued', or Book Name):").strip().lower()

if search_query:
    if search_query == "all":
        display_df = df
    elif search_query == "issued":
        display_df = df[df['Status'].str.lower() == "issued"]
    else:
        display_df = df[df['Book Name'].str.contains(search_query, case=False, na=False)]

    if not display_df.empty:
        st.markdown(f"**Found {len(display_df)} Results:**")
        # Serial counting 1 se start
        temp_df = display_df.copy()
        temp_df.index = range(1, len(temp_df) + 1)
        st.dataframe(temp_df, use_container_width=True)
    else:
        st.error("❌ Book Not Found!")

# --- 5. ADMIN SECTION (Attractive Sidebar) ---
st.sidebar.markdown("### 🔐 ADMIN CENTRAL")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    pwd = st.sidebar.text_input("Admin Password:", type="password")
    if st.sidebar.button("Unlock Admin Access"):
        if pwd == "admin123": # Apna password yahan change karein
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.sidebar.error("Galat Password!")
else:
    st.sidebar.success("Logged In ✅")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- 6. ADMIN OPERATIONS ---
if st.session_state.logged_in:
    st.header("⚙️ Admin Operations")
    tab1, tab2 = st.tabs(["📲 Barcode Scan", "✍️ Manual Entry"])
    
    with tab1:
        cam_on = st.toggle("Open Camera Scanner")
        if cam_on:
            scanned_val = qrcode_scanner(key='admin_scan')
            if scanned_val:
                st.success(f"Scanned ID: {scanned_val}")
    
    with tab2:
        with st.form("manual_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_id = st.text_input("Book ID:")
                new_name = st.text_input("Book Name:")
            with col2:
                new_status = st.selectbox("Status:", ["Available", "Issued", "Received"])
                new_loc = st.text_input("Location (Shelf):")
            
            if st.form_submit_button("Save to Inventory"):
                st.success("Entry recorded! (Update in Google Sheet manually for now)")

st.divider()
st.caption(f"Last Updated: {datetime.now().strftime('%d-%b-%Y %H:%M')}")
