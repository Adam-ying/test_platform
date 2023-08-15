from Common.http_client import BodyType, HttpClient
from Proj.harbor.Config.config_data import host, login_acc, login_pwd
from Proj.harbor.Config.config_api import Login_Token


class GetToken:
    def __init__(self, env):
        self.hc = HttpClient()
        self.cr = CommonRequest(env, header_flag=False)


    def get_token(self):
        api_params = {
            "case_name": "登录接口",
            "json": {"username": login_acc, "password": login_pwd}
        }

        self.cr.send_http_request(self.hc, data=api_params, query=Login_Token.GET_TOKEN)
        value_list = self.hc.json_value('$.data.getToken.token')
        token = value_list and value_list[0] or None
        return token
class CommonRequest:

    def __init__(self, env, header_flag=True):
        self.env = env
        self.post_method = 'POST'
        self.header_flag = header_flag
        if header_flag:
            self.headers = {'authorization': GetToken(self.env).get_token()}

    # 适用于GraphQL接口的请求
    def send_http_request(self, hc, data, query):
        hc.set_name(name=data['case_name'])
        hc.set_url(url=host.get(self.env) + '/graphql')
        hc.set_method(method=self.post_method)
        if self.header_flag:
            hc.set_headers(headers=self.headers)
        hc.set_body_type(body_type=BodyType.JSON)
        hc.set_body(data={'variables': data['json'], 'query': query})
        hc.send()

    # 适用于非GraphQl的请求
    def send_http_requests(self, hc, data):
        hc.set_name(name=data['case_name'])
        hc.set_url(url=host.get(self.env) + data['url'])
        hc.set_method(method=data['method'])
        if self.header_flag:
            hc.set_headers(headers=self.headers)
        if data.get('body_type', None):
            hc.set_body_type(body_type=data['body_type'])
        if data.get('body', None):
            hc.set_body(data=data['body'])
        if data.get('params', None):
            hc.set_params(params=data['params'])
        hc.send()



