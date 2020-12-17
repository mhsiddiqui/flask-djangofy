from flask_djangofy.utils import ImportUtil

from flask_djangofy import app
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

    def before(self):
        """
        The function which will run before starting application server
        """
        with app.app_context():
            for initializer in settings.INITIALIZERS:
                initializer_class = ImportUtil(initializer, key_type='class').get()
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
        return app
