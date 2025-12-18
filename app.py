import streamlit as st
import pandas as pd
import os
from datetime import date
from streamlit_barcode_reader import streamlit_barcode_reader

# --- CONFIGURATION ---
st.set_page_config(page_title="DIVINE LIBRARY", layout="wide")

# Dark Style CSS
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #050a14 0%, #0f172a 100%); color: white; }
    .main-logo { font-size: 20px; font-weight: bold; color: #38bdf8; border: 2px solid #38bdf8; padding: 5px 10px; border-radius: 8px; display: inline-block; }
    .stButton>button { width: 100%; height: 60px; font-size: 22px; font-weight: bold; border-radius: 12px; }
    .issue-btn button { background-color: #e11d48 !important; color: white !important; }
    .receive-btn button { background-color: #10b981 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-logo">👤 JITENDRA THAKUR</div>', unsafe_allow_html=True)
st.title("📚 DIVINE LIBRARY - PRO SYSTEM")

# --- DATABASE SETUP ---
FILE_NAME = "divine_library_v6.csv"
cols = ["Barcode", "Book Name", "Location", "Status", "Borrower Name", "Mobile", "Issue Date", "Return Date"]

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=cols)
    df.to_csv(FILE_NAME, index=False)
df = pd.read_csv(FILE_NAME)

# --- SIDEBAR: ADMIN PANEL ---
with st.sidebar:
    st.header("🔐 Admin Access")
    admin_pass = st.text_input("Password", type="password")
    is_admin = (admin_pass == st.secrets["password"])
    
    if is_admin:
        st.success("Welcome, Jitendra!")
        st.markdown("---")
        st.subheader("🆕 Add New Book")
        with st.form("new_book"):
            nbc = st.text_input("Barcode ID").upper()
            nnm = st.text_input("Book Name").upper()
            nlc = st.text_input("Location").upper()
            if st.form_submit_button("Register"):
                new_row = pd.DataFrame([[nbc, nnm, nlc, "Available", "", "", "", ""]], columns=cols)
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(FILE_NAME, index=False)
                st.success("Kitab register ho gayi!")
                st.rerun()

# --- 1. SEARCH SECTION (LAPTOP) ---
st.header("🔍 1. Search Book (Laptop)")
search_q = st.text_input("Kitab ka Naam ya Location dhoondein...").upper()
if search_q:
    results = df[df['Book Name'].str.contains(search_q, na=False) | df['Location'].str.contains(search_q, na=False)]
    st.dataframe(results[["Book Name", "Location", "Status", "Return Date"]], use_container_width=True)

st.markdown("---")

# --- 2. SCAN SECTION (MOBILE) ---
st.header("📲 2. Scan Barcode (Mobile)")
st.write("Camera ke saamne Barcode laayein ya manual likhein:")

# Mobile Camera Scanner
scanned_code = streamlit_barcode_reader(key='reader')
manual_bc = st.text_input("Ya Barcode manually likhein...").upper()
final_barcode = scanned_code if scanned_code else manual_bc

if final_barcode:
    match = df[df['Barcode'] == str(final_barcode)]
    if not match.empty:
        book = match.iloc[0]
        st.info(f"KITAB: **{book['Book Name']}** | LOCATION: **{book['Location']}**")
        
        if is_admin:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="issue-btn">', unsafe_allow_html=True)
                if st.button("ISSUE (Dena)"): st.session_state.mode = "ISSUE"
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="receive-btn">', unsafe_allow_html=True)
                if st.button("RECEIVE (Wapas Lena)"): st.session_state.mode = "RECEIVE"
                st.markdown('</div>', unsafe_allow_html=True)

            if 'mode' in st.session_state:
                with st.form("action_form"):
                    if st.session_state.mode == "ISSUE":
                        b_name = st.text_input("Student Name").upper()
                        b_mob = st.text_input("Mobile No")
                        r_date = st.date_input("Return Date")
                        if st.form_submit_button("Confirm Issue"):
                            df.loc[df['Barcode'] == str(final_barcode), ["Status", "Borrower Name", "Mobile", "Issue Date", "Return Date"]] = ["Issued", b_name, b_mob, date.today(), r_date]
                            df.to_csv(FILE_NAME, index=False)
                            st.success("Kitab Issue ho gayi!")
                            del st.session_state.mode
                            st.rerun()
                    elif st.session_state.mode == "RECEIVE":
                        if st.form_submit_button("Confirm Return"):
                            df.loc[df['Barcode'] == str(final_barcode), ["Status", "Borrower Name", "Mobile", "Issue Date", "Return Date"]] = ["Available", "", "", "", ""]
                            df.to_csv(FILE_NAME, index=False)
                            st.success("Kitab wapas mil gayi!")
                            del st.session_state.mode
                            st.rerun()
        else:
            st.warning("Admin login karein update karne ke liye.")
    else:
        st.error("Ye Barcode register nahi hai.")

# --- PUBLIC VIEW ---
st.markdown("---")
st.subheader("📚 Library Status")
st.table(df[["Book Name", "Location", "Status", "Return Date"]].head(15))
