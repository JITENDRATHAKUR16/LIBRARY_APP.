import streamlit as st
import pandas as pd
import os

# --- PASSWORD LOGIC ---
def check_password():
    """Returns True agar password sahi hai, warna False."""
    def password_entered():
        # Ye 'st.secrets' hum baad mein Streamlit ki website par set karenge
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
        st.error("😕 Password sahi nahi hai.")
        return False
    else:
        return True

# Agar password galat hai toh yahin ruk jao
if not check_password():
    st.stop()

# --- AAPKA ASLI APP CODE YAHAN SE SHURU HOTA HAI ---
st.title("📚 Meri Private Library Manager")

FILE_NAME = "library_data.csv"
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Kitab ka Naam", "Location", "Status"])
    df.to_csv(FILE_NAME, index=False)

st.sidebar.header("Nayi Entry Karein")
name = st.sidebar.text_input("Kitab ka Naam")
loc = st.sidebar.text_input("Shelf No.")
status = st.sidebar.selectbox("Status", ["Library mein hai", "Kisi ko di hui hai"])

if st.sidebar.button("Register mein likhein"):
    if name and loc:
        df = pd.read_csv(FILE_NAME)
        new_row = pd.DataFrame([[name, loc, status]], columns=["Kitab ka Naam", "Location", "Status"])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(FILE_NAME, index=False)
        st.sidebar.success(f"'{name}' save ho gayi!")

st.header("🔍 Kitab Dhoondein")
search = st.text_input("Kaunsi kitab chahiye?")
df = pd.read_csv(FILE_NAME)

if search:
    parinaam = df[df['Kitab ka Naam'].str.contains(search, case=False, na=False)]
    st.table(parinaam)
else:
    st.dataframe(df)