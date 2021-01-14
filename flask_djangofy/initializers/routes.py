import os
import sys

from flask_djangofy.conf import settings

from flask_djangofy.initializers.base import BaseInitializer
from flask_djangofy.utils.module_loading import import_string


def default_urlconf():
    """Create an empty URLconf 404 error response."""
    import flask_djangofy
    from jinja2 import Template
    with open(os.path.join(flask_djangofy.__path__[0], 'templates', 'default_urlconf.html'), 'r+') as f:
        content = f.read()
    template = Template(content)
    context = {
        'version': flask_djangofy.get_version()
    }
    return template.render(**context)


class Initializer(BaseInitializer):
    """
    Routes initialization class
    This class will start from base url defined in `ROOT_URLCONF` of your defined in your settings
    and get all urls of modules define there. Only those urls will be picked for which app name is
    in `INSTALLED_APPS`. After getting all the urls, url rules will be added in flask app.

    Parameters
    ---
    app: flask app
    config: Config object containing all settings of project
    kwargs: Any extra params
    ---
    """
    def __init__(self, **kwargs):
        self.load = kwargs.get('load_only')
        self.urls = []

    def __get_app_list(self):
        installed_app = settings.INSTALLED_APPS[:]
        if self.load != 'all':
            return ['root', self.load]
        installed_app.append('root')
        return installed_app

    def __get_base_urls(self):
        """
        Get list of urls from the settings `ROOT_URLCONF`.
        :return: list of urls
        :rtype list
        """
        root_urls = import_string('{root}.urlpatterns'.format(root=settings.ROOT_URLCONF))
        sys.stdout.write(' * {count} base urls found\n'.format(count=len(root_urls)))
        return root_urls

    def __filter_by_app(self, urls):
        """
        Exclude urls for which app is not in `INSTALLED_APPS`. The urls which are not representing any module
        but defined in base urls will have root as their app.
        :param urls: list of urls
        :return: list of filtered urls
        :rtype list
        """
        return [url for url in urls if url.get_app() in self.__get_app_list()]

    def __load_all_urls(self):
        """
        Construct list of all urls in project. This will be done on the basis of filtered urls
        """
        base_urls = self.__filter_by_app(
            self.__get_base_urls()
        )
        for url in base_urls:
            self.urls.extend(url.get_urls())
        sys.stdout.write(' * {count} total urls found\n'.format(count=len(self.urls)))

    def initialize_routes(self):
        """
        All all routes rule in flask app
        """
        if not self.urls and settings.DEBUG:
            from flask_djangofy.urls import path
            path('/', default_urlconf).initialize()
        else:
            for url in self.urls:
                url.initialize()


    def initialize(self):
        """
        Initialize routes by performing all required processes
        :return:
        """
        self.__load_all_urls()
        self.initialize_routes()