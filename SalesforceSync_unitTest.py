import unittest
import configSetting
import LoginAuthentication
import inspect


class SalesforceSyncTest(unittest.TestCase):

    def test_get_access_token(self):
        endpoint = configSetting.sf_oauth_endpoints['token_req']
        credential = configSetting.sf_oauth_cred
        result = LoginAuthentication.get_access_token(endpoint, credential)
        self.assertIsNotNone(result['access_token'])
        print(f"{inspect.currentframe().f_code.co_name} passed.")


def main():
    unittest.main()
