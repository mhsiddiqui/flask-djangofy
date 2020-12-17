from flask import Flask
from flask_djangofy.utils.functional import LazyObject

from flask_djangofy.utils.versions import get_version

VERSION = (1, 0, 0, 'alpha', 0)

__version__ = get_version(VERSION)


class _AppSetup(object):
    """
    App setup class
    """
    app = None

    def __init__(self):
        self.app = None

    @classmethod
    def initiate(cls):
        if not cls.app:
            from flask_djangofy.conf import settings
            cls.app = Flask(__name__)
            cls.app.config.from_object(settings)


def setup():
    """
    Setup flask app
    """
    _AppSetup().initiate()


class LazyApp(LazyObject):
    """
    A lazy proxy for flask app object
    """
    def _setup(self):

        if not _AppSetup.app:
            from flask_djangofy.core import ImproperlyConfigured
            raise ImproperlyConfigured("Call flask_djangofy.setup() before importing app")
        self._wrapped = _AppSetup.app


app = LazyApp()