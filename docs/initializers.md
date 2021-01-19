# Initializers

Initializers are classes which run before running server. Default initializes are

1. Route initialize


## Adding new initializer

You can add new initializer by adding this in your settings file.

```python
from flask_djangofy.conf import global_settings


global_settings.INITIALIZERS.extend([
    'path.to.your.InitializerClass'
])

```

or if your initializer is in your app, create `initializers` package in your app and flask_djangofy will pick it automatically.

## Writing custom initializer

You can write you custom initializer like this

```python

from flask_djangofy.initializers.base import BaseInitializer

class Initializer(BaseInitializer):
    def initialize(self):
        pass
```
*Name of class should be `Initializer`

Write you business logic in `initialize` function. Add this initializer in `INITIALIZERS` list. 