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

#import pip
#pip install ghseetsdb

import streamlit as st
import pandas as pd
from gsheetsdb import connect


st.title("KJV Bible")
gsheet_url = "https://docs.google.com/spreadsheets/d/1pjYzEl-Wlr2X40ECZwesX0_paxLTyssNKFjm1rHbR0U/edit?usp=sharing"
conn = connect()
rows = conn.execute(f'SELECT * FROM "{gsheet_url}"')
df_gsheet = pd.DataFrame(rows)
st.write(df_gsheet)