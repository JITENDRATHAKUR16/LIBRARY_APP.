import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="DIVINE LIBRARY", layout="wide")

# --- TOP NAMES SECTION ---
col_l, col_r = st.columns([1, 1])
with col_l:
    st.markdown("### 👤 JITENDRA THAKUR")
with col_r:
    st.markdown("<h3 style='text-align: right;'>👤 KRISHNA SHARMA</h3>", unsafe_allow_html=True)

# --- SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- SIDEBAR LOGIN ---
st.sidebar.header("Admin Access")
if not st.session_state.logged_in:
    password_input = st.sidebar.text_input("Enter Admin Password:", type="password")
    if st.sidebar.button("Login"):
        if password_input == "admin123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.sidebar.error("Galat Password!")
else:
    st.sidebar.success("Admin Logged In ✅")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

st.title("📚 Divine Library System")

# --- SEARCH BOOKS SECTION ---
st.header("🔍 Search Books")
search_query = st.text_input("Book naam likhen:", placeholder="Search here...")
# (Yahan aapka search logic pehle jaisa hi rahega)

st.divider()

# --- ADMIN SCAN & ACTION SECTION ---
if st.session_state.logged_in:
    st.header("📲 Admin Operations")
    scanned_data = qrcode_scanner(key='admin_scanner')
    
    if scanned_data:
        st.success(f"Scanned Book ID: {scanned_data}")
        
        # Action Selection
        action = st.radio("Select Action:", ["Issue Book", "Receive Book"])
        
        with st.form("action_form"):
            if action == "Issue Book":
                member_name = st.text_input("Member Name:")
                due_date = st.date_input("Return Due Date:", datetime.now() + timedelta(days=7))
                st.write("Click 'Confirm' to issue this book.")
            else:
                condition = st.selectbox("Book Condition:", ["Perfect", "Slightly Damaged", "Damaged"])
                fine = st.number_input("Fine Amount (if any):", min_value=0)
                st.write("Click 'Confirm' to return this book to shelf.")
            
            submitted = st.form_submit_button("Confirm Action")
            if submitted:
                st.balloons()
                st.success(f"Data for {scanned_data} has been updated locally!")
                # Note: Ye data save karne ke liye humein Google Sheets connect karni hogi.
else:
    st.warning("🔒 Scanning and Library Actions are locked. Please login as Admin.")
