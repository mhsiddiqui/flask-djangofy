import os
import sys


NO_COMMAND_ERROR = """
Unknown command: '{operation}'
Type 'manage.py help' for usage.
"""

NEW_LINE = '\n'

class BaseCommand(object):
    """
    The base class from which all management commands ultimately
    derive.
    """

    def __init__(self):
        self.command = None
        self.args = None
        self.kwargs = None

    def initialize(self, *args, **kwargs):
        """
        Initialize class variables
        :param args:
        :param kwargs:
        :return:
        """
        self.command = kwargs.pop('command', None)
        self.args = args
        self.kwargs = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def validate(self):
        """
        Function to check all validation logic
        """
        pass

    def run(self):
        """
        Run the command. Steps to perform operation here
        """
        pass

    def add_arguments(self, parser):
        """
        Implement to add arguments in parser
        :param parser:
        :return:
        """

    def execute(self, *args, **kwargs):
        """
        Execute required command
        """
        self.initialize(*args, **kwargs)
        self.validate()
        if 'help' not in self.args:
            self.run()



def handle_default_options(options):
    """
    Include any default options that all commands should accept here
    so that ManagementUtility can handle them before searching for
    user commands.
    """
    if options.settings:
        os.environ['APP_SETTINGS_MODULE'] = options.settings
    if options.pythonpath:
        sys.path.insert(0, options.pythonpath)