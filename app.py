import streamlit as st
import pandas as pd
import os

# App ka naam
st.title("📚 Meri Library Manager")

# Data save karne ke liye file
FILE_NAME = "library_data.csv"

# Agar file nahi hai toh nayi banayein
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Kitab ka Naam", "Location", "Status"])
    df.to_csv(FILE_NAME, index=False)

# --- Nayi Book Add Karne ka Section ---
st.sidebar.header("Nayi Entry Karein")
name = st.sidebar.text_input("Kitab ka Naam")
loc = st.sidebar.text_input("Kahan rakhi hai? (Shelf No.)")
status = st.sidebar.selectbox("Abhi ki sthiti", ["Library mein hai", "Kisi ko di hui hai"])

if st.sidebar.button("Register mein likhein"):
    if name and loc:
        df = pd.read_csv(FILE_NAME)
        new_row = pd.DataFrame([[name, loc, status]], columns=["Kitab ka Naam", "Location", "Status"])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(FILE_NAME, index=False)
        st.sidebar.success(f"'{name}' ko register kar liya gaya hai!")
    else:
        st.sidebar.error("Naam aur Location bharna zaroori hai!")

# --- Kitab Dhoondne ka Section ---
st.header("🔍 Kitab ki Inquiry Karein")
search = st.text_input("Kaunsi kitab dhoond rahe hain?")

df = pd.read_csv(FILE_NAME)

if search:
    # Kitab dhoondne ka logic
    parinaam = df[df['Kitab ka Naam'].str.contains(search, case=False, na=False)]
    if not parinaam.empty:
        st.success(f"Haan! '{search}' mil gayi.")
        st.table(parinaam)
    else:
        st.warning("Maaf kijiye, ye kitab hamare paas nahi hai.")
else:
    st.write("Saari kitabon ki list niche dekhein:")
    st.dataframe(df)