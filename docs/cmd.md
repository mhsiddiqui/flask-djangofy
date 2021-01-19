# Command Line Interface (flask-djangofy-admin and manage.py)

The command line interface of flask-djangofy is designed to use it in similar way as it is used in Django. It can used in following ways.

flask-djangofy-admin is flask-djangofy’s command-line utility for administrative tasks. This document outlines all it can do.

In addition, manage.py is automatically created in each flask-djangofy project. It does the same thing as flask-djangofy-admin but also sets the FLASK_SETTINGS_MODULE environment variable so that it points to your project’s settings.py file.

The flask-djangofy-admin script should be on your system path if you installed flask-djangofy via pip. If it’s not in your path, ensure you have your virtual environment activated.

Generally, when working on a single flask-djangofy project, it’s easier to use manage.py than flask-djangofy-admin. If you need to switch between multiple flask-djangofy settings files, use flask-djangofy-admin with FLASK_SETTINGS_MODULE or the --settings command line option.

The command-line examples throughout this document use flask-djangofy-admin to be consistent, but any example can use manage.py or python -m flask_djangofy just as well.

## Usage

```bash
$ flask-djangofy-admin <command> [options]
$ manage.py <command> [options]
$ python -m flask_djangofy <command> [options]
```

command should be one of the commands listed in this document. options, which is optional, should be zero or more of the options available for the given command.

### Getting runtime help

Run **flask-djangofy-admin help** to display usage information and a list of the commands provided by each application.

Run **flask-djangofy-admin help --commands** to display a list of all available commands.

Run **flask-djangofy-admin help <command>** to display a description of the given command and a list of its available options.

## runserver
> flask-djangofy-admin runserver [addrport]

Starts a lightweight development Web server on the local machine. By default, the server runs on port 8000 on the IP address 127.0.0.1. You can pass in an IP address and port number explicitly.

## startApp
> flask-djangofy-admin startapp name [directory]

Creates a flask-djangofy app directory structure for the given app name in the current directory or the given destination.

## startproject

> flask-djangofy-admin startproject name [directory]

Creates a flask-djangofy project directory structure for the given project name in the current directory or the given destination.

By default, the new directory contains manage.py and a project package (containing a settings.py and other files).

## Adding Custom Command
To do this, add a management/commands directory to the application. flask-djangofy will register a manage.py command for each Python module in that directory whose name doesn’t begin with an underscore. For example: 

```python
app_name/
    __init__.py
    management/
        commands/
            _private.py
            command_name.py
    views.py
```

n this example, the command_name command will be made available to any project that includes the app_name application in INSTALLED_APPS.

The _private.py module will not be available as a management command.

The command_name.py module has only one requirement – it must define a class Command that extends BaseCommand or one of its subclasses.


```python
from flask_djangofy.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Your help text here'

    def add_arguments(self, parser):
        # add arguments here

    def handle(self, *args, **options):
        # add your logic here
```


Now you can use your command like this

```python manage.py my_command arguments```