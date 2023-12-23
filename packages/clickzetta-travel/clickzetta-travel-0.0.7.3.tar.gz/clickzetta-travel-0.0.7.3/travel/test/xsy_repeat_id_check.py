import sys

from clickzetta.client import Client
from clickzetta.dbapi.connection import Connection

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check(destination_tables: list):
    try:
        client = Client(
            cz_url="clickzetta://test_02:Axshouyi123@3118b2bc.ap-shanghai-tencentcloud.api.clickzetta.com/xsy_gray?virtualcluster=DI_GP&schema=xsy_bi_v2")
        conn = Connection(client)

        cursor = conn.cursor()
        for table in destination_tables:
            logger.info(f"Checking table {table}")
            sql = f"select id, cnt from (select id, count(1) as cnt from {table} group by id) where cnt > 1;"
            try:
                cursor.execute(sql)
            except Exception as e:
                logger.error(e)
                continue
            results = cursor.fetchall()
            if len(results) > 0:
                logger.error(f"Table {table} has duplicate ids, count:{len(results)}")
    except Exception as e:
        logger.error(e)


def get_destination_tables(destination_tables_file):
    destination_tables = []
    with open(destination_tables_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            destination_tables.append(line.strip())
    return destination_tables


if __name__ == '__main__':
    destination_tables_file = sys.argv[1]
    destination_tables = get_destination_tables(destination_tables_file)
    check(destination_tables)
