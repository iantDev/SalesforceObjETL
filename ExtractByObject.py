import logging

from requests import Response

import configSetting
import requests
import datetime
import LoginAuthentication
import Util
import CacheManager
from collections import OrderedDict
from base64 import b64encode


def get_metadata(object_name=None, access_token=None):
    """
    Http get request to {instance].salesforce.com/services/data/vXX.X/sobjects/{objectName}/describe/
    :param object_name: Salesforce sObject name, ex. Account
    :param access_token: do not urlencode it
    :return: json (dict)
    """
    describe_path = f"/services/data/v{configSetting.api_version}/sobjects/{object_name}/describe/"

    if access_token is None:
        auth_result = LoginAuthentication.get_access_token(configSetting.sf_oauth_endpoints['token_req'], configSetting.sf_oauth_cred)
    endpoint = f"{auth_result['instance_url']}{describe_path}"
    header = configSetting.sf_bulk_api['header']
    header['Authorization'] = f"Bearer {auth_result['access_token']}"
    auth_header = {"Authorization": f"Bearer {auth_result['access_token']}"}
    result = requests.get(endpoint, headers=auth_header)
    metadata = result.json()
    return metadata


# metadata['fields']['Name']

def get_fields_from_sobject_metadata(sobject_describe, exclude_compound=False):
    """
    :param sobject_describe: json from rest api '/sobject/{object_name}/describe/'
    :param exclude_compound: compound fields not supported in Bulk API.
    :return: list of column names
    """
    all_fields = [item['name'] for item in sobject_describe['fields']]
    if not exclude_compound:
        return all_fields
    else:
        compound_fields = set([item['compoundFieldName'] for item in sobject_describe['fields']])
        return [f for f in all_fields if f not in compound_fields]


def bulk_query_request(access_token_obj: dict, object_name=None, fields=None, criteria_field=None, criteria_start_value=None, criteria_end_value=None, size=5000):
    """
    :param access_token_obj: Contain instance_url and access_token, which are handled by CacheManager.
    :param object_name: Salesforce Object, ex. Account.
    :param fields: Data fields separated by comma, ex. "field1, field2,...[field_n]".
    :param criteria_field: Delta extracting criteria field.
    :param criteria_start_value:
    :param criteria_end_value:
    :param size: Number of records/rows per batch.
    :return: dict with key = data, status_code, url

    Use "Authorization: Bearer <access_token_without_urlencoding>" when making Salesforce API calls.
    """
    if object_name is None:
        logging.error("Salesforce object name not provided. Exiting now...")
    if fields is None:
        fields = ', '.join(get_fields_from_sobject_metadata(get_metadata(object_name), exclude_compound=True))
    else:
        fields = fields
    if criteria_field is None:
        criteria = ""
    else:
        criteria = f"where {criteria_field} >= {criteria_start_value} and {criteria_field} < {criteria_end_value}"
    # format without line break and multiple spaces, not required.
    query = " ".join(f"select {fields} from {object_name} {criteria} limit {size}".split())

    request_element = {
        'header': configSetting.sf_bulk_api['header'],
        'body': configSetting.sf_bulk_api['body']
    }
    request_element['header']['Authorization'] = f"Bearer {access_token_obj['access_token']}"
    request_element['body']['query'] = query
    endpoint = access_token_obj['instance_url'] + configSetting.sf_bulk_api['uri_create_query_job']  # ex 'https://na136.salesforce.com/services/data/v47.0/jobs/query'

    print(datetime.datetime.now())
    try:
        response: Response = requests.post(endpoint, headers=request_element['header'], json=request_element['body'])
    except BaseException as err:
        # TODO Create logging and notification
        print(f"Exception occurred: {datetime.datetime.now()}")
        print(f"Error: {err}")
        print('EOL')
    finally:
        print(f"End of request try block: {datetime.datetime.now()}")

    return Util.format_response(response)


def get_bulk_query_result(job_id, access_token_obj: dict) -> dict:
    """
    :param job_id: bulk api query job
    :param access_token_obj: key = instance_url, access_token
    :return: dict, key = data, status_code, url
    """
    instance_url = access_token_obj['instance_url']
    endpoint = f"{instance_url}{configSetting.sf_bulk_api['bulk_operation']['uri_get_query_job_result']}"
    auth_header = {'Authorization': f"Bearer {access_token_obj['access_token']}"}
    response = requests.get(endpoint, headers=auth_header)
    return Util.format_response(response)


def rest_query_request(query: str, access_token_obj: dict) -> dict:
    """
    :param query: SOQL statment, ex. select name from Account
    :param access_token_obj: key = instance_url, access_token
    :return: dict, key = data, status_code, url
    """
    query = f"q={query}"
    endpoint = f"{access_token_obj['instance_url']}{configSetting.sf_rest_api['uri']}"
    try:
        response = requests.get(endpoint, params=query, headers={'Authorization': f'Bearer {access_token_obj["access_token"]}'})
    except BaseException as err:
        # TODO Create logging and notification
        logging.error(f"Error with rest query request: {err}")
    return Util.format_response(response)


def get_bulk_query_job_info(access_token_obj: dict, job_id: str = None) -> dict:
    """
    :param access_token_obj: dict, keys = instance_url, access_token, id
    :param job_id: when not supplied, all info of the query jobs are returned.
    :return: dict, keys = data:dict, status_code, url" ["data"].keys = done:boolean, nextRecordsUrl: (None,str), records:[]
    """
    # TODO: Create handling for all query job info return, where ['data']['done'] = false and use ['data']['nextRecordsUrl'] as rest input for the subsequent records.
    endpoint = f"{access_token_obj['instance_url']}{configSetting.sf_bulk_api['uri_get_query_job']}"
    if job_id:
        endpoint = f"{access_token_obj['instance_url']}{configSetting.sf_bulk_api['uri_get_query_job']}{job_id}"

    params = {
        # 'isPkChunkingEnabled': "false",
        'jobType': 'V2Query'
    }
    headers = {
        "Authorization": f"OAuth {access_token_obj['access_token']}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(endpoint, params=params, headers=headers)
    except BaseException as err:
        # TODO log to file
        logging.error(f"Get all bulk query job info error: {err}")
    return Util.format_response(response)
