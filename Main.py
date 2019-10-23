import ExtractByObject
import LoginAuthentication
import CacheManager
import configSetting
import requests
from base64 import b64encode


def main():
    cm = CacheManager.CacheManager()
    job = ExtractByObject.create_bulk_query_job(access_token_obj=cm.cache['salesforce.com'], object_name="Account")

    pass


main()
