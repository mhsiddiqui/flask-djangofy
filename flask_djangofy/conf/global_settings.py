DEFAULT_APP_RUNNER = 'flask_djangofy.core.runner.AppRunner'

INITIALIZERS = [
    'flask_djangofy.initializers.routes.RouteInitializer'
]

CMD_ACTIONS = {
    'runserver': 'flask_djangofy.commands.RunServer',
    # 'startproject': 'flask_djangofy.cmd.StartProject',
    # 'startapp': 'flask_djangofy.cmd.StartApp'
}


TIME_ZONE = 'America/Chicago'


DEFAULT_PORT = 5000
DEFAULT_HOST = '127.0.0.1'
