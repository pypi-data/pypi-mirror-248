import requests
from .connections.QlikRepository import QlikSenseRepository
from .connections.QlikHubApi import QlikSenseHubApi
from .connections.engine.QlikEngine import QlikSenseEngine
from .QlikApplication import QlikApp
from websockets.sync.client import connect as ws_connect
from requests_ntlm import HttpNtlmAuth

class QlikSense:
    __AUTH_TYPES = ('NTLM', 'JWT') #CERT to be added

    def __init__(self, host:str, auth_type:str, jwt_token:str=None, virtual_proxy:str="", username="", password="", cert=None, disable_warnings=False):
        if(auth_type not in self.__AUTH_TYPES): raise Exception(f"Unsupported authentication type: {auth_type}. Must be one of {self.__AUTH_TYPES}")
        if disable_warnings: requests.packages.urllib3.disable_warnings()

        self.__auth_mapping = {
            'NTLM': {
                'method': self.__auth_ntlm,
                'params': { 'username': username, 'password': password }
            },
            'JWT': {
                'method':  self.__auth_jwt,
                'params': {'jwt_token': jwt_token}
            }
        }

        self.__host = host
        self.__jwt_token = jwt_token
        self.__virtual_proxy = virtual_proxy.strip('/')
        self.__cert = cert
        self.__user = username
        self.__password = password
        self.__xref_key = "1234567890123456"
        self.__host_full: str = f"{host.rstrip(r'/')}/{virtual_proxy}".strip('/')
        self.__engine_host: str = f"{self.__host_full}/app/engineData"
        self.__qrs_host: str = f"{self.__host_full}/qrs"
        self.__engine_host:str = f"{self.__host_full.replace('http', 'ws')}"
        self.__request_params = { "xrfkey": self.__xref_key }

        self.__auth_method = self.__auth_mapping[auth_type]['method']
        self.__auth_params = self.__auth_mapping[auth_type]['params']
        self.__auth_method(**self.__auth_params)
        self.__qs_repository = QlikSenseRepository(host=self.__qrs_host, headers=self.__headers, default_params=self.__request_params)
        self.__qs_hub_api = QlikSenseHubApi(host=self.__host_full, headers=self.__headers)
        self.__qs_engine = QlikSenseEngine(host=self.__host_full, headers=self.__headers)

    def __auth_ntlm(self, username, password):
        print('NTLM AUTH '+ self.__qrs_host )
        self.__headers = {
            'X-Qlik-xrfkey': self.__xref_key,
            "Content-Type": "application/json",
            "User-Agent": "Windows"
        }

        user_auth = HttpNtlmAuth(username=username, password=password)
        handshake = requests.get(f"{self.__qrs_host}/about", headers=self.__headers, params=self.__request_params, auth=user_auth, verify=False)
        print (handshake.json())
        qlik_session_id = handshake.cookies.get('X-Qlik-Session')
        self.__headers['Cookie'] = f'X-Qlik-Session={qlik_session_id}'


        with ws_connect(f"{self.__engine_host}/app/engineData", additional_headers=self.__headers) as engine:
            print(engine.recv())
            print(engine.recv())

    def __auth_jwt(self, jwt_token):
        print ('JWT AUTH ' + self.__qrs_host)
        self.__headers = {
            "X-Qlik-XrfKey": self.__xref_key,
            "Authorization": f"Bearer {jwt_token}"
        }
        handshake = requests.get(f"{self.__qrs_host}/about", headers=self.__headers, params=self.__request_params, verify=False)
        print(handshake.json())

        with ws_connect(f"{self.__engine_host}/app/engineData", additional_headers=self.__headers) as engine:
             print (engine.recv())
             print (engine.recv())

    def create_app(self, name):
        new_app = self.__qs_engine.create_app(name)
        return new_app

    def get_apps(self):
        app_list = self.__qs_repository.get_app_list()
        apps = [QlikApp(host_server=self, **app_json ) for app_json in app_list]
        return apps

    def set_app_script(self, app_id, new_script):
        set_script = self.__qs_engine.set_app_script(app_id, new_script)
        return set_script

    def get_app_script(self, app_id: str):
        get_script = self.__qs_engine.get_app_script(app_id)
        return get_script

    def evaluate_expression(self, app_id: str, expression: str):
        result = self.__qs_engine.evaluate_expression(app_id, expression)
        return result














