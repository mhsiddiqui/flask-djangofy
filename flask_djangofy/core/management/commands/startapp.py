import os
import re
from flask_djangofy import BASE_PATH

from flask_djangofy.core.exceptions import CommandError
from flask_djangofy.core.management.templates import TemplateCommand


class Command(TemplateCommand):

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.target_path = os.path.join(os.getcwd(), self.kwargs.get('name'))

    def validate(self):
        if not re.match("^[a-zA-Z0-9_]*$", self.kwargs.get('name')):
            raise CommandError("Name should only contains alphabets or _ or numeric")
        if os.path.exists(self.target_path):
            raise CommandError("%s already exists" % self.kwargs.get('name'))

    def run(self):
        templates = {
            'urls.txt': {},
            'views.txt': {},
            'apps.txt': {
                'config_name': ''.join([h.title() for h in self.kwargs.get('name').split('_')]),
                'app': self.kwargs.get('name')
            }
        }
        for template, data in templates.items():
            path = os.path.join(BASE_PATH, 'templates', self.command, template)
            file_name = template.replace('txt', 'py')
            template_data = self.get_template(path, **data)
            self.generate(self.target_path, file_name, template_data)
        self.generate(self.target_path, '__init__.py', '')

    def add_arguments(self, parser):
        parser.add_argument(
            '--name', help="Name of the app", required=True
        )


