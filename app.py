import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
from pyzbar.pyzbar import decode
from datetime import date

# --- CONFIG & DATABASE ---
st.set_page_config(page_title="Divine Library", layout="wide")

conn = sqlite3.connect('library_v2.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS books 
             (book_id TEXT PRIMARY KEY, book_name TEXT, location TEXT, 
              receiver_name TEXT, issue_date TEXT, return_date TEXT, 
              mobile_no TEXT, address TEXT, status TEXT)''')
conn.commit()

# --- HEADER (Names) ---
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 20px;">
        <div>User Name</div>
        <div>Admin Name</div>
    </div><hr>""", unsafe_allow_html=True)

# --- PUBLIC SECTION ---
st.title("📚 Library Search")
search_query = st.text_input("Search Book by Name or ID")

df = pd.read_sql_query("SELECT book_id, book_name, location, status FROM books", conn)

if search_query:
    display_df = df[df['book_name'].str.contains(search_query, case=False) | df['book_id'].str.contains(search_query, case=False)]
    st.dataframe(display_df, use_container_width=True)
else:
    st.dataframe(df, use_container_width=True)

# --- ADMIN SECTION ---
st.sidebar.title("🔐 Admin Panel")
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    pwd = st.sidebar.text_input("Enter Password", type="password")
    if st.sidebar.button("Login"):
        if pwd == "1234":
            st.session_state.admin_logged_in = True
            st.rerun()
else:
    if st.sidebar.button("Logout"):
        st.session_state.admin_logged_in = False
        st.rerun()

    st.markdown("---")
    st.header("🛠️ Book Entry & Management")
    
    # Camera Toggle
    cam_on = st.checkbox("📷 Turn On Camera Scanner")
    scanned_id = ""

    if cam_on:
        img_file = st.camera_input("Scan Barcode")
        if img_file:
            img = Image.open(img_file)
            barcodes = decode(img)
            if barcodes:
                scanned_id = barcodes[0].data.decode('utf-8')
                st.success(f"Scanned ID: {scanned_id}")
            else:
                st.warning("No Barcode Detected")

    # Entry Options
    action = st.radio("Choose Action", ["New Book Entry", "Issue Book", "Return Book"])

    with st.form("admin_form"):
        b_id = st.text_input("Book ID", value=scanned_id)
        
        if action == "New Book Entry":
            b_name = st.text_input("Book Name")
            loc = st.text_input("Location (Rack/Shelf)")
            submitted = st.form_submit_button("Save New Book")
            if submitted:
                c.execute("INSERT OR REPLACE INTO books (book_id, book_name, location, status) VALUES (?,?,?,?)", 
                          (b_id, b_name, loc, 'Available'))
                conn.commit()
                st.success("Book Added!")

        elif action == "Issue Book":
            rec_name = st.text_input("Receiver Name")
            m_no = st.text_input("Mobile No")
            addr = st.text_area("Address")
            i_date = st.date_input("Issue Date", value=date.today())
            r_date = st.date_input("Return Date")
            submitted = st.form_submit_button("Confirm Issue")
            if submitted:
                c.execute("""UPDATE books SET receiver_name=?, mobile_no=?, address=?, 
                             issue_date=?, return_date=?, status='Issued' WHERE book_id=?""",
                          (rec_name, m_no, addr, str(i_date), str(r_date), b_id))
                conn.commit()
                st.success("Book Issued!")

        elif action == "Return Book":
            submitted = st.form_submit_button("Confirm Return")
            if submitted:
                c.execute("""UPDATE books SET receiver_name=NULL, issue_date=NULL, 
                             return_date=NULL, status='Available' WHERE book_id=?""", (b_id,))
                conn.commit()
                st.success("Book Returned to Library!")

    # Admin only full data view
    if st.checkbox("Show All Database Details"):
        full_df = pd.read_sql_query("SELECT * FROM books", conn)
        st.write(full_df)

conn.close()
