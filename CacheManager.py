import ProdconfigSetting as configSetting
import configparser
import LoginAuthentication


class CacheManager:
    """
    For .ini config file

    Get cache value by .cache[section][option_key].
    Modify cache value by append_cache or reset_cache function.
    """

    def __init__(self, section: str = None, options: dict = None, file_path=None):
        """
        :param file_path: path and cache file name.
        :param section: required if options have value.
        :param options: will append to existing options. Use reset_cache to clear the section that would only have the parameter options.
        """
        if file_path is None:
            self.file_path = configSetting.cache_file_path
        else:
            self.file_path = file_path

        self.proxy = configparser.ConfigParser()
        self.proxy.read(self.file_path)
        if section and options:
            self.append_cache(section, options)
        self.cache = self.proxy._sections

    def append_cache(self, section, options: dict):
        if not self.proxy.has_section(section):
            self.proxy.add_section(section)
            options_to_update = options
        else:
            options_to_update = dict(self.proxy._sections[section])
            options_to_update.update(options)

        self.proxy.update({section: options_to_update})
        self.cache = self.proxy._sections
        self.write_to_file()

    def reset_cache(self, section, options: dict):
        if not self.proxy.has_section(section):
            self.proxy.add_section(section)
        self.proxy.update({section: options})
        self.cache = self.proxy._sections
        self.write_to_file()

    def write_to_file(self):
        """
        Internal use for updating the local disk cache file.
        :return: None
        """
        with open(self.file_path, 'w') as f:
            self.proxy.write(f)
