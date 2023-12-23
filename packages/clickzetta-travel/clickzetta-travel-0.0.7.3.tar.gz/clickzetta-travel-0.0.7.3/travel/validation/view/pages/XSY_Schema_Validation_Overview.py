import os

import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Realtime PG Schema Validation for XSY",
    layout="wide",
)

select_pattern = 'select * from xsy_schema_validation'

current_directory = os.getcwd()
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
grandparent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))

db_paths = []

for root, dirs, files in os.walk(grandparent_directory):
    for file in files:
        if file.endswith(".db"):
            if 'schema' in file:
                db_paths.append(os.path.join(root, file))

st.subheader('Real-time Schema Validation Result Overview')
result_list = []

with sqlite3.connect(db_paths[0]) as conn:
    cursor = conn.cursor()
    cursor.execute(select_pattern)
    result = cursor.fetchall()
    for row in result:
        temp_row = [f"{row[7].upper()}_{row[1].strip().split('.')[0]}", row[1].strip().split('.')[1], row[3], row[4],
                    row[5], row[6]]
        result_list.append(temp_row)

df = pd.DataFrame(result_list,
                  columns=['source_prefix', 'table_name', 'cols_only_in_source', 'cols_only_in_dest', 'check_timestamp',
                           'cdc_table_count'])

st.dataframe(df, width=3000, height=3000)
