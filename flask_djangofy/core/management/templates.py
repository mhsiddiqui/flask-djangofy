import os

from jinja2 import Template

from flask_djangofy.core.management.base import BaseCommand


class TemplateCommand(BaseCommand):

    def get_template(self, template_path, **data):
        """
        Get template by name
        :param str template_path: template path
        :return: template
        """
        template = Template(self.__get_template_data(template_path)).render(**data)
        return template

    def __get_template_data(self, template):
        """
        Read template file and return its data
        :param template: template path
        :return: template data
        """
        with open(template, 'r+') as f:
            template_text = f.read()
        return template_text

    def generate(self, target_path, name, template):
        """
        Generate file at provided path
        :param target_path: path where file has to be created
        :param name: name of file
        :param template: content of file
        """
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        with open(os.path.join(target_path, name), 'w+') as f:
            f.write(template)

