from contextlib import contextmanager
from os import sep
import logging
import psycopg2, psycopg2.pool
from psycopg2.extras import LoggingCursor
import ProdconfigSetting as configSetting
from io import StringIO
from typing import Iterable
import Util
from datetime import date, datetime


def load_rest_result(data: dict, connection: dict) -> None:
    """
    :param data: dict, key = status_code, url, data:{ totalSize, done, [records] }; records[n]:{attributes, field_1:value ... field_n}

    """
    if data['data']['records']:
        records = data['data']['records']
    else:
        logging.error('No records in data variable. Rest result not loaded.')


def load_to_postgres(connection: dict, data):
    pass


def file_to_postgres(connection, file_path: str, field_list: list) -> None:
    pass


def data_to_file(data, file_path: str, delimiter=configSetting.delimiter) -> None:
    """
    :param data: must be one of the data types in dict, list, set, tuple, or string.`
    :param file_path: ex. /dirctory/sf_[obj_name]_[yyyy_dd_mm]_n
    :param delimiter: char that separates the fields/columns
    :return: None
    """
    # TODO: Validate path and avoid duplicate file_name

    output = ""
    if isinstance(data, str):
        output = data
    elif isinstance(data, StringIO):
        output = data.getvalue()
    elif isinstance(data, Iterable):
        for item in data:
            if isinstance(item, Iterable):
                output += f"{Util.iterable_to_line(item)}\n"
            elif isinstance(item, str):
                output += f"{item}\n"
            else:
                logging.error(
                    f"Data element must be in string, list, dict, tuple, or set data type. Data is not output to {file_path}. Item = {str(item)}.")
    else:
        msg = f"obj Data is not in supported data type. Data = {str(data)}"
        logging.error(msg)
        print(msg)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(output)
    except Exception as err:
        logging.error(err)
        print(err)


def data_to_mem(data) -> StringIO:
    """
    :param data: Iterable (set, list, tuple)
    :return:  StringIO object in table-like format.
    """
    obj = StringIO()

    for item in data:
        obj.write(f"{Util.iterable_to_line(item)}\n")

    return obj


def data_to_insert_values(data: list) -> str:
    result = ""
    for item in data:
        row = ""
        for k in item.keys():

            if isinstance(item[k], (str, date, datetime)):
                row += f"'{item[k]}',"
            elif isinstance(item[k], type(None)):
                row += "Null,"
            else:
                row += f"{str(item[k])},"
        result += f"({row[:-1]}),"
        # result +="(" + ','.join([f"'{str(item[k])}'" for k in item.keys()]) + "),"
    return result[:-1]


@contextmanager
def cursor_op(conn_pool: psycopg2.pool.SimpleConnectionPool):
    conn = conn_pool.getconn()
    conn.autocommit = True
    # cur: psycopg2._psycopg.cursor = conn.cursor(cursor_factory=LoggingCursor)
    cur: psycopg2._psycopg.cursor = conn.cursor()
    try:
        yield conn, cur
    except Exception as err:
        logging.error(err)
        print(err)
    finally:
        cur.close()
        conn_pool.putconn(conn)
