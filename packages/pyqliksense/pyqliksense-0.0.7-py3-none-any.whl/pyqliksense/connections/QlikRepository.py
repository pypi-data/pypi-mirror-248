import json

import requests

class QlikSenseRepository:
    __ENDPOINTS = {
        'app': 'app',
        'user': 'user',
        'reloadtask': 'reloadtask',
        'task': 'task'
    }

    def __init__(self, host, session: requests.Session):
        self.__host = host
        self.__session = session


    def get_app_list(self, filter=None):
        endpoint = self.__ENDPOINTS['app']
        params = { "filter": filter}
        app_response = self.__session.get(f"{self.__host}/{endpoint}", params=params)
        return app_response.json()

    def get_user_by_id(self, user_id: str):
        endpoint = self.__ENDPOINTS['user']
        user = self.__session.get(f"{self.__host}/{endpoint}/{user_id}")
        return user.json()

    def get_task(self, task_id: str):
        endpoint = self.__ENDPOINTS['reloadtask']
        task = self.__session.get(f"{self.__host}/{endpoint}/{task_id}")
        return task

    def get_tasks(self, filter=None):
        endpoint = self.__ENDPOINTS['reloadtask']
        tasks = self.__session.get(f"{self.__host}/{endpoint}", params={"filter": filter})
        return tasks.json()

    def update_task(self, payload = dict):
        endpoint = self.__ENDPOINTS['reloadtask']
        task_updated = self.__session.put(f"{self.__host}/{endpoint}/{payload['id']}", data=json.dumps(payload).encode("utf-8"))
        return task_updated

    def start_task(self, task_id: str):
        endpoint = self.__ENDPOINTS['task']
        task_started = self.__session.post(f"{self.__host}/{endpoint}/{task_id}/start")
        return task_started

    def stop_task(self, task_id):
        endpoint = self.__ENDPOINTS['task']
        task_started = self.__session.post(f"{self.__host}/{endpoint}/{task_id}/stop")
        return task_started


