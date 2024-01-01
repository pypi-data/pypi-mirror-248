import ssl
from .QlikEngineSession import QlikSenseEngineSession
from .QlikEngineMessages import QlikSenseEngineMessages
from pyqliksense.objects import QlikSenseHyperCube


class QlikSenseEngine:
    def __init__(self, host: str, headers: dict, ssl_context: ssl.SSLContext):
        self.__host = host
        self.__engine_headers = headers
        self.__ssl_context = ssl_context
        self.qlik_engine_session = QlikSenseEngineSession(self.__host, headers=self.__engine_headers, ssl_context=self.__ssl_context)

    def create_app(self, name: str):
        payload = {"handle": -1, "method": "CreateApp", "params": {"qAppName": name}}
        with self.qlik_engine_session as engine_session:
            response = engine_session.execute(payload)
            return response

    def set_app_script(self, app_id: str, new_script: str):
        open_app_payload = QlikSenseEngineMessages.open_doc(app_id)
        with self.qlik_engine_session as engine_session:
            open_app = engine_session.execute(open_app_payload)
            app_handle = open_app['result']['qReturn']['qHandle']
            set_script_payload = QlikSenseEngineMessages.set_script(new_script, app_handle)
            set_script = engine_session.execute(set_script_payload)
            return set_script

    def get_app_script(self, app_id: str):
        open_app_payload = QlikSenseEngineMessages.open_doc(app_id)
        with self.qlik_engine_session as engine_session:
            open_app = engine_session.execute(open_app_payload)
            app_handle = open_app['result']['qReturn']['qHandle']
            get_script_payload = QlikSenseEngineMessages.get_script(app_handle)
            get_script = engine_session.execute(get_script_payload)
            return get_script

    def evaluate_expression(self, app_id: str, expression: str):
        open_app_payload = QlikSenseEngineMessages.open_doc(app_id)
        with self.qlik_engine_session as engine_session:
            open_app = engine_session.execute(open_app_payload)
            app_handle = open_app['result']['qReturn']['qHandle']
            evaluate_expression_payload = QlikSenseEngineMessages.evaluate_ex(expression, app_handle)
            expression_evaluation = engine_session.execute(payload=evaluate_expression_payload)
            return expression_evaluation

    def get_hypercube_data(self, app_id, hypercube_def: QlikSenseHyperCube, x: int, y: int):
        open_app_payload = QlikSenseEngineMessages.open_doc(app_id)
        with self.qlik_engine_session as engine_session:
            open_app = engine_session.execute(open_app_payload)
            app_handle = open_app['result']['qReturn']['qHandle']
            create_session_object_payload = QlikSenseEngineMessages.create_session_object(hypercube_def.get_cube_def(), app_handle)

            session_object_created = engine_session.execute(create_session_object_payload)
            object_handle = session_object_created['result']['qReturn']['qHandle']
            engine_session.execute(QlikSenseEngineMessages.get_layout(object_handle))
            cube_data = engine_session.execute(QlikSenseEngineMessages.get_hypercube_data(object_handle, x, y))
            #  go on with getting data

            return cube_data['result']

    def create_sheet(self, app_id: str, sheet_name: str):
        open_app_payload = QlikSenseEngineMessages.open_doc(app_id)
        with self.qlik_engine_session as engine_session:
            open_app = engine_session.execute(open_app_payload)
            app_handle = open_app['result']['qReturn']['qHandle']
            create_sheet_payload = QlikSenseEngineMessages.create_sheet(app_handle, sheet_name)
            create_sheet_response = engine_session.execute(create_sheet_payload)
            sheet_handle = create_sheet_response['result']['qReturn']['qHandle']

            get_created_sheet = engine_session.execute(QlikSenseEngineMessages.get_layout(sheet_handle))
            sheet_layout = get_created_sheet['result']['qLayout']

            return sheet_layout

    def add_obj_to_sheet(self, app_id, sheet_id, obj, coordinates):
        open_app_payload = QlikSenseEngineMessages.open_doc(app_id)
        with self.qlik_engine_session as engine_session:
            open_app = engine_session.execute(open_app_payload)
            app_handle = open_app['result']['qReturn']['qHandle']
            get_sheet_obj_payload = QlikSenseEngineMessages.get_object(app_handle, sheet_id)
            obj_handle = engine_session.execute(get_sheet_obj_payload)['result']['qReturn']['qHandle']
            get_sheet_tree_payload = QlikSenseEngineMessages.get_tree(obj_handle)
            full_tree = engine_session.execute(get_sheet_tree_payload)['result']
            full_tree['qPropEntry']['qChildren'].append(obj)
            cell = {
                "name": obj['qProperty']['qInfo']['qId'],
                "type": obj['qProperty']['qInfo']['qType'],
                "col": coordinates['col'],
                "row": coordinates['row'],
                "colspan": coordinates['colspan'],
                "rowspan": coordinates['rowspan']
            }

            full_tree['qPropEntry']['qProperty']['cells'].append(cell)

            set_sheet_tree_payload = QlikSenseEngineMessages.set_tree(obj_handle, tree=full_tree)
            res = engine_session.execute(set_sheet_tree_payload)

            return res

    def add_obj_to_sheet_many(self, app_id: str, sheet_id: str, objects_and_coordinates: list[dict]):
        open_app_payload = QlikSenseEngineMessages.open_doc(app_id)
        with self.qlik_engine_session as engine_session:
            open_app = engine_session.execute(open_app_payload)
            app_handle = open_app['result']['qReturn']['qHandle']
            get_sheet_obj_payload = QlikSenseEngineMessages.get_object(app_handle, sheet_id)
            obj_handle = engine_session.execute(get_sheet_obj_payload)['result']['qReturn']['qHandle']
            get_sheet_tree_payload = QlikSenseEngineMessages.get_tree(obj_handle)
            full_tree = engine_session.execute(get_sheet_tree_payload)['result']

            for obj in objects_and_coordinates:

                full_tree['qPropEntry']['qChildren'].append(obj['obj'])
                cell = {
                    "name": obj['obj']['qProperty']['qInfo']['qId'],
                    "type": obj['obj']['qProperty']['qInfo']['qType'],
                    "col":  obj['coordinates']['col'],
                    "row": obj['coordinates']['row'],
                    "colspan": obj['coordinates']['colspan'],
                    "rowspan": obj['coordinates']['rowspan'],
                }

                full_tree['qPropEntry']['qProperty']['cells'].append(cell)

            set_sheet_tree_payload = QlikSenseEngineMessages.set_tree(obj_handle, tree=full_tree)
            res = engine_session.execute(set_sheet_tree_payload)

            return res

    def get_sheets(self, app_id: str):
        sheet_list_def = {
            "qInfo": {"qId": "SheetList", "qType": "SheetList"},
            "qAppObjectListDef": {
                "qType": "sheet",
                "qData": {
                    "title": "/qMetaDef/title",
                    "labelExpression": "/labelExpression",
                    "showCondition": "/showCondition",
                    "description": "/qMetaDef/description",
                    "descriptionExpression": "/descriptionExpression",
                    "thumbnail": "/thumbnail",
                    "cells": "/cells",
                    "rank": "/rank",
                    "columns": "/columns",
                    "rows": "/rows"
                }
            }
        }

        open_app_payload = QlikSenseEngineMessages.open_doc(app_id)
        with self.qlik_engine_session as engine_session:
            open_app = engine_session.execute(open_app_payload)
            app_handle = open_app['result']['qReturn']['qHandle']
            create_sheet_list = QlikSenseEngineMessages.create_session_object(sheet_list_def, app_handle)
            sheet_list_created = engine_session.execute(create_sheet_list)
            sheet_list_handle = sheet_list_created['result']['qReturn']['qHandle']
            layout = engine_session.execute(QlikSenseEngineMessages.get_layout(sheet_list_handle))

            sheets = layout['result']['qLayout']['qAppObjectList']['qItems']

            return sheets
