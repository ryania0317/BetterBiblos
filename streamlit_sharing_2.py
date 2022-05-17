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
import numpy as np
from gsheetsdb import connect
from collections import Counter

st.title("KJV Bible")
gsheet_url = "https://docs.google.com/spreadsheets/d/1pjYzEl-Wlr2X40ECZwesX0_paxLTyssNKFjm1rHbR0U/edit?usp=sharing"
conn = connect()
rows = conn.execute(f'SELECT * FROM "{gsheet_url}"')
df = pd.DataFrame(rows)

books = df['book'].unique()
all_books = books
books=np.insert(books,0,'All')
#books = books.insert(0, 'All')

book_choice = st.sidebar.multiselect('Book:', books, default='All')
book_choice = [str(all_books) if 'All' in book_choice else book_choice for all_books in all_books]
book_choice = list(set(book_choice))

#st.write(book_choice)
chapter = df["chapter"].loc[df["book"].isin(book_choice)].unique()
chapter_all=np.insert(chapter.astype(str),0,'All')
#st.write(chapter)
chapter_choice = st.sidebar.multiselect('Chapter', chapter_all, default='All')
chapter_choice = [all_chapters for all_chapters in chapter if 'All' in chapter_choice]

verse_number = df["verse_number"].loc[df["chapter"].isin([chapter_choice]) & df["book"].isin([book_choice])].unique()
verse_number_all=np.insert(verse_number.astype(str),0,'All')
verse_number_choice = st.sidebar.multiselect('Verse', verse_number_all, default='All')
verse_number_choice = [all_verses for all_verses in verse_number if 'All' in verse_number_choice]


output = df.loc[(df['book'].isin([book_choice])) & (df['chapter'].isin([chapter_choice])) & (df['verse_number'].isin([verse_number_choice]))]


st.write(book_choice)
st.write(chapter_choice)
st.write(verse_number_choice)

st.write('Results:', output)