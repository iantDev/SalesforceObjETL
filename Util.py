from requests import Response
import CacheManager
import LoginAuthentication
import logging
import urllib
from typing import Iterable
import ProdconfigSetting as configSetting
import json


def format_response(response: Response) -> dict:
    """
    keys = data, status_code, url
    """
    urldecode = urllib.parse.unquote_plus(response.url)
    data = response.json()
    if isinstance(data, (list, tuple)):
        data = data[0]
    return {"data": data, "status_code": response.status_code, "url": urldecode}


def response_handler(response: Response):
    content = response.json()
    if response.status_code == '401':  # The session ID or OAuth token used has expired or is invalid.
        result = LoginAuthentication.get_access_token()
        cm = CacheManager.CacheManager()
        cm.append_cache('salesforce.com', result)
    elif response.status_code == '400':
        # TODO: set up log file
        logging.error(response.text)
    elif response.status_code == "403":
        if content['message'] == "REQUEST_LIMIT_EXCEEDED":
            # TODO: send notification (email and/or slack) in addition to logging
            pass
        else:
            logging.error('Verify that the logged-in user has appropriate permissions.', response.text)
    elif response.status_code == '200':
        return response.json()


def get_by_path(item, nested_path: Iterable):
    for level in nested_path:
        parent = item
        item = item[level]
    return item


def iterable_to_line(item, delimiter=configSetting.delimiter) -> str:
    if isinstance(item, (list, set, tuple)):
        return delimiter.join(map(str, item)).replace('\r', ' ').replace('\n', ' ').replace('\\', ' ')
    elif isinstance(item, dict):
        return delimiter.join(str(v) for v in item.values()).replace('\r', ' ').replace('\n', ' ').replace('\\', ' ')
    else:
        logging.error(f"Item is not an iterable data type in dict, list, set, or tuple. Item = {str(item)}")
        return ""

def filter_schema(schema:dict, field_path:list, key_to_look:set, file_path:str = None):
    schema_info: list = get_by_path(schema, field_path)
    fields_schema = dict(enumerate([{k: v for k, v in item.items() if k in key_to_look} for item in schema_info]))
    if file_path:
        with open(file_path, 'w') as f:
            f.write(json.dumps(fields_schema), indent='\t')

def print_db_col_def(col_def: dict, col_key_name:str, col_data_type_key_name:str, data_type_mapping: dict):
    for field in col_def:
        if field[col_data_type_key_name] in data_type_mapping.keys():
            print(f"{field[col_key_name]} {data_type_mapping[field[col_data_type_key_name]]} Null,")
        else:
            print(f"{field[col_key_name]} {field[col_data_type_key_name]} Null,")