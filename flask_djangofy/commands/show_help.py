import sys

from flask_djangofy.utils import ImportUtil
from termcolor import cprint

from flask_djangofy.conf import settings
from .base import BaseCommand, HELP_COMMAND


class ShowHelp(BaseCommand):
    """
    Show help for running commands
    """
    def run(self):
        """
        Print help on console
        """
        sys.stdout.write(HELP_COMMAND)
        app_commands = {}
        for command, method in settings.CMD_ACTIONS.items():
            operation_class = ImportUtil(method, key_type='class').get()
            if app_commands.get(operation_class.APP_NAME):
                app_commands[operation_class.APP_NAME].append(command)
            else:
                app_commands[operation_class.APP_NAME] = [command]
        for app_name, commands in app_commands.items():
            cprint('\n[{app_name}]'.format(app_name=app_name), 'red')
            for command in commands:
                sys.stdout.write('\t{command}\n'.format(command=command))

