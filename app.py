import streamlit as st
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
        # Sheet se fresh data read karna
        return conn.read(ttl="0")
    except Exception:
        return pd.DataFrame(columns=["Book Name", "Status", "Location", "Book ID"])

df = load_data()

# --- 2. HEADER ---
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

# --- 4. SEARCH & DISPLAY ---
search_query = st.text_input("Search (all, issued, or Name):").strip().lower()
if search_query:
    if search_query == "all":
        res = df
    elif search_query == "issued":
        res = df[df['Status'].str.lower() == "issued"]
    else:
        res = df[df['Book Name'].str.contains(search_query, case=False, na=False)]

    if not res.empty:
        res_display = res.copy()
        res_display.index = range(1, len(res_display) + 1)
        st.dataframe(res_display, use_container_width=True)
    else:
        st.error("❌ Not Found")

# --- 5. ADMIN SECTION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.sidebar.markdown("### 🔐 ADMIN PANEL")
if not st.session_state.logged_in:
    pwd = st.sidebar.text_input("Password:", type="password")
    if st.sidebar.button("Login"):
        if pwd == "admin123":
            st.session_state.logged_in = True
            st.rerun()
else:
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- 6. DATA WRITE LOGIC (Sheet me Save karna) ---
if st.session_state.logged_in:
    st.header("⚙️ Admin Dashboard")
    tab1, tab2 = st.tabs(["📲 Barcode Scan", "✍️ Manual Entry"])

    with tab1:
        cam = st.toggle("Open Camera")
        if cam:
            scanned_id = qrcode_scanner(key='scanner')
            if scanned_id:
                st.success(f"Scanned: {scanned_id}")
                # Form to add scanned book
                with st.form("scan_form"):
                    s_name = st.text_input("Book Name:")
                    s_stat = st.selectbox("Status:", ["Available", "Issued"])
                    if st.form_submit_button("Add Scanned Book to Sheet"):
                        new_row = pd.DataFrame([{"Book Name": s_name, "Status": s_stat, "Location": "Scanned", "Book ID": scanned_id}])
                        updated_df = pd.concat([df, new_row], ignore_index=True)
                        conn.update(data=updated_df)
                        st.success("Sheet Updated! Refreshing...")
                        st.rerun()

    with tab2:
        with st.form("manual_entry_form"):
            col1, col2 = st.columns(2)
            m_id = col1.text_input("Book ID/Barcode:")
            m_name = col1.text_input("Book Name:")
            m_stat = col2.selectbox("Set Status:", ["Available", "Issued", "Received"])
            m_loc = col2.text_input("Shelf Location:")
            
            if st.form_submit_button("Save to Google Sheet"):
                if m_name and m_id:
                    # Naya data purane data me jodna
                    new_entry = pd.DataFrame([{"Book Name": m_name, "Status": m_stat, "Location": m_loc, "Book ID": m_id}])
                    final_df = pd.concat([df, new_entry], ignore_index=True)
                    # Sheet update karna
                    conn.update(data=final_df)
                    st.balloons()
                    st.success(f"'{m_name}' has been saved to Google Sheets!")
                    st.rerun()
                else:
                    st.warning("ID aur Name bharna zaroori hai!")
