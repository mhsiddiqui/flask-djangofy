# Setup

flask-djangofy is very easy to setup. You will need to perform following steps and you will be ready to go.

## Step # 1: Installation
Install it by running below command.

> `pip install flask-djangofy`


## Step # 2: Create manage.py
Create a file `manage.py` in your project directory and add following code in it.

```python
#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('APP_SETTINGS_MODULE', 'YOUR_PROJECT_NAME.settings')
    try:
        from flask_djangofy.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import flask-djangofy. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
```
Replace YOUR_PROJECT_NAME with your project name.

## Step # 3: Create Project
Run following command to create your project
> `python manage.py startproject YOUR_PROJECT_NAME`

## Step # 4: Create Apps
Run following command to create app
> `python manage.py startproject YOUR_APP_NAME`

You will need to add app in `INSTALLED_APPS` in `YOUR_PROJECT_NAME/settings.py` just like Django.

## Step # 5: Write Views/URLs
Write your views and urls.

## Step # 6: Run Server
Run development server by running following command

> `python manage.py runserver`