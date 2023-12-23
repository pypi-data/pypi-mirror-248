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
from migration.util import validation_table_util
from migration.connector.source.mysql.source import MysqlSource
from migration.connector.source.pg.source import PGSource
from migration.connector.destination.clickzetta.destination import ClickZettaDestination
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _format_job_id():
    unique_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    format_unique_id = unique_id.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') \
                       + str(random.randint(10000, 99999))
    return format_unique_id


def check_validation(source, destination, source_table, destination_table, pk_cols=None, result_dict=None):
    try:
        columns = source.get_table_columns(source_table.split('.')[0], source_table.split('.')[1])
        if result_dict['only_in_source'] == 0 and result_dict['only_in_dest'] == 0 and len(
                result_dict['both_in_but_diff']) == 0:
            st.success(
                f"Checked {result_dict['check_count']} rows, {source_table} and {destination_table} is identical")
            return
        column_names = [column.name for column in columns]
        st.text(f"Validation Result for {source_table} and {destination_table}")
        st.text(f"Only in {source_table} rows count: {result_dict['only_in_source']}")
        st.text(f"Only in {source_table} rows:\n")

        source_map = {}
        destination_map = {}
        for index, value in enumerate(column_names):
            source_map[value] = [row[index] for row in result_dict['only_in_source_list']]
        source_df_result = pd.DataFrame(source_map)
        st.table(source_df_result)
        st.divider()
        st.text(f"Only in {destination_table} rows count: {result_dict['only_in_dest']}")
        st.text(f"Only in {destination_table} rows:\n")
        for index, value in enumerate(column_names):
            destination_map[value] = [row[index] for row in result_dict['only_in_dest_list']]
        destination_df_result = pd.DataFrame(destination_map)
        st.table(destination_df_result)
        st.divider()
        in_source_diff = []
        in_dest_diff = []
        for item in result_dict['both_in_but_diff']:
            in_source_diff.append(item[0])
            in_dest_diff.append(item[1])

        source_diff_map = {}
        destination_diff_map = {}
        for index, value in enumerate(column_names):
            source_diff_map[value] = [row[index] for row in in_source_diff]
            destination_diff_map[value] = [row[index] for row in in_dest_diff]
        source_df_diff = pd.DataFrame(source_diff_map)
        destination_df_diff = pd.DataFrame(destination_diff_map)
        st.text(f"Checked {result_dict['check_count']} rows.")
        st.text(
            f"Both in {source_table} and {destination_table} but different rows count: {len(result_dict['both_in_but_diff'])}")
        st.text(f"Different rows: \n")
        diff_df = source_df_diff.compare(destination_df_diff, result_names=(source_table, destination_table))
        diff_df['id'] = [row[0] for row in in_source_diff]
        st.table(diff_df)
        st.success('validation done')
        # diagnosis_button = st.button('Diag cdc event table', key='diagnosis_button')
        # if diagnosis_button:
        if 'updated_at' not in column_names:
            st.error('updated_at not in table columns, diag abort.')
            return
        else:
            if result_dict['only_in_source'] > 0 and result_dict['only_in_dest'] == 0:
                update_by_list = [int(x) for x in source_df_result['updated_at'].tolist()]
                update_by_list.sort()
                result = destination.execute_sql(
                    f"show tables from {destination_table.split('.')[0]} like '%{destination_table.split('.')[1]}_clickzetta_cdc_event%'")
                if result:
                    cdc_table = f"{result[0][1]}"
                    cdc_ts_result = destination.execute_sql(
                        f"select max(server_ts),min(server_ts) from {result[0][0]}.`{cdc_table}`")[0]
                    cdc_max_server_ts = int(cdc_ts_result[0])
                    cdc_min_server_ts = int(cdc_ts_result[1])
                    diag_df = pd.DataFrame([
                        [cdc_table, "server_ts", cdc_min_server_ts, cdc_max_server_ts],
                        [source_table, "updated_at", update_by_list[0], update_by_list[-1]],
                    ], columns=["table", "column", "min", "max"])
                    st.dataframe(diag_df, hide_index=True)
                    if cdc_min_server_ts > update_by_list[-1]:
                        st.success(f"max updated_at < min server_ts, possible historical cdc event loss.")
                    elif cdc_max_server_ts <= update_by_list[0]:
                        st.success(
                            f"max server_ts <= min updated_at, check if cdc event is being consumed normally.")
                    else:
                        st.success(f"please diag later")

                else:
                    st.error(f"No cdc evnet table found for {destination_table}")
            elif result_dict['only_in_source'] == 0 and result_dict['only_in_dest'] > 0:
                update_by_list = [int(x) for x in destination_df_result['updated_at'].tolist()]
                update_by_list.sort()
                result = destination.execute_sql(
                    f"show tables from {destination_table.split('.')[0]} like '%{destination_table.split('.')[1]}_clickzetta_cdc_event%'")
                if result:
                    cdc_table = f"{result[0][1]}"
                    cdc_max_server_ts = int(
                        destination.execute_sql(f"select max(server_ts) from {result[0][0]}.`{cdc_table}`")[0][0])
                    cdc_min_server_ts = int(
                        destination.execute_sql(f"select min(server_ts) from {result[0][0]}.`{cdc_table}`")[0][0])
                    diag_df = pd.DataFrame([
                        [cdc_table, "server_ts", cdc_min_server_ts, cdc_max_server_ts],
                        [source_table, "updated_at", update_by_list[0], update_by_list[-1]],
                    ], columns=["table", "column", "min", "max"])
                    st.dataframe(diag_df, hide_index=True)
                    if cdc_min_server_ts > update_by_list[-1]:
                        st.success(f"max updated_at < min server_ts, possible historical cdc event loss.")
                    elif cdc_min_server_ts >= update_by_list[0]:
                        st.success(
                            f"max server_ts <= min updated_at, check if cdc event is being consumed normally.")
                    else:
                        st.success(f"unknown situation, please check manually.")
                else:
                    st.error(f"No cdc evnet table found for {destination_table}")
            elif result_dict['only_in_source'] > 0 and result_dict['only_in_dest'] > 0:
                st.success(
                    f"{destination_table} both in source and dest ids is not empty, please check manually.Or waiting next merge into.")
            else:
                st.success(f"{destination_table} both in source and dest ids is empty, Table is healthy.")

    except Exception as e:
        logger.error(f"Detail Validation for {source_table} and {destination_table} failed, error: {e}")
        st.error(e)


def get_source_connection_params(source_engine_conf):
    host = source_engine_conf['host']
    port = source_engine_conf['port']
    username = source_engine_conf['username']
    password = source_engine_conf['password']
    db_type = source_engine_conf['db_type']
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
    if source_tables_file.endswith('.json'):
        with open(source_tables_file, 'r') as f:
            json_result = json.load(f)
            dbs = json_result.keys()
            for db in dbs:
                tables = json_result[db]
                for table in tables:
                    source_tables.append(f"{db}.{table['table']}")
    else:
        with open(source_tables_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                source_tables.append(line.strip())
    return source_tables


def get_destination_tables(destination_tables_file, source_tables_file=None, target_db_schema_name=None):
    destination_tables = []
    if destination_tables_file:
        with open(destination_tables_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                destination_tables.append(line.strip())
    else:
        assert source_tables_file is not None, 'source_tables_file is None'
        assert target_db_schema_name is not None, 'target_db_schema_name is None'
        with open(source_tables_file, 'r') as f:
            json_result = json.load(f)
            dbs = json_result.keys()
            for db in dbs:
                tables = json_result[db]
                for table in tables:
                    destination_tables.append(f"{target_db_schema_name}.{table['table']}")
    return destination_tables


def main():
    try:
        current_directory = os.getcwd()
        parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
        grandparent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
        global_conf = ''
        for root, dirs, files in os.walk(grandparent_directory):
            for file in files:
                if file == 'global_conf.json':
                    global_conf = os.path.join(root, file)
        if not global_conf:
            st.error('global_conf.json not found')
        with open(global_conf, 'r') as f:
            config = json.load(f)
        target_db_conf_path = config['target_db_conf_path']
        source_confs = config['source_conf']
        source_table = ''
        destination_table = ''
        source = None
        destination = None
        pk_column = ''
        target_db_schema_name = config['target_db_schema_name']
        for conf in source_confs:
            db_conf_path = conf['db_conf_path']
            source_check_table_file_path = conf['source_check_table_file_path']
            target_check_table_file_path = conf['target_check_table_file_path']
            pk_column = conf['pk_column']

            source_engine_conf = json.load(open(db_conf_path))
            source = construct_source_engine(get_source_connection_params(source_engine_conf))
            destination_engine_conf = json.load(open(target_db_conf_path))
            destination = construct_destination_engine(get_destination_connection_params(destination_engine_conf))
            source_tables = get_source_tables(source_check_table_file_path)
            destination_tables = get_destination_tables(target_check_table_file_path, source_check_table_file_path,
                                                        target_db_schema_name)
            for table in source_tables:
                if st.session_state['table_name'] in table:
                    source_table = table
                    break
            if not source_table:
                continue
            for table in destination_tables:
                if st.session_state['table_name'] in table:
                    destination_table = table
                    break
            if not destination_table:
                st.error(f"table {st.session_state['table_name']} not found in destination table config file")
            if source_table and destination_table:
                break
        if not source_table:
            st.error(f"table {st.session_state['table_name']} not found in source table config file")
        result_dict = validation_table_util.data_diff_validation_with_pks(source_table, destination_table,
                                                                          source, destination, pk_column)
        check_validation(source, destination, source_table, destination_table, pk_column, result_dict)
    except Exception as e:
        logger.error(f"Full table Validation for {st.session_state['table_name']} failed, error: {e}")
        st.error(e)


st.set_page_config(
    page_title="Realtime Data Validation for XSY",
    layout="wide",
)

st.subheader('XSY Full table Validation')

st.session_state['table_name'] = st.text_input('Please enter check table name:')
if st.session_state['table_name']:
    main()
