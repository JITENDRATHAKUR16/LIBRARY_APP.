import streamlit as st
import sqlite3
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Divine Library System", layout="wide")

# --- DATABASE CONNECTION ---
# Ye apne aap 'library.db' file bana dega
conn = sqlite3.connect('library.db', check_same_thread=False)
c = conn.cursor()

# --- TABLES CREATION (Merging Features) ---
c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_name TEXT,
        author TEXT,
        category TEXT,
        status TEXT
    )
''')
conn.commit()

# --- HEADER ---
st.title("📚 Divine Library System")
st.markdown("---")

# --- SIDEBAR (Input Features) ---
st.sidebar.header("Add New Book")
with st.sidebar.form("add_book_form"):
    book_name = st.text_input("Book Name")
    author = st.text_input("Author Name")
    category = st.selectbox("Category", ["Fiction", "Non-Fiction", "Science", "History", "Other"])
    submit_button = st.form_submit_button("Add to Library")

    if submit_button:
        if book_name and author:
            c.execute("INSERT INTO books (book_name, author, category, status) VALUES (?, ?, ?, ?)", 
                      (book_name, author, category, 'Available'))
            conn.commit()
            st.sidebar.success("Book Added Successfully!")
        else:
            st.sidebar.error("Please fill all details.")

# --- MAIN DASHBOARD (Stats Features) ---
# Data fetch karna
df = pd.read_sql_query("SELECT * FROM books", conn)

# Stats calculation
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Books", len(df))
with col2:
    st.metric("Available", len(df[df['status'] == 'Available']))
with col3:
    st.metric("Issued", len(df[df['status'] == 'Issued']))

st.markdown("---")

# --- DISPLAY DATA TABLE ---
st.subheader("📋 Library Inventory")
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("Library khali hai. Sidebar se books add karein.")

# --- SEARCH FEATURE ---
st.sidebar.markdown("---")
search_query = st.sidebar.text_input("Search Book by Name")
if search_query:
    search_df = df[df['book_name'].str.contains(search_query, case=False, na=False)]
    st.subheader("🔍 Search Results")
    st.write(search_df)

conn.close()
