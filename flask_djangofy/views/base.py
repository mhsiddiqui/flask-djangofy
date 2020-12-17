from flask.views import MethodView, http_method_funcs


class View(MethodView):
    """
    Base View Class
    """

    def options(self):
        """"
        Method to return supported request method of view
        """
        return [method.upper() for method in http_method_funcs if hasattr(self, method)]