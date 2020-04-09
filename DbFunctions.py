import ProdconfigSetting as configSetting
import psycopg2
import datetime
import pytz

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
    """
    Return latest SystemModstamp in a given table name in Salesforce database in Postgres. IF result is none, return 1980-01-01T00:00:00+0000 timestamp.
    :param table_name: table name in Salesforce database.
    :param cur: Pyscopy2 cursor object.
    :return: datetime.
    """
    query = f"select SystemModstamp from public.{table_name} order by SystemModstamp desc limit 1;"
    print(query)
    cur.execute(query)
    result = cur.fetchone()
    if result is not None:
        return result[0]
    else:
        return datetime.datetime(year=1980,month=1,day=1,hour=0,minute=0,second=0,tzinfo=pytz.timezone('UTC'))

# last_ts.strftime('%Y-%m-%d %H:%M:%S')

