import argparse
import os
import pkgutil
import sys
from collections import defaultdict
from importlib import import_module

import flask_djangofy
from flask_djangofy.apps import apps
from flask_djangofy.conf import settings
from flask_djangofy.core.exceptions import CommandError, ImproperlyConfigured
from flask_djangofy.core.management.base import handle_default_options, NO_COMMAND_ERROR, BaseCommand
from flask_djangofy.core.management.color import color_style


def find_commands(management_dir):
    """
    Given a path to a management directory, return a list of all the command
    names that are available.
    """
    command_dir = os.path.join(management_dir, 'commands')
    return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir])
            if not is_pkg and not name.startswith('_')]


def load_command_class(app_name, name):
    """
    Given a command name and an application name, return the Command
    class instance. Allow all errors raised by the import process
    (ImportError, AttributeError) to propagate.
    """
    module = import_module('%s.management.commands.%s' % (app_name, name))
    return module.Command


def get_commands():
    """
    Return a dictionary mapping command names to their callback applications.

    Look for a management.commands package in flask_djangofy.core, and in each
    installed application -- if a commands package exists, register all
    commands in that package.

    Core commands are always included. If a settings module has been
    specified, also include user-defined commands.

    The dictionary is in the format {command_name: app_name}. Key-value
    pairs from this dictionary can then be used in calls to
    load_command_class(app_name, command_name)

    If a specific version of a command must be loaded (e.g., with the
    startapp command), the instantiated module can be placed in the
    dictionary in place of the application name.

    The dictionary is cached on the first call and reused on subsequent
    calls.
    """
    commands = {name: 'flask_djangofy.core' for name in find_commands(__path__[0])}

    if not settings.configured:
        return commands

    for app_config in reversed(list(apps.get_app_configs())):
        path = os.path.join(app_config.path, 'management')
        commands.update({name: app_config.name for name in find_commands(path)})

    return commands


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

    def main_help_text(self, commands_only=False):
        """Return the script's main help text, as a string."""
        if commands_only:
            usage = sorted(get_commands())
        else:
            usage = [
                "",
                "Type '%s help <subcommand>' for help on a specific subcommand." % self.prog_name,
                "",
                "Available subcommands:",
            ]
            commands_dict = defaultdict(lambda: [])
            for name, app in get_commands().items():
                if app == 'flask_djangofy.core':
                    app = 'flask_djangofy'
                else:
                    app = app.rpartition('.')[-1]
                commands_dict[app].append(name)
            style = color_style()
            for app in sorted(commands_dict):
                usage.append("")
                usage.append(style.NOTICE("[%s]" % app))
                for name in sorted(commands_dict[app]):
                    usage.append("    %s" % name)
            # Output an extra note if settings are not properly configured
            if self.settings_exception is not None:
                usage.append(style.NOTICE(
                    "Note that only Django core commands are listed "
                    "as settings are not properly configured (error: %s)."
                    % self.settings_exception))

        return '\n'.join(usage)

    def __fetch_command(self):
        """
        Try to fetch the given subcommand, printing a message with the
        appropriate command called from the command line (usually
        "flask_djangofy-admin" or "manage.py") if it can't be found.
        """
        # Get commands outside of try block to prevent swallowing exceptions
        commands = get_commands()
        try:
            app_name = commands[self.operation]
        except KeyError:
            if os.environ.get('APP_SETTINGS_MODULE'):
                # If `subcommand` is missing due to misconfigured settings, the
                # following line will retrigger an ImproperlyConfigured exception
                # (get_commands() swallows the original one) so the user is
                # informed about it.
                settings.INSTALLED_APPS
            elif not settings.configured:
                sys.stderr.write("No flask_djangofy settings specified.\n")
            sys.stderr.write("\nType '%s help' for usage.\n" % self.prog_name)
            sys.exit(1)
        if isinstance(app_name, BaseCommand):
            # If the command is already loaded, use it directly.
            klass = app_name
        else:
            klass = load_command_class(app_name, self.operation)
        return klass

    def __execute_command(self):
        """
        Execute command
        :param args: arguments required by command
        :param options: keyword arguments
        """
        command_class = self.__fetch_command()()
        argument_parser = argparse.ArgumentParser(
            usage='manage.py operation [options] [args]',
            add_help=False, allow_abbrev=False
        )
        argument_parser.add_argument('--command')
        argument_parser.add_argument('--settings')
        argument_parser.add_argument('--pythonpath')

        command_class.add_arguments(argument_parser)
        try:
            options, args = argument_parser.parse_known_args(self.argv[2:])
            handle_default_options(options)
        except CommandError:
            pass  # Ignore any option errors at this point.

        command_class.execute(*args, **vars(options))

    def execute(self):
        """
        Execute a command
        """
        self.__set_operation()

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
                    self.__execute_command()
                except CommandError:
                    raise
            else:
                sys.stdout.write(self.main_help_text() + '\n')


def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    utility = ManagementUtility(argv)
    utility.execute()
