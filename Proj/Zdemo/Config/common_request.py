from Proj.Zdemo.Config.config_data import host, login_acc, login_pwd
from Common.http_client import BodyType
from Proj.Zdemo.Config.config_api import Login_Token
from Common.http_client import HttpClient


class CommonRequest:
    """ 公共接口请求类 """

    def __init__(self, env, headers_flag=True):
        self.env = env  # 执行环境
        self.post_method = "POST"
        self.headers_flag = headers_flag
        if self.headers_flag:
            self.headers = {'authorization': GetToken(env=env).get_token()}

    def send_http_request(self, hc, data, query):
        hc.set_name(name=data["case_name"])
        hc.set_url(url=host.get(self.env))
        hc.set_method(method=self.post_method)
        if self.headers_flag:
            hc.set_headers(headers=self.headers)
        hc.set_body_type(body_type=BodyType.JSON)
        hc.set_body(data={'query': query, 'variables': data['json']})
        hc.send()


class GetToken:
    """ 获取登录token类 """

    def __init__(self, env):
        self.hc = HttpClient()
        self.cr = CommonRequest(env=env, headers_flag=False)

    def get_token(self):
        api_params = {
            "case_name": "登录接口",
            "json": {"username": login_acc, "password": login_pwd}
        }
        # 发送请求(登录接口)
        self.cr.send_http_request(hc=self.hc, data=api_params, query=Login_Token.GET_TOKEN)
        # 获取'token'值
        value_list = self.hc.json_value("$.data.getToken.token")
        token = value_list and value_list[0] or None
        return token
