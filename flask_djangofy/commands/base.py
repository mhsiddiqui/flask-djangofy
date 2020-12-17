import argparse
import sys

from termcolor import cprint

from flask_djangofy.core.exceptions import ImproperlyConfigured

NO_COMMAND_ERROR = """
Unknown command: '{operation}'
Type 'manage.py help' for usage.
"""

HELP_COMMAND = """
Type 'manage.py help <subcommand>' for help on a specific subcommand.

Available subcommands:
"""

NEW_LINE = '\n'

class BaseCommand(object):
    """
    The base class from which all management commands ultimately
    derive.
    """

    # Arguments required by command
    ARGUMENTS = []

    # App name for categorizing commands in helo
    APP_NAME = None

    # Help data in case if command help is required
    HELP_DATA = {
        "title": "command_help",
        "description": "description",
        "usage": "python manage.py operation args",
        "examples": ["python manage.py operation args"]
    }

    def __init__(self, command=None, *args, **kwargs):
        self.command = command
        self.args = args
        self.kwargs = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def show_help(self):
        """
        Show help text for command in case of validation error
        """
        cprint('\nCommand: {title}'.format(**self.HELP_DATA), 'green')
        sys.stdout.write('\n{description}\n\n'.format(**self.HELP_DATA))
        for index, example in enumerate(self.HELP_DATA.get('examples', [])):
            sys.stdout.write('\t{index}: {example}\n'.format(index=index, example=example))
        sys.stdout.write(NEW_LINE)
        tmp_parser = argparse.ArgumentParser(usage=self.HELP_DATA.get('usage'))
        for argument in self.ARGUMENTS:
            args, kwargs = argument.get()
            tmp_parser.add_argument(*args, **kwargs)
        tmp_parser.print_help()

    def validate(self):
        """
        Function to check all validation logic
        """
        pass

    def is_valid(self):
        """
        Check if arguments are valid or not
        """
        if not self.APP_NAME:
            raise ImproperlyConfigured("App name not set in {command}".format(command=type(self).__name__))
        if self.validate():
            return True
        else:
            self.show_help()

    def run(self):
        """
        Run the command. Steps to perform operation here
        """
        pass

    def execute(self):
        """
        Execute required command
        """
        if 'help' in self.args:
            self.show_help()
        else:
            self.run()


class BaseArgument(object):
    """
    Argument class for argument parser
    """
    def __init__(self, argument, short='', help_text='No Help Available', default='', required=False):
        self.argument = argument
        self.short = short
        self.help = help_text
        self.default = default
        self.required = required

    def get(self):
        """
        Return argument in args and kwargs form
        :return: args and kwargs
        :rtype tuple
        """
        args = [self.argument]
        if self.short:
            args.append(self.short)
        kwargs = {
            'help': self.help,
            'default': self.default,
            'required': self.required
        }
        return args, kwargs