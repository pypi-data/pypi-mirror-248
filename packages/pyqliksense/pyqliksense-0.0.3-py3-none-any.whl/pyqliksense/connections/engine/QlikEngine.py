from .QlikEngineSession import QlikSenseEngineSession
from .QlikEngineMessages import QlikSenseEngineMessages
from pyqliksense.objects import QlikSenseHyperCube


class QlikSenseEngine:
    def __init__(self, host: str, headers: dict):
        self.__host = host.rstrip('/').replace('http', 'ws') + '/app/engineData'
        self.__engine_headers = headers

    def create_app(self, name: str):
        payload = {"handle": -1, "method": "CreateApp", "params": {"qAppName": name}}
        with QlikSenseEngineSession(self.__host, headers=self.__engine_headers) as engine_session:
            response = engine_session.execute(payload)
            return response

    def set_app_script(self, app_id: str, new_script: str):
        open_app_payload   = QlikSenseEngineMessages.open_doc(app_id)
        with QlikSenseEngineSession(self.__host, headers=self.__engine_headers) as engine_session:
            open_app = engine_session.execute(open_app_payload)
            app_handle = open_app['result']['qReturn']['qHandle']
            set_script_payload = QlikSenseEngineMessages.set_script(new_script, app_handle)
            set_script = engine_session.execute(set_script_payload)
            return set_script

    def get_app_script(self, app_id: str):
        open_app_payload = QlikSenseEngineMessages.open_doc(app_id)
        with QlikSenseEngineSession(self.__host, headers=self.__engine_headers) as engine_session:
            open_app = engine_session.execute(open_app_payload)
            app_handle = open_app['result']['qReturn']['qHandle']
            get_script_payload = QlikSenseEngineMessages.get_script(app_handle)
            get_script = engine_session.execute(get_script_payload)
            return get_script

    def evaluate_expression(self, app_id: str, expression: str):
        open_app_payload = QlikSenseEngineMessages.open_doc(app_id)
        with QlikSenseEngineSession(self.__host, headers=self.__engine_headers) as engine_session:
            open_app = engine_session.execute(open_app_payload)
            app_handle = open_app['result']['qReturn']['qHandle']
            evaluate_expression_payload = QlikSenseEngineMessages.evaluale_ex(expression ,app_handle)
            expression_evaluation = engine_session.execute(payload=evaluate_expression_payload)
            return expression_evaluation

    def get_hypercube_data(self, app_id, hypercube_def: QlikSenseHyperCube, x:int, y:int):
        open_app_payload = QlikSenseEngineMessages.open_doc(app_id)
        with QlikSenseEngineSession(self.__host, headers=self.__engine_headers) as engine_session:
            open_app = engine_session.execute(open_app_payload)
            app_handle = open_app['result']['qReturn']['qHandle']
            create_session_object_payload = QlikSenseEngineMessages.create_session_object(hypercube_def.get_cube_def(), app_handle)

            session_object_created = engine_session.execute(create_session_object_payload)
            object_handle = session_object_created['result']['qReturn']['qHandle']
            object_layout = engine_session.execute(QlikSenseEngineMessages.get_layout(object_handle))
            cube_data = engine_session.execute(QlikSenseEngineMessages.get_hypercube_data(object_handle, x, y))
            #go on with getting data

            return cube_data['result']



