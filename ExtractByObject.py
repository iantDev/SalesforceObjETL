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


def create_bulk_query_job(object_name=None, fields=None, criteria_field=None, criteria_start_value=None, criteria_end_value=None, size=5000, access_token=None):
    """
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

    # TODO Access_token_object local copy: should be saved in a file as cache. Response parsing for when to run LoginAuthentication.get_access_token.
    if access_token is None:
        response = LoginAuthentication.get_access_token(configSetting.sf_oauth_endpoints['token_req'], configSetting.sf_oauth_cred)
        access_token = response['access_token']
        instance_url = response['instance_url']

    request_element = {
        'header': configSetting.sf_bulk_api['header'],
        'body': configSetting.sf_bulk_api['body']
    }

    endpoint = instance_url + configSetting.sf_bulk_api['uri_create_query_job']  # 'https://na136.salesforce.com/services/data/v47.0/jobs/query'

    request_element['header']['Authorization'] = f"Bearer {access_token}"
    request_element['body']['query'] = query

    print(datetime.datetime.now())
    try:
        req = requests.post(endpoint, headers=request_element['header'], json=request_element['body'])
        cache = CacheManager.CacheManager()
        [cache.set_cache(section=req['id'], key=key, value=req[key]) for key in req.keys()]

    except BaseException as err:
        # TODO Create logging and notification
        print(f"Exception occurred: {datetime.datetime.now()}")
        print(f"Error: {err}")
        print('EOL')
    finally:
        print(f"End of request try block: {datetime.datetime.now()}")

    # req = requests.post(endpoint, headers=request_element['header'], data=request_element['body'])
    # req_params = configSetting.sf_bulk_api['header_test']
    # req_params.update(request_element['body'])
    # req_params['Host'] = instance_url
    # # req_params['Authorization'] = "Bearer {}".format(b64encode(access_token.encode('utf-8')).decode('utf-8'))
    # auth_header = {'Authorization': 'Bearer {}'.format(b64encode(access_token.encode('utf-8')).decode('utf-8'))}
    # # auth_header = {'X-SFDC-Session': b64encode(access_token.encode('utf-8')).decode('utf-8')}
    # req = requests.post(endpoint, headers=auth_header, params=req_params, verify=False)
    return req.json()


def get_bulk_query_result(job_id, access_token=None):
    # TODO Update to local cache when available.
    instance_url = configSetting.sf_cache['instance_url']
    endpoint = f"{instance_url}{configSetting.sf_bulk_api['uri_get_query_job_result']}"
    if access_token is None:
        # TODO update when local cache is available.
        token = configSetting.sf_access_token

        auth_header = {'Authorization': f'Bearer {configSetting.sf_access_token}'}

    result = requests.get(endpoint, headers=auth_header)

    return result.json()


def get_last_element(obj):
    if isinstance(obj, (list, tuple, set)):
        return obj[-1]
    if isinstance(OrderedDict):
        key = next(reversed(obj.keys()))
        return obj[key]

    pass


def test_access_token_for_access():
    auth_result = LoginAuthentication.get_access_token(configSetting.sf_oauth_endpoints['token_req'], configSetting.sf_oauth_cred)
    endpoint = auth_result['instance_url'] + "/services/data/v47.0/sobjects/"
    # token_encoded = b64encode(auth_result['access_token'].encode('utf-8')).decode('utf-8')
    auth_header = {"Authorization": f"Bearer {auth_result['access_token']}"}
    # params = {"scope": "web"}
    # cookies = auth_result['session'].cookies
    # for i in cookies:
    #     print(i.domain, i.name, i.value)
    # items = cookies.list_domains()[0]
    # c_items = cookies._cookies
    # cookies.set("SID", auth_result['access_token'], domain=cookies.list_domains()[0])

    # s = auth_result['session']
    # s.cookies = cookies
    result = requests.get(endpoint, headers=auth_header, verify=False)

    # with requests.session() as s:
    #     result = s.get(endpoint, headers=auth_header, cookies=cookies, verify=False)
    # # result = requests.get(endpoint, auth=auth_header, cookies=cookies)
    result.json()
    print(result)
    pass
