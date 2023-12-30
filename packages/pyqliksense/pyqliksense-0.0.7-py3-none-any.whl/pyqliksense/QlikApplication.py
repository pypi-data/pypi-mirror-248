

class QlikApp:
    def __init__(self, host_server = None,  **kwargs):
        self.id = self.__get_kwarg(kwargs, 'id')
        self.name: str = self.__get_kwarg(kwargs, 'name')
        self.is_published = self.__get_kwarg(kwargs, 'published')
        self.__host_server = host_server

    def set_server(self, server):
        if self.__host_server is not None:
            raise Exception("Application's server is already established and cannot be changed")

        self.__host_server = server

    def set_script(self, script):
        result = self.__host_server.qs_engine.set_app_script(self.id, script)
        return result

    def get_script(self):
        script = self.__host_server.qs_engine.get_app_script(self.id)
        return script

    def evaluate_expression(self, expression):
        result = self.__host_server.qs_engine.evaluate_expression(self.id, expression)
        return result

    def get_hypercube_data(self, cube, x, y):
        result = self.__host_server.qs_engine.get_hypercube_data(self.id, cube, x, y)
        return result

    def create_sheet(self, sheet_name):
        return self.__host_server.qs_engine.create_sheet(self.id, sheet_name)

    def get_sheets(self):
        return self.__host_server.qs_engine.get_sheets(self.id)


    @staticmethod
    def __get_kwarg(kwargs, param):
        return kwargs[param] if param in kwargs else None









