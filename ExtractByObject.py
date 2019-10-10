import logging
import configSetting
import requests

def get_object_data( object_name=None,fields=None,delta_field=None, delta_last_value=None):
    if object_name is None:
        logging.error("Salesforce object name not provided. Exiting now...")
    if fields is None:
        fields = configSetting.sf_data_fields[object_name]

    query = f"select {fields} from {object_name} limit 10"


    pass
