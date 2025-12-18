import streamlit as st
import pandas as pd
import os
from datetime import date

# --- CONFIGURATION & LOGO ---
st.set_page_config(page_title="DIVINE LIBRARY", layout="wide")

# Custom CSS for Gradient Background & Styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .main-logo {
        font-size: 20px;
        font-weight: bold;
        color: #1E3A8A;
        border: 2px solid #1E3A8A;
        padding: 5px 10px;
        border-radius: 8px;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# Top Left Logo (Jitendra Thakur)
st.markdown('<div class="main-logo">👤 JITENDRA THAKUR</div>', unsafe_allow_html=True)
st.title("📚 DIVINE LIBRARY")

# --- DATABASE SETUP ---
FILE_NAME = "divine_library_v4.csv"
cols = ["Book Name", "Location", "Status", "Borrower Name", "Mobile", "Address", "Issue Date", "Return Date"]

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=cols)
    df.to_csv(FILE_NAME, index=False)

df = pd.read_csv(FILE_NAME)

# --- ADMIN LOGIN CHECK ---
# Isse sirf aap (Admin) hi entry/edit kar payenge
is_admin = False
with st.sidebar:
    st.header("🔐 Admin Login")
    admin_pass = st.text_input("Admin Password", type="password")
    if admin_pass == st.secrets["password"]:
        is_admin = True
        st.success("Welcome, Jitendra!")
    elif admin_pass:
        st.error("Access Denied")

# --- ADMIN PANEL (ONLY FOR JITENDRA) ---
if is_admin:
    st.sidebar.markdown("---")
    st.sidebar.header("📋 Book Entry/Update")
    
    all_books = ["-- Nayi Kitab Add Karein --"] + sorted(df["Book Name"].unique().tolist())
    selected_book = st.sidebar.selectbox("Kitab Chunein", all_books)

    if selected_book == "-- Nayi Kitab Add Karein --":
        name = st.sidebar.text_input("Kitab ka Naam (Automatic CAPITAL)").upper() # Always Capital
        existing_data = None
    else:
        name = selected_book
        existing_data = df[df["Book Name"] == name].iloc[0]

    loc = st.sidebar.text_input("Shelf/Row No.", value=str(existing_data["Location"]) if existing_data is not None else "").upper()
    status = st.sidebar.selectbox("Status", ["Available", "Issued"], 
                                 index=0 if existing_data is None or existing_data["Status"] == "Available" else 1)

    b_name, b_mobile, b_addr, b_issue, b_return = "", "", "", "", ""
    if status == "Issued":
        b_name = st.sidebar.text_input("Student Name", value=existing_data["Borrower Name"] if existing_data is not None else "").upper()
        b_mobile = st.sidebar.text_input("Mobile No", value=existing_data["Mobile"] if existing_data is not None else "")
        b_addr = st.sidebar.text_area("Address", value=existing_data["Address"] if existing_data is not None else "").upper()
        b_issue = st.sidebar.date_input("Issue Date", date.today())
        b_return = st.sidebar.date_input("Return Date")

    if st.sidebar.button("Save Record"):
        if name:
            df = df[df["Book Name"] != name] # Remove old entry
            new_row = pd.DataFrame([[name, loc, status, b_name, b_mobile, b_addr, b_issue, b_return]], columns=cols)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(FILE_NAME, index=False)
            st.sidebar.success(f"{name} Updated!")
            st.rerun()

# --- PUBLIC VIEW (FOR EVERYONE) ---
st.header("🔍 Dynamic Search")
search_query = st.text_input("Search by Book Name or Location...", "").upper()

# Filter data dynamically
if search_query:
    filtered_df = df[df['Book Name'].str.contains(search_query, na=False) | 
                     df['Location'].str.contains(search_query, na=False)]
else:
    filtered_df = df

# Security: Other person sees only restricted columns
if is_admin:
    st.subheader("Full Inventory (Admin View)")
    st.dataframe(filtered_df)
else:
    st.subheader("Library Catalog")
    # Hide private details from users
    public_cols = ["Book Name", "Location", "Status", "Return Date"]
    st.table(filtered_df[public_cols])

if not is_admin:
    st.info("ℹ️ Student details are hidden. Login as admin to manage entries.")
