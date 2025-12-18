import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="DIVINE LIBRARY", layout="wide")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .metric-card { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #007bff; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    .admin-header { color: #1E3A8A; font-weight: bold; border-bottom: 2px solid #1E3A8A; }
    </style>
    """, unsafe_allow_html=True)

# --- TOP NAMES SECTION ---
col_l, col_r = st.columns([1, 1])
with col_l:
    st.markdown("### 👤 JITENDRA THAKUR")
with col_r:
    st.markdown("<h3 style='text-align: right;'>👤 KRISHNA SHARMA</h3>", unsafe_allow_html=True)

# --- DATABASE / INVENTORY ---
if "inventory" not in st.session_state:
    st.session_state.inventory = pd.DataFrame({
        "Book Name": ["The Alchemist", "Think and Grow Rich", "Power of Habit", "Deep Work", "Atomic Habits"],
        "Status": ["Available", "Available", "Issued", "Available", "Issued"],
        "Location": ["Shelf A1", "Shelf B2", "Shelf C1", "Shelf A2", "Shelf B1"]
    })

# --- ADMIN SECTION (Attractive Sidebar) ---
st.sidebar.markdown("<h2 class='admin-header'>🔐 ADMIN CENTRAL</h2>", unsafe_allow_html=True)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    with st.sidebar:
        pass_input = st.text_input("Admin Password:", type="password")
        if st.button("Unlock Admin Access"):
            if pass_input == "admin123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Key ❌")
else:
    st.sidebar.success("Logged In: Jitendra Thakur ✅")
    if st.sidebar.button("🔒 Secure Logout"):
        st.session_state.logged_in = False
        st.rerun()

st.title("📚 Divine Library System")

# --- SEARCH & STATS SECTION ---
st.header("🔍 Search Books")
search_query = st.text_input("Book naam, 'all' ya 'issued' likhen:", placeholder="Typing here...").strip().lower()

# Stats Calculation
df = st.session_state.inventory
total_books = len(df)
issued_count = len(df[df['Status'] == "Issued"])
avail_count = len(df[df['Status'] == "Available"])

# Display Stats Cards
s1, s2, s3 = st.columns(3)
with s1: st.info(f"📁 **Total Books:** {total_books}")
with s2: st.warning(f"📤 **Total Issued:** {issued_count}")
with s3: st.success(f"✅ **Available:** {avail_count}")

st.divider()

# --- DISPLAY LOGIC ---
if search_query:
    display_df = pd.DataFrame()
    if search_query == "all":
        display_df = df
    elif search_query == "issued":
        display_df = df[df['Status'].str.lower() == "issued"]
    else:
        display_df = df[df['Book Name'].str.contains(search_query, case=False, na=False)]

    if not display_df.empty:
        # Serial Number from 1
        display_df = display_df.copy()
        display_df.index = range(1, len(display_df) + 1)
        st.dataframe(display_df.style.set_properties(**{'background-color': '#f9f9f9', 'color': 'black', 'border-color': 'silver'}), use_container_width=True)
    else:
        st.error("Book Not Found!")

st.divider()

# --- ADMIN OPERATIONS ---
if st.session_state.logged_in:
    st.header("⚙️ Admin Control Operations")
    t1, t2 = st.tabs(["📲 Barcode Scan", "✍️ Manual Data Entry"])
    
    with t1:
        cam = st.toggle("Activate Scanner")
        if cam:
            data = qrcode_scanner(key='adm_cam')
            if data: st.write(f"Scanned: {data}")
            
    with t2:
        with st.form("manual_entry"):
            col1, col2 = st.columns(2)
            with col1:
                b_id = st.text_input("Book ID / Barcode:")
                b_name = st.text_input("Book Name:")
            with col2:
                b_status = st.selectbox("Current Status:", ["Available", "Issued", "Received"])
                b_loc = st.text_input("Shelf Location:")
            
            if st.form_submit_button("Save to Inventory"):
                st.success(f"Successfully Added: {b_name}")
else:
    st.caption("User Mode: Only Search is active.")

st.markdown("---")
st.caption(f"Divine Library | {datetime.now().strftime('%d-%b-%Y')}")
