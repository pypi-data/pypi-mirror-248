import requests


class QlikSenseRepository:
    __ENDPOINTS = {
        'apps': 'app',
    }

    def __init__(self, host, headers, default_params):
        self.__host = host
        self.__headers = headers
        self.__default_params = default_params

    def get_app_list(self, filter=None):
        endpoint = self.__ENDPOINTS['apps']
        params = {**self.__default_params, "filter": filter}
        app_response = requests.get(f"{self.__host}/{endpoint}", params=params, headers=self.__headers)
        return app_response.json()