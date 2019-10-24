import configSetting
import configparser
import LoginAuthentication


class CacheManager:
    """
    For .ini config file

    Get cache value by .cache[section][option_key].
    Modify cache value by set_cache function.
    """

    def __init__(self, file_path=None):
        if file_path is None:
            self.file_path = configSetting.cache_file_path
        else:
            self.file_path = file_path

        self.proxy = configparser.ConfigParser()
        self.proxy.read(self.file_path)
        self.cache = self.proxy._sections

        if not self.proxy.has_option('salesforce.com', 'access_token'):
            result = LoginAuthentication.get_access_token()
            self.set_cache('salesforce.com', result)

    def set_cache(self, section, options: dict):
        if not self.proxy.has_section(section):
            self.proxy.add_section(section)
        else:
            existing_options = dict(self.proxy._sections[section])
            # for o in options:
            #     existing_options[o]=options[o]
            existing_options.update(options)

        self.proxy.update({section: existing_options})
        self.cache = self.proxy._sections
        self.write_to_file()

    def write_to_file(self):
        """
        Internal use for updating the local disk cache file.
        :return: None
        """
        with open(self.file_path, 'w') as f:
            self.proxy.write(f)
