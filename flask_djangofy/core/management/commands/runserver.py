from flask_djangofy.conf import settings
from flask_djangofy.conf.global_settings import DEFAULT_HOST, DEFAULT_PORT
from flask_djangofy.core.management.base import BaseCommand
from flask_djangofy.utils.module_loading import import_string


class Command(BaseCommand):
    """
    Run development server
    """

    def run(self):
        """
        Runs runserver command with provided arguments
        """
        runner_class = import_string(settings.DEFAULT_APP_RUNNER)
        runner_class(**self.kwargs).run()

    def validate(self):
        """
        Validate if port and host are in arguments provided
        :return: If arguments are valid or not
        :rtype bool
        """
        if hasattr(self, 'port') and hasattr(self, 'host'):
            return True
        return False

    def add_arguments(self, parser):
        parser.add_argument(
            '--host', '-H', help="Host of the Flask-app default: {host}".format(host=DEFAULT_HOST),
            default=DEFAULT_HOST
        )
        parser.add_argument(
            '--port', '-P', help="Port for the Flask-app default: {port}".format(port=DEFAULT_PORT),
            default=DEFAULT_PORT
        )
        parser.add_argument(
            '--load_only', '-lo',
            help="Load only a specific app if you want to run your project in microservice architecture",
            default='all'
        )
