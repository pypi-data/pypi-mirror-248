import sys, os, json
from io import BytesIO
import xmldict

sys.path.append(os.getcwd())
try:
    from config import APP_SETTING
except Exception:
    APP_SETTING = {}

import cgi
import threading
from urllib.parse import parse_qs
from panax.utils.jwt_helper import jwt_decode

from panax.utils.request_helper import request_process


MEMFILE_MAX = 1024*100


def getRequestText(r):
    maxread = max(0, r.content_length)
    stream = r._environ['wsgi.input']
    body = BytesIO() if maxread < MEMFILE_MAX else TemporaryFile(mode='w+b')
    while maxread > 0:
        part = stream.read(min(maxread, MEMFILE_MAX))
        if not part:  # TODO: Wrong content_length. Error? Do nothing?
            break
        body.write(part)
        maxread -= len(part)
    return body.getvalue().decode()



class Request(threading.local):
    def bind(self, environ, url_map):
        self._environ = environ

        self._headers = None
        self._user = None
        self._BODY = ''
        self._GET = {}
        self._POST = {}
        self._FILES = {}

        # 资源
        path_resource = self.path[0]
        # 方法
        path_operation = self.path[1]

        if path_resource in url_map and path_operation in url_map[path_resource] \
                and url_map[path_resource][path_operation]["secret"] != None:
            secret = url_map[path_resource][path_operation]["secret"]
        elif path_resource == "file":
            secret = False
        else:
            secret = APP_SETTING["request"]["secret"]
        # region URL 参数
        query_string = self._environ.get('QUERY_STRING', '')
        raw_dict = parse_qs(query_string, keep_blank_values=1)
        for key, value in raw_dict.items():
            if len(value) == 1:
                self._GET[key] = value[0]
            else:
                self._GET[key] = value
        # endregion

        # if "text/plain" in self.content_type:
            # region body 文本
        self._BODY = getRequestText(self)
            # endregion
        if "multipart/form-data" in self.content_type:
            # region body form
            raw_data = cgi.FieldStorage(fp=self._environ['wsgi.input'], environ=self._environ)
            if raw_data.list:
                for key in raw_data:
                    if raw_data[key].filename:
                        self._FILES[key] = raw_data[key]
                    elif isinstance(raw_data[key], list):
                        self._POST[key] = [v.value for v in raw_data[key]]
                    else:
                        self._POST[key] = raw_data[key].value

            if secret:
                self._POST = request_process(self._POST)

            # if not self._FILES and APP_SETTING["request"]["secret"]:
            #     self._POST = request_process(self._POST)
            # endregion
        if "application/json" in self.content_type:
            # region body json
            # self._BODY = getRequestText(self)
            self._POST = json.loads(self._BODY)
            if secret:
                self._POST = request_process(self._POST)
            # endregion
        if "application/xml" in self.content_type:
            # region body xml
            # self._BODY = getRequestText(self)
            self._POST = xmldict.xml_to_dict(self._BODY)
            if secret:
                self._POST = request_process(self._POST)
            # endregion

    # region 请求信息

    @property
    def path(self):
        full_path = '/' + self._environ.get('PATH_INFO', '').lstrip('/')
        request_path = full_path.replace('/api/', '')
        arr_path = str(request_path).split('/')
        return arr_path

    @property
    def method(self):
        return self._environ.get('REQUEST_METHOD', 'GET').upper()

    @property
    def headers(self):
        if self._headers == None:
            self._headers = {}
            for key, value in dict(self._environ).items():
                if str(key).startswith("HTTP_"):
                    self._headers[str(key).replace("HTTP_", "")] = value
        return self._headers

    @property
    def user(self):
        if self._user == None:
            token = self.headers["AUTHORIZATION"] if "AUTHORIZATION" in self.headers and self.headers[
                "AUTHORIZATION"] else ""
            if token:
                self._user = jwt_decode(token)
            else:
                self._user = {
                    "id": "",
                    "username": "anymore",
                    "name": "匿名用户",
                    "role": "anymore"
                }
                for item in APP_SETTING["jwt"]["column"]:
                    if item not in self._user:
                        self._user[item] = ""
        return self._user

    @property
    def content_type(self):
        return self._environ.get('CONTENT_TYPE', '')

    @property
    def content_length(self):
        return int(self._environ.get('CONTENT_LENGTH', '') or -1)

    # endregion

    # region 请求数据

    @property
    def BODY(self):
        return self._BODY

    @property
    def GET(self):
        return self._GET

    @property
    def POST(self):
        return self._POST

    @property
    def FILES(self):
        return self._FILES

    # endregion

