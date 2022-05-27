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

def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])

#!pip install streamlit
install_and_import('streamlit')
#import streamlit as st

st.title("KJV Bible")
gsheet_url = "https://docs.google.com/spreadsheets/d/1pjYzEl-Wlr2X40ECZwesX0_paxLTyssNKFjm1rHbR0U/edit?usp=sharing"
conn = connect()
rows = conn.execute(f'SELECT * FROM "{gsheet_url}"')
df = pd.DataFrame(rows)
df = df[['book','chapter','verse_number','verse']]
df[['chapter','verse_number']] = df[['chapter','verse_number']].astype(float).astype(int)

books = df['book'].unique()
all_books = list(books)
books=np.insert(books,0,'All')

col1, col2, col3 = streamlit.columns(3)

with col1:
    book_choice = streamlit.multiselect('Book:', books, default='All')
    book_choice = [all_books if "All" in book_choice else book_choice for book_choice in book_choice]
    book_choice = flatten(book_choice)
with col2:
    chapter = df["chapter"].loc[df["book"].isin(book_choice)].unique()
    chapter = df["chapter"].unique()
    chapter_all = np.insert(chapter.astype(str), 0, 'All')
    chapter_choice = streamlit.multiselect('Chapter', chapter_all, default='All')
    chapter_choice = [chapter if "All" in chapter_choice else chapter_choice for chapter_choice in chapter_choice]
    chapter_choice = [item for sublist in chapter_choice for item in sublist]
with col3:
    verse_number = df["verse_number"].loc[df["chapter"].isin([chapter_choice]) & df["book"].isin([book_choice])].unique()
    verse_number = df["verse_number"].unique()
    verse_number_all = np.insert(verse_number.astype(str), 0, 'All')
    verse_number_choice = streamlit.multiselect('Verse', verse_number_all, default='All')
    verse_number_choice = [verse_number if "All" in verse_number_choice else verse_number_choice for verse_number_choice in verse_number_choice]
    verse_number_choice = [item for sublist in verse_number_choice for item in sublist]

book_filter = df['book'].isin(book_choice)
chapter_filter = df['chapter'].isin([int(item) for item in chapter_choice])
verse_filter = df['verse_number'].isin([int(item) for item in verse_number_choice])

output = df.loc[book_filter & chapter_filter & verse_filter]

streamlit.write('Results:', output)