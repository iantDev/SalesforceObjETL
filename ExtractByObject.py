import logging
import configSetting
import requests
import datetime
import LoginAuthentication
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
    print(metadata)
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


def create_bulk_query_job(access_token_obj: dict, object_name=None, fields=None, criteria_field=None, criteria_start_value=None, criteria_end_value=None, size=5000):
    """
    :param access_token_obj: Contain instance_url and access_token, which are handled by CacheManager.
    :param object_name: Salesforce Object, ex. Account.
    :param fields: Data fields separated by comma, ex. "field1, field2,...[field_n]".
    :param criteria_field: Delta extracting criteria field.
    :param criteria_start_value:
    :param criteria_end_value:
    :param size: Number of records/rows per batch.

    :return: dictionary dataset.

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

    endpoint = access_token_obj['instance_url'] + configSetting.sf_bulk_api['uri_create_query_job']  # 'https://na136.salesforce.com/services/data/v47.0/jobs/query'

    request_element['header']['Authorization'] = f"Bearer {access_token_obj['access_token']}"
    request_element['body']['query'] = query

    print(datetime.datetime.now())
    try:
        req = requests.post(endpoint, headers=request_element['header'], json=request_element['body'])
    except BaseException as err:
        # TODO Create logging and notification
        print(f"Exception occurred: {datetime.datetime.now()}")
        print(f"Error: {err}")
        print('EOL')
    finally:
        print(f"End of request try block: {datetime.datetime.now()}")

    return req.json()


def get_bulk_query_result(job_id, access_token_obj: dict):
    instance_url = access_token_obj['instance_url']
    endpoint = f"{instance_url}{configSetting.sf_bulk_api['uri_get_query_job_result']}"
    auth_header = {'Authorization': f"Bearer {access_token_obj['access_token']}"}
    result = requests.get(endpoint, headers=auth_header)
    return result.json()
