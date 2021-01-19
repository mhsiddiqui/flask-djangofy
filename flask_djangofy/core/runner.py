import os
import pkgutil
from importlib import import_module

import sys

from flask_djangofy import app, BASE_PATH
from flask_djangofy.apps import apps
from flask_djangofy.conf import settings


class AppRunner(object):
    """
    Flask app runner class.
    This will initialize all initializers defined in `INITIALIZERS` and then run the server
    """
    def __init__(self, **kwargs):
        """
        :param str load: name of app if you want to load urls of a specific app only
        """
        self.kwargs = kwargs

    def find_initializers(self, directory):
        """
        Find intializers under provided directory
        :param directory: directory path
        :return: list of initializers
        """
        initializers_dir = os.path.join(directory, 'initializers')
        return [name for _, name, is_pkg in pkgutil.iter_modules([initializers_dir])
                if not is_pkg and not name.startswith('_') and name != 'base']

    def get_initializers(self):
        """
        Get all initializers in project
        :return: list of initializers
        """
        initializer = ['flask_djangofy.initializers.%s' % name for name in self.find_initializers(BASE_PATH)]
        initializer.extend(settings.INITIALIZERS)
        for app_config in reversed(list(apps.get_app_configs())):
            path = os.path.join(app_config.path, 'initializers')
            initializer.extend('%s.initializers.%s' % (app_config.name, name) for name in self.find_initializers(path))

        return initializer

    def before(self):
        """
        The function which will run before starting application server
        """
        initializers = self.get_initializers()
        with app.app_context():
            for index, initializer in enumerate(initializers):
                sys.stdout.write('{index}: {initializer} initializing.\n'.format(
                    index=index, initializer=initializer
                ))
                initializer_class = import_module(initializer).Initializer
                initializer_class(**self.kwargs).initialize()

    def run(self):
        """
        Function to run the server
        :param kwargs: Configurations for server
        """
        self.before()
        app.run(**self.__get_app_params())

    def __get_app_params(self):
        """
        Get app specific params
        :return: params dict
        :rtype dict
        """
        return {
            'port': self.kwargs.get('port'),
            'host': self.kwargs.get('host')
        }

    def get_app(self):
        """
        Get app object to be used by wsgi
        :return: app
        """
        self.before()
        return app.configure()
