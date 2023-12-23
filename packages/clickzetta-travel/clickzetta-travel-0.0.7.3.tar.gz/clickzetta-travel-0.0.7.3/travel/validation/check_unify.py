import math
import os.path
import random
import sys
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

global_result_map = {}

real_time_table_ddl = ('create table xsy_validation (id integer primary key autoincrement, source_table varchar(255), '
                       'dest_table varchar(255), source_count integer, '
                       'dest_count integer, only_in_source integer, '
                       'only_in_dest integer, only_in_source_list text, only_in_dest_list text,'
                       ' only_source_max_times_id text, only_dest_max_times_id text,'
                       'check_timestamp text, max_source_db_time text, last_check_status varchar(255), db_type varchar(255))')

select_pattern = 'select only_in_source_list,only_in_dest_list from xsy_validation where source_table = ? and dest_table = ?'

update_pattern = (
    'update xsy_validation set source_count = ?, dest_count = ?, last_check_status = ?, only_in_source = ?, only_in_dest = ?, '
    'only_in_source_list = ?, only_in_dest_list = ?,only_source_max_times_id = ?, only_dest_max_times_id = ?'
    ' ,check_timestamp = ?, max_source_db_time = ?'
    'where source_table = ? and dest_table = ?')

insert_pattern = (
    'insert into xsy_validation (source_table, dest_table, source_count, dest_count,last_check_status, only_in_source, '
    'only_in_dest, only_in_source_list, only_in_dest_list,only_source_max_times_id, only_dest_max_times_id,'
    ' check_timestamp, max_source_db_time, db_type)'
    ' values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')

delete_pattern = 'delete from xsy_validation where source_table = ? and dest_table = ?'

schema_real_time_table_ddl = (
    'create table xsy_schema_validation (id integer primary key autoincrement, source_table varchar(255), '
    'dest_table varchar(255), cols_only_in_source text, '
    'cols_only_in_dest text,'
    'check_timestamp text, cdc_table_count integer, db_type varchar(255))')
schema_select_pattern = 'select cols_only_in_source,cols_only_in_dest from xsy_schema_validation where source_table = ? and dest_table = ?'

schema_update_pattern = (
    'update xsy_schema_validation set cols_only_in_source = ?, cols_only_in_dest = ?, check_timestamp = ?, cdc_table_count = ? '
    'where source_table = ? and dest_table = ?')

schema_insert_pattern = (
    'insert into xsy_schema_validation (source_table, dest_table, cols_only_in_source, cols_only_in_dest,'
    ' check_timestamp, cdc_table_count, db_type)'
    ' values (?, ?, ?, ?, ?, ?, ?)')

schema_delete_pattern = 'delete from xsy_schema_validation where source_table = ? and dest_table = ?'


def _format_job_id():
    unique_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    format_unique_id = unique_id.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') \
                       + str(random.randint(10000, 99999))
    return format_unique_id


def schema_validation(job_name, source, destination, source_table, destination_table, sqlite_db_path, cdc_table_prefix,
                      db_type):
    try:
        logger.info(f'processing {source_table} and {destination_table} schema check for {job_name}')
        check_schema_result = validation_util.schema_table_validation(source, destination, source_table,
                                                                      destination_table)
        only_in_source_cols = check_schema_result['only_in_source_cols']
        only_in_destination_cols = check_schema_result['only_in_dest_cols']
        if len(only_in_source_cols) > 0 or len(only_in_destination_cols) > 0:
            cdc_event_table_name = f'{cdc_table_prefix}_{destination_table.split(".")[0]}_{destination_table.split(".")[1]}_clickzetta_cdc_event'
            schema_name = destination_table.split('.')[0]
            try:
                cdc_table_count = \
                    destination.execute_sql(f'select count(1) from {schema_name}.`{cdc_event_table_name}`')[0][
                        0]
            except Exception as e:
                logger.error(f'{job_name} get cdc table count for {cdc_event_table_name} error:', e)
                cdc_table_count = 0
            with sqlite3.connect(sqlite_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(schema_select_pattern, (source_table, destination_table))
                result = cursor.fetchone()
                if result:
                    cursor.execute(schema_update_pattern, (','.join(only_in_source_cols),
                                                           ','.join(only_in_destination_cols),
                                                           datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                                                           cdc_table_count,
                                                           source_table, destination_table))
                else:
                    cursor.execute(schema_insert_pattern, (source_table, destination_table,
                                                           ','.join(only_in_source_cols),
                                                           ','.join(only_in_destination_cols),
                                                           datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                                                           cdc_table_count, db_type))
        else:
            with sqlite3.connect(sqlite_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(schema_delete_pattern, (source_table, destination_table))
    except Exception as e:
        print(f'{job_name} schema check validation for table {source_table} error: {e}')
    except BaseException as e:
        print(f'{job_name} schema check validation for table {source_table} error: {e}')


def check_validation(job_id, source, destination, source_table, destination_table, pk_cols=None,
                     cdc_event_table_prefix=None, sqlite_db_file_path=None, db_type=None):
    logger.info(f'processing {source_table} and {destination_table} for {job_id}')
    try:
        source_count, dest_count, abs_count = validation_util.count_table_validation_without_df(source, destination,
                                                                                                source_table,
                                                                                                destination_table)
        if abs_count == 0:
            with sqlite3.connect(sqlite_db_file_path) as conn:
                cursor = conn.cursor()
                cursor.execute(delete_pattern, (source_table, destination_table))
            logger.info(
                f'{source_table} and {destination_table} for {job_id} are equal.Source_count: {source_count}, dest_count: {dest_count}')
            return
        assert pk_cols is not None, 'pk_cols is None'
        if abs_count > 0:
            check_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            assert cdc_event_table_prefix is not None, 'cdc_event_table_prefix is None'
            cdc_evnt_table_name = f'{cdc_event_table_prefix}_{destination_table.split(".")[0]}_{destination_table.split(".")[1]}_clickzetta_cdc_event'
            schema_name = destination_table.split('.')[0]
            try:
                max_cdc_time = \
                    destination.execute_sql(f'select max(server_ts) from {schema_name}.`{cdc_evnt_table_name}`')[0][0]
            except Exception as e:
                logger.error(f'{job_id} get max cdc time for {cdc_evnt_table_name} error:', e)
                max_cdc_time = 0
            if max_cdc_time == 0 or math.isnan(max_cdc_time):
                max_cdc_time_str = '1970-01-01 00:00:00.000000'
            else:
                max_cdc_time_str = datetime.fromtimestamp(int(max_cdc_time) / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')
            result_dict = validation_util.pk_id_table_validation_with_count(source, destination, source_table,
                                                                            destination_table, pk_cols, abs_count)
            result_dict['source_count'] = source_count
            result_dict['dest_count'] = dest_count
            result_dict['check_timestamp'] = check_timestamp
            map_key = f'{source_table}-{destination_table}'
            if map_key not in global_result_map:
                global_result_map[map_key] = []
            global_result_map[map_key].append(result_dict)
            status = 'DONE' if result_dict['check_status'] == 1 else 'UN_DONE'
            with sqlite3.connect(sqlite_db_file_path) as conn:
                cursor = conn.cursor()
                cursor.execute(select_pattern, (map_key.split('-')[0], map_key.split('-')[1]))
                result = cursor.fetchall()
                if len(result) == 0:
                    if int(result_dict['only_in_source']) == 0 and int(result_dict['only_in_dest']) == 0:
                        return
                    source_entries = ','.join(
                        '%s' % (str(entry).strip()) for entry in result_dict['only_in_source_list'])
                    if len(result_dict['only_in_source_list']) > 0:
                        source_entries = '1-{' + source_entries + '}'
                    dest_entries = ','.join('%s' % (str(entry).strip()) for entry in result_dict['only_in_dest_list'])
                    if len(result_dict['only_in_dest_list']) > 0:
                        dest_entries = '1-{' + dest_entries + '}'
                    cursor.execute(insert_pattern,
                                   (map_key.split('-')[0], map_key.split('-')[1], result_dict['source_count'],
                                    result_dict['dest_count'], status, result_dict['only_in_source'],
                                    result_dict['only_in_dest'], source_entries, dest_entries,
                                    '1',
                                    '1',
                                    result_dict['check_timestamp'], max_cdc_time_str, db_type))
                    return
                assert len(result) == 1, 'sqlite3 result length is not 1'
                for row in result:
                    only_in_source_list, only_in_dest_list = row
                source_map = {}
                dest_map = {}
                for entry in only_in_source_list.strip().split('|'):
                    if len(entry) == 0:
                        continue
                    count = int(entry.split('-')[0])
                    entries = entry.split('-')[1][1:][:-1].split(',')
                    for item in entries:
                        source_map[str(item).strip()] = count
                for entry in only_in_dest_list.strip().split('|'):
                    if len(entry) == 0:
                        continue
                    count = int(entry.split('-')[0])
                    entries = entry.split('-')[1][1:][:-1].split(',')
                    for item in entries:
                        dest_map[str(item).strip()] = count

                former_source_set = set(source_map.keys())
                former_dest_set = set(dest_map.keys())
                now_source_set = set(str(entry).strip() for entry in result_dict['only_in_source_list'])
                now_dest_set = set(str(entry).strip() for entry in result_dict['only_in_dest_list'])
                diff_source = former_source_set - now_source_set
                diff_dest = former_dest_set - now_dest_set

                for entry in result_dict['only_in_source_list']:
                    if str(entry) in source_map:
                        source_map[str(entry)] += 1
                    else:
                        source_map[str(entry)] = 1
                for entry in result_dict['only_in_dest_list']:
                    if str(entry) in dest_map:
                        dest_map[str(entry)] += 1
                    else:
                        dest_map[str(entry)] = 1
                for entry in diff_source:
                    source_map.pop(entry)
                for entry in diff_dest:
                    dest_map.pop(entry)
                sorted_source = sorted(source_map.items(), key=lambda x: x[1], reverse=True)
                sorted_dest = sorted(dest_map.items(), key=lambda x: x[1], reverse=True)
                temp_source_map = {}
                temp_dest_map = {}
                for index, entry in enumerate(sorted_source):
                    if entry[1] not in temp_source_map:
                        temp_source_map[entry[1]] = [str(entry[0]).strip()]
                    else:
                        temp_source_map[entry[1]].append(str(entry[0]).strip())
                for index, entry in enumerate(sorted_dest):
                    if entry[1] not in temp_dest_map:
                        temp_dest_map[entry[1]] = [str(entry[0]).strip()]
                    else:
                        temp_dest_map[entry[1]].append(str(entry[0]).strip())
                new_source_item = []
                new_dest_item = []
                for key, value in temp_source_map.items():
                    new_source_item.append(str(key) + '-{' + ','.join('%s' % (entry) for entry in value) + '}')

                for key, value in temp_dest_map.items():
                    new_dest_item.append(str(key) + '-{' + ','.join('%s' % (entry) for entry in value) + '}')
                cursor.execute(update_pattern, (result_dict['source_count'], result_dict['dest_count'],
                                                status, result_dict['only_in_source'],
                                                result_dict['only_in_dest'],
                                                '|'.join('%s' % (entry) for entry in new_source_item),
                                                '|'.join('%s' % (entry) for entry in new_dest_item),
                                                new_source_item[0].split('-')[0] if len(new_source_item) > 0 else ''
                                                , new_dest_item[0].split('-')[0] if len(new_dest_item) > 0 else '',
                                                result_dict['check_timestamp'],
                                                max_cdc_time_str, map_key.split('-')[0], map_key.split('-')[1]))
    except Exception as e:
        logger.error(f'{job_id} real-time validation for {source_table} error:', e)


def real_time_validate(job_name, source, destination, source_tables, destination_tables, pk_cols=None,
                       cdc_event_table_prefix=None, sqlite_db_file_path=None, db_type=None):
    if len(source_tables) != len(destination_tables):
        raise Exception("Source tables and destination tables should have the same length")
    uid = _format_job_id()
    logger.info(f"real-time validation for {job_name}_{uid} has been started")
    try:
        inner_executor_currency = 3
        executor = ThreadPoolExecutor(max_workers=inner_executor_currency)
        future_results = []
        for source_table, destination_table in zip(source_tables, destination_tables):
            future = executor.submit(check_validation, f"{job_name}_{uid}", source, destination, source_table,
                                     destination_table, pk_cols, cdc_event_table_prefix, sqlite_db_file_path, db_type)
            future_results.append(future)
            wait(future_results, None, return_when=ALL_COMPLETED)
        executor.shutdown(wait=True)
        logger.info(f"real-time validation for {job_name}_{uid} has been finished")
    except Exception as e:
        print(f'real-time validation for {job_name}_{uid} error:', e)


def real_time_schema_validate(job_name, source, destination, source_tables, destination_tables,
                              cdc_event_table_prefix=None, sqlite_db_file_path=None, db_type=None):
    if len(source_tables) != len(destination_tables):
        raise Exception("Source tables and destination tables should have the same length")
    uid = _format_job_id()
    logger.info(f"real-time schema validation for {job_name}_{uid} has been started")
    try:
        inner_executor_currency = 3
        executor = ThreadPoolExecutor(max_workers=inner_executor_currency)
        future_results = []
        for source_table, destination_table in zip(source_tables, destination_tables):
            future = executor.submit(schema_validation, f"{job_name}_{uid}", source, destination, source_table,
                                     destination_table, sqlite_db_file_path, cdc_event_table_prefix, db_type)
            future_results.append(future)
            wait(future_results, None, return_when=ALL_COMPLETED)
        executor.shutdown(wait=True)
        logger.info(f"real-time schema validation for {job_name}_{uid} has been finished")
    except Exception as e:
        print('real-time schema validation error:', e)


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


if __name__ == '__main__':
    try:
        while True:
            out_executor_currency = 8
            out_executor = ThreadPoolExecutor(max_workers=out_executor_currency)
            current_dir = os.path.dirname(os.path.realpath(__file__))
            schema_validation_sqlite_db = f"{current_dir}/sqlite_schema_validation.db"
            schema_db_exits = os.path.exists(schema_validation_sqlite_db)
            with sqlite3.connect(schema_validation_sqlite_db) as conn:
                if not schema_db_exits:
                    conn.execute(schema_real_time_table_ddl)
                    logger.info(f"schema validation sqlite db {schema_validation_sqlite_db} has been created")
            with open(f'{current_dir}/global_conf.json', 'r') as f:
                config = json.load(f)
            target_db_conf_path = config['target_db_conf_path']
            source_confs = config['source_conf']
            target_db_schema_name = config['target_db_schema_name']
            for conf in source_confs:
                name = conf['name']
                db_type = conf['db_type'].lower()
                db_conf_path = conf['db_conf_path']

                source_check_table_file_path = conf['source_check_table_file_path']
                target_check_table_file_path = conf['target_check_table_file_path']
                cz_cdc_table_prefix = conf['cz_cdc_table_prefix']
                pk_column = conf['pk_column']
                sqlite_db_name = f"sqlite_{name}_{db_type}.db"
                sqlite_db_file_path = f"{current_dir}/{sqlite_db_name}"
                sqlite_db_exists = os.path.exists(sqlite_db_file_path)
                with sqlite3.connect(sqlite_db_file_path) as conn:
                    if not sqlite_db_exists:
                        conn.execute(real_time_table_ddl)
                        logger.info(f"sqlite db {sqlite_db_file_path} has been created")
                source_engine_conf = json.load(open(db_conf_path))
                source = construct_source_engine(get_source_connection_params(source_engine_conf))
                destination_engine_conf = json.load(open(target_db_conf_path))
                destination = construct_destination_engine(get_destination_connection_params(destination_engine_conf))
                source_tables = get_source_tables(source_check_table_file_path)
                destination_tables = get_destination_tables(target_check_table_file_path, source_check_table_file_path,
                                                            target_db_schema_name)
                out_executor.submit(real_time_validate, name, source, destination, source_tables,
                                    destination_tables, pk_column, cz_cdc_table_prefix, sqlite_db_file_path, db_type)
                out_executor.submit(real_time_schema_validate, name, source, destination, source_tables,
                                    destination_tables, cz_cdc_table_prefix, schema_validation_sqlite_db, db_type)
                logger.info(f"real-time validation for {name} has been submitted")
            out_executor.shutdown(wait=True)
            sleep(7200)
    except Exception as e:
        logger.error(f'{datetime.now()} real-time validation error:', e)
