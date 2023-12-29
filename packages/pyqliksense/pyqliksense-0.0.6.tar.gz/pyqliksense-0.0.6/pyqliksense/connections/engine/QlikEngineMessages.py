class QlikSenseEngineMessages:

    @staticmethod
    def build_engine_message(handle: int, method: str, params):
        return {
            "handle": handle,
            "method": method,
            "params": params
        }

    @classmethod
    def create_app(cls, app_name):
        return cls.build_engine_message(-1, "CreateApp", {"qAppName": app_name})

    @classmethod
    def open_doc(cls, app_id: str):
        return cls.build_engine_message(-1, "OpenDoc", [app_id])

    @classmethod
    def set_script(cls, script, handle):
        return cls.build_engine_message(handle, "SetScript", {"qScript": script})

    @classmethod
    def get_script(cls, handle):
        return cls.build_engine_message(handle, "GetScript", {})

    @classmethod
    def evaluate_ex(cls, expression, handle):
        return cls.build_engine_message(handle, "EvaluateEx", {"qExpression": expression})

    @classmethod
    def create_session_object(cls, object_def, handle):
        return cls.build_engine_message(handle, "CreateSessionObject", [object_def])

    @classmethod
    def get_object(cls, handle, obj_id):
        return cls.build_engine_message(handle, "GetObject", params=[obj_id])

    @classmethod
    def get_layout(cls, handle):
        return cls.build_engine_message(handle, "GetLayout", [])

    @classmethod
    def get_hypercube_data(cls, handle, x, y):
        return cls.build_engine_message(handle, "GetHyperCubeData", ["/qHyperCubeDef", [{"qWidth": x, "qHeight": y}]])

    @staticmethod
    def create_sheet(handle, sheet_name, cols=24, rows=12, description="", rank=0):
        sheet_def = {
                "qInfo": {"qType": "sheet"},
                "qMetaDef": {"title": sheet_name, "description": description},
                "rank": rank,
                "thumbnail": {"qStaticContentUrlDef": None},
                "columns": cols,
                "rows": rows,
                "cells": [],
                "qChildListDef": {
                    "qData": {"title": "/title"}
                }
            }

        return {
            "handle": handle,
            "method": "CreateObject",
            "params": [sheet_def]
        }
