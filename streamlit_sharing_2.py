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

books = df['book'].unique()
#chapter = df['chapter']
#verse_number = df['verse_number']
#output = df

book_choice = st.sidebar.multiselect('Book:', books)
chapter = df["chapter"].loc[df["book"].isin([book_choice])].unique()
chapter_choice = st.sidebar.multiselect('Chapter', chapter)
verse_number = df["verse_number"].loc[df["chapter"].isin([chapter_choice])].unique()
verse_number_choice = st.sidebar.multiselect('Verse', verse_number)

output = df.loc[(df['book']==book_choice) & (df['chapter']==chapter_choice) & (df['verse_number']== verse_number_choice)]

st.write('Results:', output)