import requests
from ..QlikUser import QlikSenseUser

class QlikSenseRepository:
    __ENDPOINTS = {
        'apps': 'app',
        'user': 'user'
    }

    def __init__(self, host, session: requests.Session):
        self.__host = host
        self.__session = session

    def get_app_list(self, filter=None):
        endpoint = self.__ENDPOINTS['apps']
        params = { "filter": filter}
        app_response = self.__session.get(f"{self.__host}/{endpoint}", params=params)
        return app_response.json()

    def get_user_by_id(self, user_id: str):
        endpoint = self.__ENDPOINTS['user']
        user = self.__session.get(f"{self.__host}/{endpoint}/{user_id}")
        return QlikSenseUser(user.json())