# Views

Views can be created using flask-djangofy like this.


```python
from flask_djangofy.views import View

# class based view

class MyView(View):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

# function based views
def my_view():
    pass
```
As in flask, request object can be accessed by importing it from flask, request is not passed to every views which is different from Django.