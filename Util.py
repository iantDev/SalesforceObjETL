from requests import Response
import CacheManager
import LoginAuthentication
import logging
import urllib
from typing import Iterable


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


def iterable_to_line(item, delimiter="|") -> str:
    if isinstance(item, (list,set,tuple)):
        return delimiter.join(map(str,item))
    elif isinstance(item, dict):
        return delimiter.join(str(v) for v in item.values())
    else:
        logging.error(f"Item is not a dict or iterable data type list, set, or tuple. Item = {str(item)}")
        return ""
