import sqlite3
import streamlit as st
import pandas as pd

# 1. Database file se connect karein (agar nahi hai toh ban jayegi)
conn = sqlite3.connect('my_data.db')
c = conn.cursor()

# 2. Ek table banayein (Example: Library Table)
c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        status TEXT
    )
''')
conn.commit()

st.title("My Library Database")

# 3. Data add karne ka option (Streamlit interface)
with st.form("entry_form"):
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    submit = st.form_submit_button("Add to Database")
    
    if submit:
        c.execute("INSERT INTO books (title, author, status) VALUES (?, ?, ?)", (title, author, 'Available'))
        conn.commit()
        st.success("Data save ho gaya!")

# 4. Data dikhane ke liye
df = pd.read_sql_query("SELECT * FROM books", conn)
st.dataframe(df)

conn.close()
