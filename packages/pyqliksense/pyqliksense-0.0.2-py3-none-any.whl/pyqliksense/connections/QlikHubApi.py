import requests


class QlikSenseHubApi:
    def __init__(self, host: str, headers):
        self.__host = f"{host.rstrip(r'/')}/api/hub/v1"
        self.__headers = headers
        self.__ENDPOINTS = {
            'app' : 'apps'
        }

    def create_app(self, name):
        endpoint = self.__ENDPOINTS['app']
        payload = { "data": {"type": "App", "attributes": {"name": name}}}

        response = requests.post(f"{self.__host}/{endpoint}", data=payload, headers=self.__headers, verify=False)
        return response
