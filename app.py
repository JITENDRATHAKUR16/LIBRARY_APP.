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

# --- SAMPLE INVENTORY (Database) ---
# Jab aap Google Sheets connect karenge, toh ye data wahan se aayega
if "inventory" not in st.session_state:
    st.session_state.inventory = pd.DataFrame({
        "Book Name": ["The Alchemist", "Think and Grow Rich", "Power of Habit", "Deep Work", "Atomic Habits"],
        "Status": ["Available", "Available", "Issued", "Available", "Issued"],
        "Location": ["Shelf A1", "Shelf B2", "Shelf C1", "Shelf A2", "Shelf B1"]
    })

# --- SESSION STATE FOR LOGIN ---
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
search_query = st.text_input("Book naam, 'all' ya 'issued' likhen:", placeholder="Search here...").strip().lower()

if search_query:
    df = st.session_state.inventory
    
    # Special Keywords Logic
    if search_query == "all":
        st.success("Showing all books in library:")
        st.table(df)
    elif search_query == "issued":
        issued_books = df[df['Status'].str.lower() == "issued"]
        if not issued_books.empty:
            st.warning("List of currently Issued books:")
            st.table(issued_books)
        else:
            st.info("Abhi koi bhi kitab issued nahi hai.")
    else:
        # Normal Search Logic
        result = df[df['Book Name'].str.contains(search_query, case=False, na=False)]
        if not result.empty:
            st.success(f"Result for: {search_query}")
            st.table(result)
        else:
            st.error(f"❌ '{search_query}' - Book Not Found!")

st.divider()

# --- ADMIN OPERATIONS ---
if st.session_state.logged_in:
    st.header("⚙️ Admin Control Panel")
    tab1, tab2 = st.tabs(["📲 Scan Barcode", "✍️ Manual Entry"])

    with tab1:
        cam_on = st.toggle("Turn Camera ON", value=False)
        if cam_on:
            scanned_data = qrcode_scanner(key='admin_scanner')
            if scanned_data:
                st.success(f"Scanned ID: {scanned_data}")
        else:
            st.info("Camera is OFF.")

    with tab2:
        st.subheader("Manual Book Update")
        with st.form("manual_form"):
            m_book_id = st.text_input("Book ID:")
            m_book_name = st.text_input("Book Name:")
            m_action = st.radio("Operation:", ["Issue", "Receive"], horizontal=True)
            m_submit = st.form_submit_button("Save Entry")
            if m_submit:
                st.success("Entry Saved!")
else:
    st.warning("🔒 Admin login required for Scan/Manual entry.")

st.divider()
st.caption("Divine Library App | Update Date: 18-Dec-2025")
