import json

from websockets.sync.client import connect as ws_connect


class QlikSenseEngineSession:
    def __init__(self, host, headers):
        self.__host = host
        self.__headers = headers
        self.__engine = None
        self.__request_id = 1

    def __enter__(self):
        self.__engine = ws_connect(self.__host, additional_headers=self.__headers)
        self.__engine.recv()
        self.__engine.recv()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__engine.close()

    def execute(self, payload: dict):
        payload['id'] = self.__request_id
        self.__request_id += 1
        payload_string = json.dumps(payload)
        self.__engine.send(payload_string)
        response_str = self.__engine.recv()
        response_json = json.loads(response_str)
        return response_json
