import requests
import configSetting
import logging


# ###  Testing zeep soap WSDL ###
# client = zeep.Client(wsdl='http://www.soapclient.com/xml/soapresponder.wsdl')
# print(client.service.Method1("zeep", "trying the package"))

# soap_client = zeep.Client(wsdl=configSetting.file_path['salesforce_WSDL'])

# grant_type = configSetting.SF_OAuth['grant_type']
# client_id = configSetting.SF_OAuth['client_id']
# client_secret = configSetting.SF_OAuth['client_secret']
# username = configSetting.SF_OAuth['username']
# password = configSetting.SF_OAuth['password']

def get_access_token_json(endpoint=None, credential=None):
    """

    :param endpoint: token request URI, ex. https://login.salesforce.com/services/oauth2/token
    :param credential:
        'grant_type': 'password',
        'client_id': <from API setting>,
    'client_secret': <from API setting>,
    'username': <login>,
    'password': <password>
    :return: dictionary {'access_token':<token>, 'instance_url:<url>, 'id':<id>, 'token_type':'Bearer'}
    """
    if endpoint is None:
        token_req_endpoint = configSetting.sf_oauth_endpoints['token_req']
        credential = configSetting.sf_oauth_cred
    else:
        token_req_endpoint = endpoint

    req = requests.post(token_req_endpoint, params=credential)
    result = req.json()
    if result['access_token'] is None:
        logging.error(f"No access return: {result}")
    else:
        return result
