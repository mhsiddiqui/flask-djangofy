import argparse
import os
import sys

import flask_djangofy
from flask_djangofy.conf import settings
from flask_djangofy.core.exceptions import CommandError, ImproperlyConfigured
from flask_djangofy.core.management.base import handle_default_options, NO_COMMAND_ERROR
from flask_djangofy.core.management.commands import ShowHelp
from flask_djangofy.utils import ImportUtil


class ManagementUtility(object):
    """
    Encapsulate the logic of the flask-djangofy and manage.py utilities.
    """
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.operation = 'help'
        self.prog_name = os.path.basename(self.argv[0])
        self.settings_exception = None

    def __set_operation(self):
        """
        Set operation
        """
        try:
            self.operation = self.argv[1]
            self.argv.append('--command={}'.format(self.operation))
        except IndexError:
            pass

    def __no_command_error(self):
        """
        Error in case of no command found
        """
        error_message = NO_COMMAND_ERROR.format(operation=self.operation)
        sys.stdout.write(error_message)

    def __get_argument_parser(self):
        """
        Construct and return argument parser
        :return: argument parser
        """
        argument_parser = argparse.ArgumentParser(
            usage='manage.py operation [options] [args]',
            add_help=False, allow_abbrev=False
        )
        argument_parser.add_argument('--command')
        argument_parser.add_argument('--settings')
        argument_parser.add_argument('--pythonpath')
        actions = settings.CMD_ACTIONS
        for _, parser in actions.items():
            parser_class = ImportUtil(parser, key_type='class').get()
            arguments = parser_class.ARGUMENTS
            for argument in arguments:
                args, kwargs = argument.get()
                argument_parser.add_argument(*args, **kwargs)
        return argument_parser

    def __execute_command(self, *args, **options):
        """
        Execute command
        :param args: arguments required by command
        :param options: keyword arguments
        """
        command_function = settings.CMD_ACTIONS.get(self.operation)
        if not command_function:
            raise CommandError
        operation_class = ImportUtil(command_function, key_type='class').get()
        op_class = operation_class(*args, **options)
        if op_class.is_valid():
            op_class.execute()

    def execute(self):
        """
        Execute a command
        """
        self.__set_operation()
        parser = self.__get_argument_parser()
        try:
            options, args = parser.parse_known_args(self.argv[2:])
            handle_default_options(options)
        except CommandError:
            pass  # Ignore any option errors at this point.

        try:
            settings.INSTALLED_APPS
        except ImproperlyConfigured as exc:
            self.settings_exception = exc
        except ImportError as exc:
            self.settings_exception = exc

        if settings.configured:
            # Start the auto-reloading dev server even if the code is broken.
            # The hardcoded condition is a code smell but we can't rely on a
            # flag on the command class because we haven't located it yet.
            flask_djangofy.setup()
            if self.operation != 'help':
                try:
                    self.__execute_command(*args, **vars(options))
                except CommandError:
                    self.__no_command_error()
            else:
                ShowHelp(arg_parser=parser).run()


def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    utility = ManagementUtility(argv)
    utility.execute()
