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
In Development


## StartProject
In Development


## Adding Custom Command
To add a new management command, write yur command class like this

```python
from flask_djangofy.cmd.base import BaseCommand, BaseArgument

class MyCommand(BaseCommand):
    ARGUMENTS = [
        BaseArgument(
            '--abc', short='-A', help_text="Help Text",
            default='default'
        )
    ]
    def run(self):
        # your logic here
    
    def show_help(self):
        return "Your Help text here"
        
    def validate(self):
        # your validate logic here
    
    
```

After creating this class, add this in your settings file like this


```python
from flask_djangofy.conf import default_settings
default_settings.CMD_ACTIONS.update({
    'my_command': 'path.to.MyCommand'
})

```

Now you can use your command like this

```python manage.py my_command arguments```