import inspect

from flask_djangofy.conf import global_settings


class Config(object):
    """
    App Config Class
    This class process configuration by merging default settings and user defined settings
    """
    def __init__(self, setting_module=None):
        self.setting_module = setting_module

    def _set_default_settings(self):
        """
        Set default settings
        """
        attributes = [x for x in dir(global_settings) if not x.startswith('__')]
        self.__set_settings(attributes, global_settings)

    def __set_settings(self, settings, setting_module):
        """
        Pick settings from provided settings module and set in config object
        :param settings:
        :param setting_module:
        :return:
        """
        for attribute in settings:
            if not inspect.ismodule(getattr(setting_module, attribute)):
                setattr(self, attribute, getattr(setting_module, attribute))

    def process(self):
        """
        Merge default and user defined settings to make a single configuration object
        :return: configurations
        :rtype Config
        """
        self._set_default_settings()
        project_settings = [x for x in dir(self.setting_module) if not x.startswith('__')]
        self.__set_settings(project_settings, self.setting_module)
        del self.setting_module
        return self
