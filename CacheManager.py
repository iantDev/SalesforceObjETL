import configSetting
import configparser


class CacheManager:
    """
    For .ini config file
    """

    def __init__(self, file_path=None):
        if file_path is None:
            self.file_path = configSetting.cache['file_path']
        else:
            self.file_path = file_path

        self.cache = configparser.ConfigParser()
        self.cache.read(self.file_path)

    def set_cache(self, section, options: dict):
        if not self.cache.has_section(section):
            self.cache.add_section(section)

         configparser.ConfigParser(self.cache).
            self.cache[section][key] = value

        with open(self.file_path, 'w') as f:
            self.cache.write(f)

