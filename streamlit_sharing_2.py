def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)
install_and_import('gsheetsdb')

import streamlit as st
import pandas as pd
from gsheetsdb import connect

st.title("KJV Bible")
gsheet_url = "https://docs.google.com/spreadsheets/d/1pjYzEl-Wlr2X40ECZwesX0_paxLTyssNKFjm1rHbR0U/edit?usp=sharing"
conn = connect()
rows = conn.execute(f'SELECT * FROM "{gsheet_url}"')
df = pd.DataFrame(rows)

books = df['book'].drop_duplicates()
chapter = df['chapter']
verse_number = df['verse_number']
output = df

book_choice = st.sidebar.selectbox('Which book(s)?:', books)
chapter_choice = st.sidebar.selectbox('', chapter)
verse_choice = st.sidebar.selectbox('', verse_number)

st.write('Results:', output)