import ProdconfigSetting as configSetting
import psycopg2
import datetime

db_config = configSetting.db['data_prod']


def get_conn_cur(db_config: dict = db_config) -> (psycopg2._psycopg.connection, psycopg2._psycopg.cursor):
    try:
        conn: psycopg2._psycopg.connection = psycopg2.connect(**db_config)
        cur = conn.cursor()
    except BaseException as e:
        # TODO logging
        print("Error getting postgres connection")
    return conn, cur


def table_last_timestamp(table_name: str, cur: psycopg2._psycopg.cursor) -> datetime.datetime:
    query = f"select SystemModstamp from public.{table_name} order by SystemModstamp desc limit 1;"
    print(query)
    cur.execute(query)
    last_ts = cur.fetchone()[0]
    return last_ts

# last_ts.strftime('%Y-%m-%d %H:%M:%S')

