import os

import streamlit as st
import sqlite3
import pandas as pd

select_pattern = 'select * from xsy_validation '

current_directory = os.getcwd()
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
grandparent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))

db_paths = []

for root, dirs, files in os.walk(grandparent_directory):
    for file in files:
        if file.endswith(".db"):
            if 'schema' not in file:
                db_paths.append(os.path.join(root, file))
st.set_page_config(
    page_title="Realtime Data Validation for XSY",
    layout="wide",
)

st.markdown(
    """
    ### Clickzetta real-time data validation tool.

    - source_prefix: db_type and source db name
    - table_name: table name
    - source_count: source table row count
    - dest_count: destination table row count
    - only_in_source: row_count only in source table
    - only_in_dest: row_count only in destination table
    - only_in_source_list: PKs only in source table, x-{pks} means pks are not in destination table occured x times
    - only_in_dest_list: PKs only in destination table, x-{pks} means pks are not in source table occured x times
    - only_source_max_times_id: max PKs missing times of only_in_source_list
    - only_dest_max_times_id: max PKs missing times of only_in_dest_list
    - check_timestamp: check timestamp
    - max_cdc_ts: dest table max cdc time
    - check_status: 'DONE' means success, 'UN_DONE' means pks check times more than 10 times and still not find all difference

"""
)

st.subheader('Real-time Validation Result Overview')
result_list = []

for db_path in db_paths:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(select_pattern)
        result = cursor.fetchall()
        for row in result:
            temp_row = [f"{row[14].strip().upper()}_{row[1].strip().split('.')[0]}", row[1].strip().split('.')[1],
                        int(row[3]), int(row[4]), row[5], row[6], row[7],
                        row[8], int(row[9]) if len(row[9]) > 0 else 0, int(row[10]) if len(row[10]) > 0 else 0, row[11],
                        row[12], row[13]]
            result_list.append(temp_row)

df = pd.DataFrame(result_list, columns=['source_prefix', 'table_name', 'source_count',
                                        'dest_count', 'only_in_source', 'only_in_dest',
                                        'only_in_source_list', 'only_in_dest_list', 'only_source_max_times_id',
                                        'only_dest_max_times_id', 'check_timestamp', 'max_cdc_ts', 'check_status'])
st.dataframe(df, width=3000, height=3000)
