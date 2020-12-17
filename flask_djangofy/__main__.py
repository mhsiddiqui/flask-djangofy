"""
Invokes django-admin when the flask-djangofy module is run as a script.
Example: python -m django check
"""
from flask_djangofy.core import management

if __name__ == "__main__":
    management.execute_from_command_line()