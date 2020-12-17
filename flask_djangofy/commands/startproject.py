import os
from binascii import hexlify

from flask_djangofy.commands import BaseArgument
from flask_djangofy.commands import TemplateCommand


class StartProject(TemplateCommand):
    ARGUMENTS = [
        BaseArgument(
            '--name', help_text="Name of the project", required=True
        )
    ]

    APP_NAME = 'flask_djangofy'

    HELP_DATA = {
        "title": "startproject",
        "description": "Command to create project",
        "usage": "python manage.py startproject --name=ProjectName",
        "examples": [
            "python manage.py startproject --name=MyProjectName"
        ]
    }

    def validate(self):
        if hasattr(self, 'name'):
            return True
        return False

    def run(self):
        templates = {
            'settings.txt': {
                'secret_key': hexlify(os.urandom(20)),
                'project': self.kwargs.get('name')
            },
            'urls.txt': {},
            'wsgi.txt': {}
        }
        os.mk
        for template, data in templates.items():
            jtemp = self.get_template(template, **data)


