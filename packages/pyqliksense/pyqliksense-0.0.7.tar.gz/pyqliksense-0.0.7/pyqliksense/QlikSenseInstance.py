import requests, ssl
from .connections.QlikRepository import QlikSenseRepository
from .connections.QlikHubApi import QlikSenseHubApi
from .connections.engine.QlikEngine import QlikSenseEngine, QlikSenseEngineSession
from .QlikApplication import QlikApp
from .QlikUser import QlikSenseUser
from .QlikTask import QlikSenseTask
from requests_ntlm import HttpNtlmAuth

class QlikSense:
    __AUTH_TYPES = ('NTLM', 'JWT', 'CERT')

    def __init__(self, host:str, auth_type:str, jwt_token: str = None, virtual_proxy: str = "", userdirectory = "", username = "", password = "", cert=None, qrs_port=4242, engine_port=4747, disable_warnings=False):
        if(auth_type not in self.__AUTH_TYPES): raise Exception(f"Unsupported authentication type: {auth_type}. Must be one of {self.__AUTH_TYPES}")
        if disable_warnings: requests.packages.urllib3.disable_warnings()

        __QRS_PORT    = f':{qrs_port}' if auth_type == 'CERT' else ''
        __ENGINE_PORT = f':{engine_port}' if auth_type == 'CERT' else ''

        self.__auth_mapping = {
            'NTLM': {
                'method': self.__auth_ntlm,
                'params': { 'username': f"{userdirectory}\{username}", 'password': password }
            },
            'JWT': {
                'method':  self.__auth_jwt,
                'params': {'jwt_token': jwt_token}
            },
            'CERT': {
                'method': self.__cert_auth,
                'params': {'cert': cert, "user_directory": userdirectory, "username": username}
            }
        }

        self.__host = host
        self.__jwt_token = jwt_token
        self.__virtual_proxy = virtual_proxy.strip('/')
        self.__cert = cert
        self.__ssl_context = ssl.create_default_context()
        self.__ssl_context.check_hostname = False
        if cert is not None:
            self.__ssl_context.load_cert_chain(certfile=self.__cert[0], keyfile=self.__cert[1])
            self.__ssl_context.load_verify_locations(cafile=self.__cert[2])

        self.__user = username
        self.__password = password
        self.__xref_key = "1234567890123456"
        self.__basic_headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "X-Qlik-XrfKey": self.__xref_key,
        }

        self.__host_full: str = f"{host.rstrip(r'/')}/{virtual_proxy}".strip('/')
        self.__qrs_host: str = f"{self.__host.rstrip(r'/')}{__QRS_PORT}/{virtual_proxy}/".rstrip('/') + '/qrs'
        self.__engine_rest_host: str = f"{self.__host.rstrip(r'/')}{__QRS_PORT}/{virtual_proxy}/".rstrip('/') + '/api/v1'
        self.__engine_host: str = f"{self.__host.replace('http', 'ws').rstrip(r'/')}{__ENGINE_PORT}/{virtual_proxy}/".rstrip('/') + '/app/engineData'
        self.__request_params = { "xrfkey": self.__xref_key }
        self.__headers = {}
        self.__auth_method = self.__auth_mapping[auth_type]['method']
        self.__auth_params = self.__auth_mapping[auth_type]['params']
        qrs_session = self.__auth_method(**self.__auth_params)

        self.qs_repository = QlikSenseRepository(host=self.__qrs_host, session=qrs_session)
        self.__qs_hub_api = QlikSenseHubApi(host=self.__host_full, headers=self.__headers)
        self.qs_engine = QlikSenseEngine(host=self.__engine_host, headers=self.__headers, ssl_context=self.__ssl_context)

    def __auth_ntlm(self, username, password):
        self.__headers = {
            **self.__basic_headers,
            "User-Agent": "Windows"
        }
        user_auth = HttpNtlmAuth(username=username, password=password)
        qrs_session = requests.Session()
        qrs_session.auth = user_auth
        qrs_session.verify = False
        qrs_session.headers = self.__headers
        qrs_session.params = self.__request_params

        handshake = qrs_session.get(f"{self.__qrs_host}/about")
        print (handshake.json())
        qlik_session_id = handshake.cookies.get('X-Qlik-Session')
        self.__headers['Cookie'] = f'X-Qlik-Session={qlik_session_id}'

        qlik_engine_session = QlikSenseEngineSession(host=self.__engine_host, headers=self.__headers,
                                                     ssl_context=self.__ssl_context)

        with qlik_engine_session as engine_session:
            pass

        return qrs_session

    def __auth_jwt(self, jwt_token):

        self.__headers = {
            **self.__basic_headers,
            "Authorization": f"Bearer {jwt_token}",
        }
        qrs_session = requests.Session()
        qrs_session.headers = self.__headers
        qrs_session.params = self.__request_params
        qrs_session.verify = False

        handshake = qrs_session.get(f"{self.__qrs_host}/about")
        print(handshake.json())

        qlik_engine_session = QlikSenseEngineSession(host=self.__engine_host, headers=self.__headers,
                                                     ssl_context=self.__ssl_context)

        with qlik_engine_session as engine_session:
            pass

        return qrs_session

    def __cert_auth(self, cert: tuple[str], user_directory: str, username: str):
        qrs_session = requests.Session()
        self.__headers = {
            **self.__basic_headers,
            "X-Qlik-User": f"UserDirectory={user_directory};UserId={username}"
        }
        qrs_session.cert = cert
        qrs_session.headers = self.__headers
        qrs_session.params = self.__request_params
        qrs_session.verify = False
        handshake = qrs_session.get(f"{self.__qrs_host}/about")
        print (handshake.json())

        qlik_engine_session = QlikSenseEngineSession(host=self.__engine_host, headers=self.__headers, ssl_context=self.__ssl_context)

        with qlik_engine_session as engine_session:
            pass

        return qrs_session

    def create_app(self, name):
        new_app = self.qs_engine.create_app(name)
        return new_app

    def get_apps(self):
        app_list = self.qs_repository.get_app_list()
        apps = [QlikApp(host_server=self, **app_json ) for app_json in app_list]
        return apps

    def get_apps_by_name(self, app_name):
        apps = self.qs_repository.get_app_list(filter=f"name eq '{app_name}'")
        apps = [QlikApp(host_server=self, **app_json) for app_json in apps]
        return apps

    def get_user(self, user_id: str):
        user_json = self.qs_repository.get_user_by_id(user_id)
        return QlikSenseUser(user_json)

    def get_tasks(self):
        return [QlikSenseTask(t, self.qs_repository) for t in self.qs_repository.get_tasks()]
















