import ExtractByObject
import LoginAuthentication
import CacheManager
import configSetting
import requests
from base64 import b64encode


def main():
    access_token = LoginAuthentication.get_access_token()
    cm = CacheManager.CacheManager()
    url = cm.cache['salesforce.com']['instance_url']

    # data = ExtractByObject.create_bulk_query_job(object_name="Account", size=20)
    data = ExtractByObject.get_bulk_query_result(job_id="7504T000000RwkeQAC")
    if data['errorCode']:
        if data['errorCode'] == "INVALID_SESSION_ID":
            access_token_obj = LoginAuthentication.get_access_token(configSetting.sf_oauth_endpoints['token_req'],configSetting.sf_oauth_cred)
            ExtractByObject.get_bulk_query_result()

    with open("Account_query.txt", "w") as f:
        f.write(data)
    # ExtractByObject.test_access_token_for_access()
    # metadata = ExtractByObject.get_metadata('Account')
    print('end of line')


def main_old():
    with requests.session() as s:
        req = s.post(token_req_endpoint, params=credential)
        auth_result = req.json()

        endpoint = auth_result['instance_url'] + "/services/data/v47.0/sobjects/"
        token_encoded = b64encode(auth_result['access_token'].encode('utf-8')).decode('utf-8')
        # auth_header = {"Authorization": f"Bearer {token_encoded}"}
        auth_header = {"Authorization": f"Bearer {auth_result['access_token']}"}
        params = {"scope": "web"}
        cookies = s.cookies
        cookies_empty = requests.cookies.RequestsCookieJar()
        for i in cookies:
            print(i.domain, i.name, i.value)
        # items = cookies.list_domains()[0]
        # c_items = cookies._cookies
        cookies_empty.set("SID", auth_result['access_token'], domain=cookies.list_domains()[0])
        cookies.set("SID", auth_result['access_token'], domain=cookies.list_domains()[0])

        result = requests.get(endpoint, headers=auth_header, verify=False)

        s.cookies = cookies_empty
        result = s.get(endpoint, headers=auth_header, params=params, verify=False)

        print(result)
        pass


main()
# curl https://na136.salesforce.com/services/data/v47.0/sobjects/ -H "Authorization: Bearer MDBENFQwMDAwMDBEUldNIUFRb0FRQ0tyelJtbVpUaGJOVEZHN1BQOU5JNk9IM0JnRFQ5RGJVS0JJUENnY1V5NkpiWWxwRHMwNlNJeDhzdWxPZjIydnJIWGUwZ0VoMEI0eF9Eb0h5Vjcuc0NYWDlGVw=="
# curl https://na136.salesforce.com/services/data/v47.0/sobjects/ -H "Authorization: OAuth MDBENFQwMDAwMDBEUldNIUFRb0FRQ0tyelJtbVpUaGJOVEZHN1BQOU5JNk9IM0JnRFQ5RGJVS0JJUENnY1V5NkpiWWxwRHMwNlNJeDhzdWxPZjIydnJIWGUwZ0VoMEI0eF9Eb0h5Vjcuc0NYWDlGVw=="

# curl https://na136.salesforce.com/services/data/v47.0/sobjects/ -H 'Authorization: Bearer 00D4T000000DRWM!AQoAQBD8RaKDdgKTy3PJgB0kq1iEQ7dhkwIo9wMNOEAYYWdpifvhedwO2O8S4GKP1c1p6ilCpDR0K0YKDhRfWb1l4oToHUNf'
# curl https://na136.salesforce.com/services/data/v47.0/sobjects/ -H 'Authorization: OAuth 00D4T000000DRWM!AQoAQCKrzRmmZThbNTFG7PP9NI6OH3BgDT9DbUKBIPCgcUy6JbYlpDs06SIx8sulOf22vrHXe0gEh0B4x_DoHyV7.sCXX9FW'

# b'[{"errorCode":"API_ERROR","message":"Selecting compound data not supported in Bulk Query"}]'
