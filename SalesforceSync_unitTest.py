import unittest
import configSetting
import LoginAuthentication
import inspect
import CacheManager


class SalesforceSyncTest(unittest.TestCase):

    def test_get_access_token(self):
        endpoint = configSetting.sf_oauth_endpoints['token_req']
        credential = configSetting.sf_oauth_cred
        result = LoginAuthentication.get_access_token(endpoint, credential)
        self.assertIsNotNone(result['access_token_obj'])
        print(f"{inspect.currentframe().f_code.co_name} passed.")

    def test_set_access_token_expired(self):
        pass


class CacheManagerTest(unittest.TestCase):

    def test_set_cache_with_existing_section(self):
        cm = CacheManager.CacheManager()
        test_options = {'key1': 'value1', 'key2': "value2"}
        cm.append_cache(section='salesforce.com', options=test_options)
        expect_values = {'salesfroce.com': test_options}
        self.assertIn(expect_values, cm.cache)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(CacheManagerTest('test_set_cache_with_existing_section'))


def main():
    # unittest.main()
    runner = unittest.TestRunner()
    runner.run(suite())
