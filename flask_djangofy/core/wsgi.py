from flask_djangofy.conf import settings
from flask_djangofy.utils import ImportUtil

import flask_djangofy


def get_wsgi_application(load_only='all'):
    """
    The public interface to Flask's WSGI support. Return a WSGI callable.

    :param str load_only: name of app to load or all
    :return: wsgi app
    """
    flask_djangofy.setup()
    runner_class = ImportUtil(settings.DEFAULT_APP_RUNNER, key_type='class').get()
    return runner_class(load_only=load_only).get_app()
