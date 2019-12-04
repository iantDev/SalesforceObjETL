import ExtractByObject
import LoginAuthentication
import CacheManager
import configSetting
import requests
from base64 import b64encode
from pathlib import Path
from airflow import DAG


def main():
    cm = CacheManager.CacheManager()
    response = ExtractByObject.bulk_query_request(access_token_obj=cm.cache['salesforce.com'], object_name="Account", size=100)

    if response.status_code == 401:  # The session ID or OAuth token used has expired or is invalid.
        access_token_obj = LoginAuthentication.get_access_token()
        cm.append_cache('salesforce.com', access_token_obj)
        # TODO: Implement better way to handle the looping of error responses.
        response = ExtractByObject.bulk_query_request(access_token_obj=cm.cache['salesforce.com'], object_name="Account", size=100)
    data = response.json()

    home_dir = str(Path.home())
    anchor = Path.home().anchor
    file_path = f"{home_dir}{anchor}Downloads{anchor}sfAccountData.txt"
    with open(file_path, "w") as f:
        f.write(data)


main()
