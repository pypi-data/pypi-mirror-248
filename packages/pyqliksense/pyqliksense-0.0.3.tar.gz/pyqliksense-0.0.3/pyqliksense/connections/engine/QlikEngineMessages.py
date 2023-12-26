class QlikSenseEngineMessages:

    @staticmethod
    def create_app(app_name):
        return {"handle": -1, "method": "CreateApp", "params": {"qAppName": app_name}}

    @staticmethod
    def open_doc(app_id: str):
        return {"method": "OpenDoc", "params": [app_id], "handle": -1}

    @staticmethod
    def set_script(script, handle):
        return {"handle": handle, "method": "SetScript", "params": {"qScript": script}}

    @staticmethod
    def get_script(handle):
        return {"handle": handle, "method": "GetScript", "params": {}}

    @staticmethod
    def evaluale_ex(expression, handle):
        return {"handle": handle, "method": "EvaluateEx", "params": { "qExpression": expression}}

    @staticmethod
    def create_session_object(object_def, handle):
        return {"handle": handle, "method": "CreateSessionObject", "params": [object_def]}

    @staticmethod
    def get_layout(handle):
        return {"handle": handle, "method": "GetLayout", "params": []}

    @staticmethod
    def get_hypercube_data(handle, x, y):
        return {"handle": handle, "method": "GetHyperCubeData", "params": ["/qHyperCubeDef", [{"qWidth": x, "qHeight": y}]]}


