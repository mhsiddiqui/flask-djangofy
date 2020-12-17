# Initializers

Initializers are classes which run before running server. Default initializers are

1. Route initlizer


## Adding new initializer

You can add new initializer by adding this in your settings file.

```python
from flask_djangofy.conf import default_settings


default_settings.INITIALIZERS.extend([
    'path.to.your.InitializerClass'
])

```

## Writing custom initializer

You can write you custom initializer like this

```python

from flask_djangofy.initializers.base import BaseInitializer

class YourInitializer(BaseInitializer):
    def initialize(self):
        pass
```

Write you business logic in `initialize` function. Add this inializer in `INITIALIZERS` list. 