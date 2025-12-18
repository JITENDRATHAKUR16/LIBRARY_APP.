import streamlit as st
import pandas as pd
import os
from datetime import date

# --- PASSWORD LOGIC (Wahi purana) ---
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"] 
        else:
            st.session_state["password_correct"] = False
    if "password_correct" not in st.session_state:
        st.title("🔐 Access Restricted")
        st.text_input("Kripya Library Password Likhein", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.title("🔐 Access Restricted")
        st.text_input("Galat Password! Dubara koshish karein", type="password", on_change=password_entered, key="password")
        return False
    else:
        return True

if not check_password():
    st.stop()

# --- APP START ---
st.title("📚 Advanced Library Tracker")

FILE_NAME = "library_data_v2.csv"
cols = ["Book Name", "Location", "Status", "Borrower Name", "Mobile", "Address", "Issue Date"]

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=cols)
    df.to_csv(FILE_NAME, index=False)

# --- Sidebar Form ---
st.sidebar.header("📋 Entry Form")
name = st.sidebar.text_input("Kitab ka Naam")
loc = st.sidebar.text_input("Shelf/Row No.")
status = st.sidebar.selectbox("Status", ["Available", "Issued"])

# Agar status 'Issued' hai toh extra details mangna
b_name, b_mobile, b_addr, b_date = "", "", "", ""
if status == "Issued":
    st.sidebar.subheader("👤 Borrower Details")
    b_name = st.sidebar.text_input("Student ka Naam")
    b_mobile = st.sidebar.text_input("Mobile Number")
    b_addr = st.sidebar.text_area("Address")
    b_date = st.sidebar.date_input("Kab le gaya?", date.today())

if st.sidebar.button("Data Save Karein"):
    df = pd.read_csv(FILE_NAME)
    new_data = pd.DataFrame([[name, loc, status, b_name, b_mobile, b_addr, b_date]], columns=cols)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)
    st.sidebar.success("Entry saved successfully!")

# --- Display Data ---
st.header("🔍 Library Records")
df_display = pd.read_csv(FILE_NAME)
st.dataframe(df_display)
