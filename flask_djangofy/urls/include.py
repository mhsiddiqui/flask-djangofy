from flask_djangofy.utils.module_loading import import_string


class ModuleUrlIncluder(object):
    """
    Module Url Includer class
    """
    def __init__(self, app_name, namespace):
        assert app_name is not None, "app_name is required"
        assert namespace is not None, "namespace is required"
        self.app_name = app_name
        self.namespace = namespace
        self.base = None

    def get_app(self):
        return self.app_name

    def set_base(self, base):
        self.base = base

    def get_urls(self):
        module_urls = import_string('{namespace}.urlpatterns'.format(namespace=self.namespace))
        for url in module_urls:
            url.set_base(self.base)
            url.set_app(self.app_name)
        return module_urls
