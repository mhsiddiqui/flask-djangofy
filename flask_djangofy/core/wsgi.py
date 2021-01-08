import flask_djangofy
from flask_djangofy.conf import settings
from flask_djangofy.utils.module_loading import import_string


def get_wsgi_application(load_only='all'):
    """
    The public interface to Flask's WSGI support. Return a WSGI callable.

    :param str load_only: name of app to load or all
    :return: wsgi app
    """
    flask_djangofy.setup()
    runner_class = import_string(settings.DEFAULT_APP_RUNNER)
    return runner_class(load_only=load_only).get_app()
