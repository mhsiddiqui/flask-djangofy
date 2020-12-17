from flask_djangofy import app
from .include import ModuleUrlIncluder


class Url(object):
    """
    Url class to define urls

    Parameters
    ---
    url: Url string
    view: view function/class or module url includer
    """
    def __init__(self, url=None, view=None, name=''):
        assert url is not None, "Url is required"
        assert view is not None, "View is required"
        self.url = url
        self.view = view
        self.name = name
        self.app_name = None
        self.base = '/'
        if not isinstance(self.view, ModuleUrlIncluder) and not self.app_name:
            self.app_name = 'root'
        if isinstance(self.view, ModuleUrlIncluder):
            self.set_app(self.view.app_name)

    def __str__(self):
        """
        String representation of url
        :return: representation
        :rtype str
        """
        return '<url {view} ({url})>'.format(view=self._get_name(), url=self._get_url())

    def get_app(self):
        """
        Get url app
        :return: url app
        :rtype str
        """
        return self.app_name

    def set_app(self, app_name):
        """
        Set url app
        :param str app_name: name of app
        """
        self.app_name = app_name

    def set_base(self, base):
        """
        Set base url
        :param str base: base url
        """
        self.base = base

    def _get_name(self):
        """
        Get name of view
        :return: name of view
        :rtype str
        """
        if self.name:
            return self.name
        else:
            return '{module}:{name}'.format(module=self.app_name, name=self.view.__name__)

    def get_urls(self):
        """
        Get list of urls
        If view is module includer, then return all urls of that module. Otherwise return list of current url
        :return: list of urls
        :rtype list
        """
        if isinstance(self.view, ModuleUrlIncluder):
            self.view.set_base(self.url)
            module_urls = self.view.get_urls()
            app.logger.info('{count} urls found in {app_name}'.format(
                count=len(module_urls), app_name=self.app_name)
            )
            return module_urls
        else:
            return [self]

    def _get_url(self):
        """
        Construct url using base and url
        :return: url
        :rtype str
        """
        return '{base}{url}'.format(base=self.base, url=self.url).replace('//', '/')

    def initialize(self):
        """
        Add route rules in app
        """
        app.add_url_rule(self._get_url(), self._get_name(), view_func=self.view)
