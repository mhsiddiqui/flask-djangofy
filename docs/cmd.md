# Command Line Interface

The command line interface of flask-djangofy is designed to use it in similar way as it is used in Django. It can used in following ways.

```python manage.py operation arguments```


## Runserver
To start development server, run following command

```python manage.py runserver --port=your_port --host=your_host --load_only=app_name```
 
1. PORT: Any port. Default is 5000
2. HOST: IP of server. Default is 127.0.0.1
3. Load Only: Name of App. In case your want to serve only a specific app. Default is all


## StartApp
```python manage.py startapp --name=APP_NAME```

1. APP_NAME: Name of app. Name cannot contain space or any special character other than underscore.


## StartProject
```python manage.py startapp --name=PROJECT_NAME```

1. PROJECT_NAME: Name of project. Name cannot contain space or any special character other than underscore.


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
from flask_djangofy.cmd.base import BaseCommand

class Command(BaseCommand):

    def run(self):
        # your logic here
    
    def add_arguments(self, parser):
        # Add argument in parser
        
    def validate(self):
        # your validate logic here
    
    
```


Now you can use your command like this

```python manage.py my_command arguments```