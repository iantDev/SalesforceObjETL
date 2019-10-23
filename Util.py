from requests import Response
import CacheManager
import LoginAuthentication
import logging


def response_handler(response: Response):
    content = response.json()
    if response.status_code == '401':  # The session ID or OAuth token used has expired or is invalid.
        result = LoginAuthentication.get_access_token()
        cm = CacheManager.CacheManager()
        cm.set_cache('salesforce.com', result)
    elif response.status_code == '400':
        # TODO: set up log file
        logging.error(response.text)
    elif response.status_code == "403":
        if content['message'] == "REQUEST_LIMIT_EXCEEDED":
            # TODO: send notification (email and/or slack) in addition to logging
            pass
        else:
            logging.error('Verify that the logged-in user has appropriate permissions.', response.text)
