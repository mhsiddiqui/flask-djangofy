"""
Invokes flask_djangofy-admin when the flask-djangofy module is run as a script.
Example: python -m flask_djangofy check
"""
from flask_djangofy.core import management

if __name__ == "__main__":
    management.execute_from_command_line()