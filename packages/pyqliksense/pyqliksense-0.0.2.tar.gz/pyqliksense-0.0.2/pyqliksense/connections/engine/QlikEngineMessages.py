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


