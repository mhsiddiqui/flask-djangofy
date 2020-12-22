import os

from jinja2 import Template

from flask_djangofy.core.management.base import BaseCommand


class TemplateCommand(BaseCommand):

    def get_template(self, template, **data):
        """
        Get template by name
        :param str template: template name
        :return: template
        """
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_path = os.path.join(base_path, self.command, template)
        template = Template(template_path).render(**data)
        return template

    def generate(self, template, path, name):
        with open(os.path.join(path, name), 'r+') as f:
            f.write(template)

