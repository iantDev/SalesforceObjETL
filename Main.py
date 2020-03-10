import ExtractByObject,LoadData, LoginAuthentication, Util
import ProdconfigSetting as configSetting
import psycopg2.pool
import DbFunctions
from os import sep
# from airflow import DAG

def get_sf_data(query: str,access_token_obj :dict) -> list:
    result = ExtractByObject.rest_query_request(query,access_token_obj)
    # TODO: Http status handling
    data : list = Util.get_by_path(result,configSetting.sf_rest_result_path_list['records'])
    while True:
        try:
            # ex. '/services/data/v47.0/query/01g0M000067owIlQAI-2000'
            next_Records_Url = Util.get_by_path(result,configSetting.sf_rest_result_path_list['nextRecordsUrl'])
            endpoint = f"{access_token_obj['instance_url']}{next_Records_Url}"
            result = ExtractByObject.rest_query_request(query=None, access_token_obj=access_token_obj,
                                                        endpoint=endpoint)
            data = [*data , *(Util.get_by_path(result, configSetting.sf_rest_result_path_list['records']))]
        except:
            break
    return data


def main():
    obj_names = configSetting.sobject_to_process
    for obj_name in obj_names:
        access_token_obj = LoginAuthentication.get_access_token()
        conn, cur = DbFunctions.get_conn_cur()
        timestamp = DbFunctions.table_last_timestamp(obj_name, cur)
        query = f"select {configSetting.sf_data_fields[obj_name]} from {obj_name} where SystemModstamp>={timestamp.strftime('%Y-%m-%dT%H:%M:%S%z')}"
        data = get_sf_data(query, access_token_obj)

        [item.pop('attributes') for item in data if 'attributes' in item]
        mem_obj = LoadData.data_to_mem(data)
        obj = mem_obj.getvalue()
        conn_pool: psycopg2.pool.SimpleConnectionPool = psycopg2.pool.SimpleConnectionPool(1, 10,
                                                                                           **configSetting.db['data_prod'])
        mem_obj.seek(0)
        with LoadData.cursor_op(conn_pool) as (conn, cur):
            cur.execute(f"truncate table stg.{obj_name};")
            cur.copy_from(mem_obj, f'stg.{obj_name}', sep=configSetting.delimiter, null='None',
                          columns=[i.strip(' \t\n\r') for i in configSetting.sf_data_fields[obj_name].split(",")])
            cur.execute(f" select stg.proc_{obj_name.lower()}_update_from_stg()" )

    # TODO: handling non-200 response
    # if response.status_code == 401:  # The session ID or OAuth token used has expired or is invalid.
    #     access_token_obj = LoginAuthentication.get_access_token()
    #     cm.append_cache('salesforce.com', access_token_obj)
    #     # TODO: Implement better way to handle the looping of error responses.
    #     response = ExtractByObject.bulk_query_request(access_token_obj=cm.cache['salesforce.com'], object_name="Account", size=100)
    # data = response.json()

main()
