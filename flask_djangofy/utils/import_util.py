import importlib


class ImportUtil(object):
    """
    Utility to import class/variable/function/module by string
    """
    def __init__(self, key, key_type='module'):
        self.key = key
        self.type = key_type

    def get(self):
        """
        Import by key type
        :return:
        """
        return getattr(self, 'import_{type}'.format(type=self.type))()

    def import_module(self):
        """
        Import a module
        :return: module
        """
        return importlib.import_module(self.key)

    def __import(self):
        """
        Import class/function/variable
        :return:
        """
        module_path, module_cfv = self.key.rsplit('.', 1)
        module_object = importlib.import_module(module_path)
        return getattr(module_object, module_cfv)

    def import_function(self):
        """
        Import function
        :return: function
        """
        return self.__import()

    def import_class(self):
        """
        Import class
        :return: class
        """
        return self.__import()

    def import_variable(self):
        """
        Import variable
        :return: variable
        """
        return self.__import()

