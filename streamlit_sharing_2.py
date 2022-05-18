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
import itertools

st.title("KJV Bible")
st.write("Prototype Under Construction")
gsheet_url = "https://docs.google.com/spreadsheets/d/1pjYzEl-Wlr2X40ECZwesX0_paxLTyssNKFjm1rHbR0U/edit?usp=sharing"
conn = connect()
rows = conn.execute(f'SELECT * FROM "{gsheet_url}"')
df = pd.DataFrame(rows)
df[['chapter','verse_number']] = df[['chapter','verse_number']].astype(float).astype(int)

books = df['book'].unique()
all_books = books
books=np.insert(books,0,'All')

#st.write(list(all_books))

book_choice = st.sidebar.multiselect('Book:', books, default='All')
book_choice = [all_books if "All" in book_choice else book_choice for book_choice in book_choice]
book_choice = [item if 'All' in sublist else list(itertools.chain(*book_choice)) for sublist in book_choice]

chapter = df["chapter"].loc[df["book"].isin(book_choice)].unique()
chapter = df["chapter"].unique()
chapter_all=np.insert(chapter.astype(str),0,'All')
chapter_choice = st.sidebar.multiselect('Chapter', chapter_all, default='All')
chapter_choice = [chapter if 'All' in chapter_choice else chapter_choice for chapter_choice in chapter_choice]
#chapter_choice = [all_chapters for all_chapters in chapter if 'All' in chapter_choice]

verse_number = df["verse_number"].loc[df["chapter"].isin([chapter_choice]) & df["book"].isin([book_choice])].unique()
verse_number = df["verse_number"].unique()
verse_number_all=np.insert(verse_number.astype(str),0,'All')
verse_number_choice = st.sidebar.multiselect('Verse', verse_number_all, default='All')
verse_number_choice = [verse_number if 'All' in verse_number_choice else verse_number_choice for verse_number_choice in verse_number_choice]
verse_number_choice = [list(itertools.chain(*verse_number)) if 'All' in verse_number_choice else verse_number_choice for verse_number_choice in verse_number_choice]
#verse_number_choice = [all_verses for all_verses in verse_number if 'All' in verse_number_choice]

book_filter = df['book'].isin(book_choice)
chapter_filter = df['chapter'].isin(chapter_choice)
verse_filter = df['verse_number'].isin(verse_number_choice)

output = df.loc[book_filter & chapter_filter & verse_filter]


st.write(book_choice)
st.write(book_filter)
st.write(chapter_choice)
st.write(type(chapter_choice))
st.write(verse_number_choice)
st.write(type(verse_number_choice))

st.write('Results:', output)

st.write(df)