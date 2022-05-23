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

book_choice = st.sidebar.multiselect('Book:', books, default='All')
book_choice = [all_books if "All" in book_choice else book_choice for book_choice in book_choice]
book_choice = [item if len(book_choice) > 1 else sublist for sublist in book_choice for item in sublist]

chapter = df["chapter"].loc[df["book"].isin(book_choice)].unique()
chapter = df["chapter"].unique()
chapter_all=np.insert(chapter.astype(str),0,'All')
chapter_choice = st.sidebar.multiselect('Chapter', chapter_all, default='All')
chapter_choice = [chapter if "All" in chapter_choice else chapter_choice for chapter_choice in chapter_choice]
#chapter_choice = [item if len(chapter_choice) > 1 else sublist for sublist in chapter_choice for item in sublist]

verse_number = df["verse_number"].loc[df["chapter"].isin([chapter_choice]) & df["book"].isin([book_choice])].unique()
verse_number = df["verse_number"].unique()
verse_number_all=np.insert(verse_number.astype(str),0,'All')
verse_number_choice = st.sidebar.multiselect('Verse', verse_number_all, default='All')
verse_number_choice = [verse_number if "All" in verse_number_choice else verse_number_choice for verse_number_choice in verse_number_choice]
#verse_number_choice = [item if len(verse_number_choice) > 1 else sublist for sublist in verse_number_choice for item in sublist]

book_filter = df['book'].isin(book_choice)
#chapter_filter = df['chapter'].isin([np.vectorize(np.int(item)) for item in list(chapter_choice)])
chapter_filter = df['chapter'].isin([item.astype(int) for item in chapter_choice])
#chapter_filter = df['chapter'].isin([1])
verse_filter = df['verse_number'].isin([item.astype(int) for item in verse_number_choice])

output = df.loc[book_filter & chapter_filter & verse_filter]


st.write(book_choice)
#st.write(book_filter)
st.write(chapter_choice)
#st.write(chapter_filter)
st.write(verse_number_choice)
#st.write(verse_filter)

st.write('Results:', output)

#st.write(df)