import requests
import ProdconfigSetting as configSetting
import CacheManager
import logging
from datetime import datetime, timedelta

# grant_type = configSetting.SF_OAuth['grant_type']
# client_id = configSetting.SF_OAuth['client_id']
# client_secret = configSetting.SF_OAuth['client_secret']
# username = configSetting.SF_OAuth['username']
# password = configSetting.SF_OAuth['password']

def get_access_token(endpoint=None, credential=None):
    """Read from cache or retrieve from endpoint with credential.
    :param endpoint: token request URI, ex. https://login.salesforce.com/services/oauth2/token
    :param credential:
        'grant_type': 'password',
        'client_id': <from API setting>,
    'client_secret': <from API setting>,
    'username': <login>,
    'password': <password>
    :return: dictionary {'access_token_obj':<token>, 'instance_url:<url>, 'id':<id>, 'token_type':'Bearer'}
    """
    cm = CacheManager.CacheManager()
    if datetime.fromisoformat(cm.cache['access_token_obj']['issued_datetime']) + timedelta(hours=1) > datetime.now().astimezone():
        return cm.cache['access_token_obj']

    if endpoint is None:
        token_req_endpoint = configSetting.sf_oauth_endpoints['token_req']
        credential = configSetting.sf_oauth_cred
    else:
        token_req_endpoint = endpoint

    with requests.session() as s:
        req = s.post(token_req_endpoint, params=credential)
    result = req.json()

    if result['access_token']:
        #
        # timestamp = datetime.now().astimezone()
        # utcTime = timestamp.utcfromtimestamp(timestamp.timestamp())
        result['issued_datetime'] = datetime.fromtimestamp(float(result['issued_at']) / 1e3).astimezone()
        result['issued_UTCdatetime'] = datetime.utcfromtimestamp(result['issued_datetime'].timestamp())
        cm.reset_cache('access_token_obj', result)
        return result
    else:
        logging.error(f"No access token return: {result}")
        exit(SystemExit())


def set_access_token_expired(cache_manager: CacheManager = None):
    if cache_manager is None:
        cache_manager = CacheManager.CacheManager()
    cache_manager.cache.remove_option('salesforce.com', 'access_token_obj')
    cache_manager.write_to_file()
