import math
import os.path
import random
import sys
import pandas as pd
import streamlit as st
import json
from datetime import datetime
from time import sleep
import sqlite3
import travel.util.validation_util as validation_util
from migration.connector.source.mysql.source import MysqlSource
from migration.connector.source.pg.source import PGSource
from concurrent.futures import ThreadPoolExecutor, CancelledError, wait, ALL_COMPLETED
from migration.connector.destination.clickzetta.destination import ClickZettaDestination
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _format_job_id():
    unique_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    format_unique_id = unique_id.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') \
                       + str(random.randint(10000, 99999))
    return format_unique_id

def check_validation(source, destination, source_table, destination_table, pk_cols=None):
    try:
        columns = source.get_table_columns(source_table.split('.')[0], source_table.split('.')[1])
        result_dict = validation_util.pk_all_columns_table_validation(source, destination, source_table, destination_table, pk_cols)
        column_names = [column.name for column in columns]
        st.text(f"Validation Result for {source_table} and {destination_table}")
        st.text(f"Only in {source_table} rows count: {result_dict['only_in_source']}")
        st.text(f"Only in {source_table} rows:\n")
        source_df_result = pd.DataFrame()
        destination_df_result = pd.DataFrame()
        for index, value in enumerate(column_names):
            source_df_result[value] = [row[index] for row in result_dict['only_in_source_list']]
        st.table(source_df_result)
        st.divider()
        st.text(f"Only in {destination_table} rows count: {result_dict['only_in_dest']}")
        st.text(f"Only in {destination_table} rows:\n")
        for index, value in enumerate(column_names):
            destination_df_result[value] = [row[index] for row in result_dict['only_in_dest_list']]
        st.table(destination_df_result)
        st.divider()
        in_source_diff = []
        in_dest_diff = []
        for item in result_dict['both_in_but_diff']:
            in_source_diff.append(item[0])
            in_dest_diff.append(item[1])
        source_df_diff = pd.DataFrame()
        destination_df_diff = pd.DataFrame()
        for index, value in enumerate(column_names):
            source_df_diff[value] = [row[index] for row in in_source_diff]
            destination_df_diff[value] = [row[index] for row in in_dest_diff]
        st.text(f"Both in {source_table} and {destination_table} but different rows count: {len(result_dict['both_in_but_diff'])}")
        st.text(f"Both in {source_table} and {destination_table} but different rows: \n")
        diff_df = source_df_diff.compare(destination_df_diff, result_names=(source_table, destination_table))
        diff_df['id'] = [row[0] for row in in_source_diff]
        st.table(diff_df)
        st.success('validation success')
        diagnosis_button = st.button('进行诊断')
        if diagnosis_button:
            if 'updated_at' not in column_names:
                st.error('updated_at not in table columns, please check manually')
                return
            else:
                if result_dict['only_in_source'] > 0 and result_dict['only_in_dest'] == 0:
                    update_by_list = [int(x) for x in source_df_result['updated_at'].tolist()]
                    update_by_list.sort()
                    result = destination.execute_sql(f"show tables from {destination_table.split('.')[0]} like '%{destination_table.split('.')[1]}_clickzetta_cdc_event%'")
                    if result:
                        cdc_table = f"{result[0][1]}"
                        cdc_max_server_ts = int(destination.execute_sql(f"select max(server_ts) from {result[0][0]}.`{cdc_table}`")[0][0])
                        cdc_min_server_ts = int(destination.execute_sql(f"select min(server_ts) from {result[0][0]}.`{cdc_table}`")[0][0])
                        st.text(f"{destination_table} cdc_max_server_ts: {cdc_max_server_ts}")
                        st.text(f"{destination_table} cdc_min_server_ts: {cdc_min_server_ts}")
                        st.text(f"{destination_table} only in source ids max update time is: {update_by_list[-1]}")
                        st.text(f"{destination_table} only in source ids min update time is: {update_by_list[0]}")
                        st.text(f"Only in dest table ids is empty.")
                        if cdc_min_server_ts > update_by_list[-1]:
                            st.success(f"{destination_table} cdc 表最小 server_ts 大于缺失id最大update 时间，检查cdc同步逻辑，大概率更新数据永恒丢失。")
                        elif cdc_max_server_ts <= update_by_list[0]:
                            st.success(f"{destination_table} cdc 表最大 server_ts 小于缺失id最小update 时间，请等待cdc 表同步数据。")
                        else:
                            st.success(f"请等待下一次merge into 后再进行诊断")

                    else:
                        st.error(f"{destination_table} cdc 表不存在，请检查是否存在cdc event表。")
                elif result_dict['only_in_source'] == 0 and result_dict['only_in_dest'] > 0:
                    update_by_list = [int(x) for x in destination_df_result['updated_at'].tolist()]
                    update_by_list.sort()
                    result = destination.execute_sql(f"show tables from {destination_table.split('.')[0]} like '%{destination_table.split('.')[1]}_clickzetta_cdc_event%'")
                    if result:
                        cdc_table = f"{result[0][1]}"
                        cdc_max_server_ts = int(destination.execute_sql(f"select max(server_ts) from {result[0][0]}.`{cdc_table}`")[0][0])
                        cdc_min_server_ts = int(destination.execute_sql(f"select min(server_ts) from {result[0][0]}.`{cdc_table}`")[0][0])
                        st.text(f"{destination_table} cdc_max_server_ts: {cdc_max_server_ts}")
                        st.text(f"{destination_table} cdc_min_server_ts: {cdc_min_server_ts}")
                        st.text(f"{destination_table} only in dest ids max update time is: {update_by_list[-1]}")
                        st.text(f"{destination_table} only in dest ids min update time is: {update_by_list[0]}")
                        st.text(f"Only in source table ids is empty.")
                        if cdc_min_server_ts > update_by_list[-1]:
                            st.success(f"{destination_table} cdc 表最小 server_ts 大于缺失id最大update 时间，检查cdc同步逻辑，大概率更新数据永恒丢失。")
                        elif cdc_min_server_ts >= update_by_list[0]:
                            st.success(f"{destination_table} cdc 表最小 server_ts 大于缺失id最小update 时间，请等待下一次 merge into后再进行检查。")
                        else:
                            st.success(f"{destination_table} 被写花了，建议重新同步数据。")
                    else:
                        st.error(f"{destination_table} cdc 表不存在，请检查是否存在cdc event表。")
                elif result_dict['only_in_source'] > 0 and result_dict['only_in_dest'] > 0:
                    st.success(f"{destination_table} both in source and dest ids is not empty, please check manually.Or waiting next merge into.")
                else:
                    st.success(f"{destination_table} both in source and dest ids is empty, Table is healthy.")
    except Exception as e:
        logger.error(f"Detail Validation for {source_table} and {destination_table} failed, error: {e}")
        raise e


def validate(source, destination, source_tables, destination_tables, pk_cols):
    if len(source_tables) != len(destination_tables):
        raise Exception("Source tables and destination tables should have the same length")
    try:
        for source_table, destination_table in zip(source_tables, destination_tables):
            check_validation(source, destination, source_table, destination_table, pk_cols)
    except Exception as e:
        raise e
def get_source_connection_params(source_engine_conf):
    host = source_engine_conf['host']
    port = source_engine_conf['port']
    username = source_engine_conf['username']
    password = source_engine_conf['password']
    db_type= source_engine_conf['db_type']
    database = source_engine_conf['database']
    return {
        'host': host,
        'port': port,
        'user': username,
        'password': password,
        'db_type': db_type,
        'database': database,
    }

def get_destination_connection_params(destination_engine_conf):
    service = destination_engine_conf['service']
    workspace = destination_engine_conf['workspace']
    instance = destination_engine_conf['instance']
    vcluster = destination_engine_conf['vcluster']
    username = destination_engine_conf['username']
    password = destination_engine_conf['password']
    schema = destination_engine_conf['schema']
    instance_id = destination_engine_conf['instanceId']

    return {
        'service': service,
        'workspace': workspace,
        'instance': instance,
        'vcluster': vcluster,
        'username': username,
        'password': password,
        'schema': schema,
        'instanceId': instance_id,
    }

def construct_source_engine(connection_dict: dict):
    db_type = connection_dict['db_type']
    if db_type == 'mysql':
        return MysqlSource(connection_dict)
    elif db_type == 'postgres':
        return PGSource(connection_dict)
    else:
        raise Exception(f"Unsupported db type {db_type}")

def construct_destination_engine(connection_dict: dict):
    return ClickZettaDestination(connection_dict)


def get_source_tables(source_tables_file):
    source_tables = []
    with open(source_tables_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            source_tables.append(line.strip())
    return source_tables

def get_destination_tables(destination_tables_file):
    destination_tables = []
    with open(destination_tables_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            destination_tables.append(line.strip())
    return destination_tables


def main():
    source_engine_conf = '/home/xsy/pg_conf.json'
    destination_engine_conf = '/home/xsy/cz_conf_example.json'
    pk_cols = 'id'
    try:
        source_engine_conf = json.load(open(source_engine_conf))
        source = construct_source_engine(get_source_connection_params(source_engine_conf))
        destination_engine_conf = json.load(open(destination_engine_conf))
        destination = construct_destination_engine(get_destination_connection_params(destination_engine_conf))
        source_tables = st.session_state['source_table'].split(',')
        destination_tables = st.session_state['dest_table'].split(',')
        validate(source, destination, source_tables, destination_tables, pk_cols)
    except Exception as e:
        print('validation error:', e)
        raise e

st.set_page_config(
    page_title="Realtime Data Validation for XSY",
    layout="wide",
)

st.subheader('PgSQL Full table Validation')

cols = st.columns(2)
st.session_state['source_table'] = cols[0].text_input('source table')
st.session_state['dest_table'] = cols[1].text_input('destination table')
if st.session_state['source_table'] and st.session_state['dest_table']:
    main()