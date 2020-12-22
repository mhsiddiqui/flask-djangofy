from flask_djangofy.conf import settings
from flask_djangofy.conf.global_settings import DEFAULT_HOST, DEFAULT_PORT
from flask_djangofy.core.management.base import BaseCommand, BaseArgument
from flask_djangofy.utils import ImportUtil


class RunServer(BaseCommand):
    """
    Run development server
    """

    ARGUMENTS = [
        BaseArgument(
            '--host', short='-H', help_text="Host of the Flask-app default: {host}".format(host=DEFAULT_HOST),
            default=DEFAULT_HOST
        ),
        BaseArgument(
            '--port', short='-P', help_text="Port for the Flask-app default: {port}".format(port=DEFAULT_PORT),
            default=DEFAULT_PORT
        ),
        BaseArgument(
            '--load_only', short='-lo',
            help_text="Load only a specific app if you want to run your project in microservice architecture",
            default='all'
        )
    ]

    APP_NAME = 'flask_djangofy'

    HELP_DATA = {
        "title": "runserver",
        "description": "Command to run development server",
        "usage": "python manage.py runserver --port=port --host=host --load_only=app_name",
        "examples": [
            "python manage.py runserver",
            "python manage.py runserver --port=8000 --host=127.0.0.1"
        ]
    }

    def run(self):
        """
        Runs runserver command with provided arguments
        """
        runner_class = ImportUtil(settings.DEFAULT_APP_RUNNER, key_type='class').get()
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
