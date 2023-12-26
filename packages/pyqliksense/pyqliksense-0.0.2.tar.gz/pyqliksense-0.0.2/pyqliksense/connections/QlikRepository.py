import requests


class QlikSenseRepository:
    __ENDPOINTS = {
        'apps': 'app',
    }

    def __init__(self, host, headers, default_params):
        self.__host = host
        self.__headers = headers
        self.__default_params = default_params


    def get_app_list(self):
        endpoint = self.__ENDPOINTS['apps']
        app_response = requests.get(f"{self.__host}/{endpoint}", params=self.__default_params, headers=self.__headers).json()
        return app_response