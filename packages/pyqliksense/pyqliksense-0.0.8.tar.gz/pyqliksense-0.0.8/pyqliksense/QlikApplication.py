from .objects.QlikSheet import QlikSenseSheet


class QlikApp:
    def __init__(self, host_server=None,  **kwargs):
        self.id = self.__get_kwarg(kwargs, 'id')
        self.name: str = self.__get_kwarg(kwargs, 'name')
        self.is_published = self.__get_kwarg(kwargs, 'published')
        self.host_server = host_server

    def set_server(self, server):
        if self.host_server is not None:
            raise Exception("Application's server is already established and cannot be changed")

        self.host_server = server

    def set_script(self, script):
        result = self.host_server.qs_engine.set_app_script(self.id, script)
        return result

    def get_script(self):
        script = self.host_server.qs_engine.get_app_script(self.id)
        return script

    def evaluate_expression(self, expression):
        result = self.host_server.qs_engine.evaluate_expression(self.id, expression)
        return result

    def get_hypercube_data(self, cube, x, y):
        result = self.host_server.qs_engine.get_hypercube_data(self.id, cube, x, y)
        return result

    def create_sheet(self, sheet_name):
        sheet_layout = self.host_server.qs_engine.create_sheet(self.id, sheet_name)
        return QlikSenseSheet(sheet_layout, self)

    def get_sheets(self):
        engine_sheets = self.host_server.qs_engine.get_sheets(self.id)
        return [QlikSenseSheet(sh, self) for sh in engine_sheets]

    @staticmethod
    def __get_kwarg(kwargs, param):
        return kwargs[param] if param in kwargs else None
