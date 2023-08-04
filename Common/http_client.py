from typing import List
import os
import requests
import json
import jsonpath
from Util.logger_util import info_log, error_log


class BodyType:
    """ 请求正文体类型 """
    URL_ENCODE = 'URL_ENCODE'  # 表单格式  'Content-Type'：'application/x-www-form-urlencoded'
    JSON = 'JSON'  # JSON格式 'Content-Type'：'application/json'
    FILE = 'FILE'  # 文件格式  'Content-Type'：'multipart/form-data'


class HttpClient:
    SESSION = requests.session()

    def __init__(self, timeout=5, only_session=True):
        self.only_session = only_session
        self.timeout = timeout  # 请求超时时间
        self.name = None  # 用例名称
        self.url = None  # 请求地址
        self.method = None  # 请求方式
        self.params = {}  # 请求参数
        self.body_type = None  # 正文体类型
        self.headers = {}  # 请求头文件
        self.body = {}  # 请求正文体
        self.res = None  # 响应结果
        self.fail_flag = 0  # 断言失败计数
        self.check_list = []  # 所有断言的检查列表
        self.result = None  # 用例执行结果

    def set_name(self, name):
        self.name = name

    def set_url(self, url):
        self.url = url

    def set_method(self, method):
        self.method = method

    def set_body_type(self, body_type):
        self.body_type = body_type

    def set_header(self, key, value):
        self.headers[key] = value

    def set_headers(self, headers):
        if isinstance(headers, dict):
            self.headers = headers
        else:
            raise Exception('请求头信息请以字典形式填写!')

    def set_cookie(self, key, value):
        cookie = self.headers.get('Cookie')
        if not cookie:
            self.headers['Cookie'] = '{key}={value};'.format(key=key, value=value)
        else:
            self.headers['Cookie'] = cookie + '{key}={value};'.format(key=key, value=value)

    def set_body(self, data):
        if isinstance(data, dict):
            if self.body_type == BodyType.FILE:
                for name, filename in data:
                    self.body[filename] = open(filename, 'rb')
            else:
                self.body = data
        else:
            raise Exception('请求体请以字典形式填写!')

    def set_params(self, params):
        if isinstance(params, dict):
            self.params = params
        else:
            raise Exception('URL参数请以字典形式填写!')

    def send(self):
        if self.method == 'GET':
            try:
                if self.only_session:
                    self.res = HttpClient.SESSION.get(url=self.url, params=self.params, headers=self.headers,
                                                      timeout=self.timeout, verify=False)
                else:
                    self.res = requests.get(url=self.url, params=self.params, headers=self.headers,
                                            timeout=self.timeout, verify=False)
            except:
                self.check_list.append('服务器无响应或请求超时:get, url = {url} '.format(url=self.url))
                self.fail_flag += 1

        elif self.method == 'POST':
            if self.body_type == BodyType.URL_ENCODE:
                self.set_header('Content-Type', 'application/x-www-form-urlencoded')
                try:
                    if self.only_session:
                        self.res = HttpClient.SESSION.post(url=self.url, headers=self.headers, data=self.body,
                                                           verify=False)
                    else:
                        self.res = requests.post(url=self.url, headers=self.headers, data=self.body, verify=False)
                except:
                    self.check_list.append(
                        '服务器无响应或请求超时:post, url = {url}, data = {body}'.format(url=self.url, body=self.body))
                    self.fail_flag += 1

            elif self.body_type == BodyType.JSON:
                self.set_header('Content-Type', 'application/json')
                try:
                    if self.only_session:
                        self.res = HttpClient.SESSION.post(url=self.url, headers=self.headers, json=self.body,
                                                           verify=False)
                    else:
                        self.res = requests.post(url=self.url, headers=self.headers, json=self.body, verify=False)
                except:
                    self.check_list.append(
                        '服务器无响应或请求超时:post, url = {url}, data = {body}'.format(url=self.url, body=self.body))
                    self.fail_flag += 1

            elif self.body_type == BodyType.FILE:
                self.set_header('Content-Type', 'multipart/form-data')
                try:
                    if self.only_session:
                        self.res = HttpClient.SESSION.post(url=self.url, headers=self.headers, files=self.body,
                                                           verify=False)
                    else:
                        self.res = requests.post(url=self.url, headers=self.headers, files=self.body, verify=False)
                except:
                    self.check_list.append(
                        '服务器无响应或请求超时:post, url = {url}, data = {body}'.format(url=self.url, body=self.body))
                    self.fail_flag += 1
        elif self.method == 'DELETE':
            if self.body_type == BodyType.URL_ENCODE:
                self.set_header('Content-Type', 'application/x-www-form-urlencoded')
                try:
                    if self.only_session:
                        self.res = HttpClient.SESSION.delete(url=self.url, headers=self.headers, data=self.body,
                                                             verify=False)
                    else:
                        self.res = requests.delete(url=self.url, headers=self.headers, data=self.body, verify=False)
                except:
                    self.check_list.append(
                        '服务器无响应或请求超时:delete, url = {url}, data = {body}'.format(url=self.url,
                                                                                           body=self.body))
                    self.fail_flag += 1

            elif self.body_type == BodyType.JSON:
                self.set_header('Content-Type', 'application/json')
                try:
                    if self.only_session:
                        self.res = HttpClient.SESSION.delete(url=self.url, headers=self.headers, json=self.body,
                                                             verify=False)
                    else:
                        self.res = requests.delete(url=self.url, headers=self.headers, json=self.body, verify=False)
                except:
                    self.check_list.append(
                        '服务器无响应或请求超时:delete, url = {url}, data = {body}'.format(url=self.url,
                                                                                           body=self.body))
                    self.fail_flag += 1

            elif self.body_type == BodyType.FILE:
                self.set_header('Content-Type', 'multipart/form-data')
                try:
                    if self.only_session:
                        self.res = HttpClient.SESSION.delete(url=self.url, headers=self.headers, files=self.body,
                                                             verify=False)
                    else:
                        self.res = requests.delete(url=self.url, headers=self.headers, files=self.body, verify=False)
                except:
                    self.check_list.append(
                        '服务器无响应或请求超时:delete, url = {url}, data = {body}'.format(url=self.url,
                                                                                           body=self.body))
                    self.fail_flag += 1
        else:
            raise Exception('不支持的请求方法类型!')

    @property
    def status_code(self):
        if self.res is not None:
            return self.res.status_code
        else:
            return None

    @property
    def response_times(self):
        if self.res is not None:
            return round(self.res.elapsed.total_seconds() * 1000)
        else:
            return None

    @property
    def response_body(self):
        if self.res is not None:
            self.res.encoding = "utf-8"
            return self.res.text
        else:
            return None

    @property
    def response_cookie(self):
        if self.res is not None:
            return self.res.cookies
        else:
            return None

    def res_to_json(self):
        if self.res is not None:
            info_log(self.res.json)
            try:
                return self.res.json()
            except:
                return None
        else:
            return None

    def json_value(self, path):
        if self.res is not None:
            object = jsonpath.jsonpath(self.res_to_json(), path)
            if isinstance(object, list):
                return object
        return None

    def check_status_code(self, exp, msg=None):
        content = '响应状态码 预期结果 [{a}], 实际结果 [{b}]'.format(a=exp, b=self.status_code)
        try:
            assert self.status_code == exp
            self.check_list.append(f'<断言成功> : {content} - [ {msg} ]')
        except:
            self.check_list.append(f'<断言失败> : {content} - [ {msg} ]')
            self.fail_flag += 1

    def check_response_less_than(self, exp, msg=None):
        content = '响应时间 预期结果小于 [{a}] ms，实际结果 [{b}] ms'.format(a=exp, b=self.response_times)
        try:
            assert self.response_times <= exp
            self.check_list.append(f'<断言成功> : {content} - [ {msg} ]')
        except:
            self.check_list.append(f'<断言失败> : {content} - [ {msg} ]')
            self.fail_flag += 1

    def check_response_body_equal(self, exp, msg=None):
        content = '预期响应内容 [{a}]，实际响应内容 [{b}]'.format(a=exp, b=self.response_body)
        try:
            assert exp == self.response_body()
            self.check_list.append(f'<断言成功> : {content} - [ {msg} ]')
        except:
            self.check_list.append(f'<断言失败> : {content} - [ {msg} ]')
            self.fail_flag += 1

    def check_response_body_contains(self, exp, msg=None):
        content = '预期响应内容包含 [{a}]，实际响应内容 [{b}]'.format(a=exp, b=self.response_body)
        try:
            assert exp in self.response_body
            self.check_list.append(f'<断言成功> : {content} - [ {msg} ]')
        except:
            self.check_list.append(f'<断言失败> : {content} - [ {msg} ]')
            self.fail_flag += 1

    def check_response_body_no_contains(self, exp, msg=None):
        content = '预期响应内容不包含 [{a}]，实际响应内容 [{b}]'.format(a=exp, b=self.response_body)
        try:
            assert exp not in self.response_body
            self.check_list.append(f'<断言成功> : {content} - [ {msg} ]')
        except:
            self.check_list.append(f'<断言失败> : {content} - [ {msg} ]')
            self.fail_flag += 1

    def check_json_value(self, node_name, exp, msg=None):
        try:
            j = json.loads(self.response_body)
            content = '响应Json [{node}] 字段，预期值等于 [{a}] ，实际值等于 [{b}]'.format(node=node_name, a=exp,
                                                                                         b=j[node_name])
            try:
                assert j[node_name] == exp
                self.check_list.append(f'<断言成功> : {content} - [ {msg} ]')
            except:
                self.check_list.append(f'<断言失败> : {content} - [ {msg} ]')
                self.fail_flag += 1
        except:
            self.check_list.append('<断言失败> : 响应Json值验证失败！响应内容不是有效的Json格式')
            self.fail_flag += 1

    def check_json_path_value_not_none(self, path, msg=None):
        node = self.json_value(path)
        if isinstance(node, list):
            content = '响应Json [{path}] 字段，预期值不等于 [{a}]，实际值等于 [{b}]'.format(path=path, a=None, b=node[0])
            try:
                assert node[0] is not None
                self.check_list.append(f'<断言成功> : {content} - [ {msg} ]')
            except:
                self.check_list.append(f'<断言失败> : {content} - [ {msg} ]')
                self.fail_flag += 1
        else:
            self.check_list.append('<断言失败> : 响应Json值验证失败！json节点[{path}]不存在'.format(path=path))
            self.fail_flag += 1

    def check_json_path_node_not_existent(self, path, msg=None):
        node = self.json_value(path)
        if node is None:
            self.check_list.append(f'<断言成功> : 响应Json [{path}] 节点不存在 - [ {msg} ]')
        else:
            self.check_list.append(f'<断言失败> : 响应Json [{path}] 节点存在 - [ {msg} ]')
            self.fail_flag += 1

    def check_assert_equal(self, arg1, arg2, msg=None):
        if arg1 == arg2:
            self.check_list.append(f'<断言成功> : 结果1：{arg1} 与 结果2：{arg2} 相等 - [ {msg} ]')
        else:
            self.check_list.append(f'<断言失败> : 结果1：{arg1} 与 结果2：{arg2} 不相等 - [ {msg} ]')
            self.fail_flag += 1

    def check_assert_not_equal(self, arg1, arg2, msg=None):
        if arg1 != arg2:
            self.check_list.append(f'<断言成功> : 结果1：{arg1} 与 结果2：{arg2} 不相等 - [ {msg} ]')
        else:
            self.check_list.append(f'<断言失败> :  结果1：{arg1} 与 结果2：{arg2} 相等 - [ {msg} ]')
            self.fail_flag += 1

    def check_assert_contain(self, exp, act, msg=None):
        """ 检查 预期结果是否包含 """
        if act is None:
            act = "None"
        act = isinstance(act, list) and ",".join(act) or act
        if exp in act:
            self.check_list.append(f'<断言成功> : 预期结果: [ {exp} ], 包含在实际结果: [ {act} ] 中 - [ {msg} ]\n')
        else:
            self.check_list.append(f'<断言失败> : 预期结果: [ {exp} ], 未包含在实际结果: [ {act} ] 中 - [ {msg} ]')
            self.fail_flag += 1

    def check_assert_no_contain(self, exp, act, msg=None):
        """ 检查 预期结果是否不包含 """
        if act is None:
            act = "None"
        act = isinstance(act, list) and ",".join(act) or act
        if exp not in act:
            self.check_list.append(f'<断言成功> : 预期结果: [ {exp} ], 不包含在实际结果: [ {act} ] 中 - [ {msg} ]\n')
        else:
            self.check_list.append(f'<断言失败> : 预期结果: [ {exp} ], 包含在实际结果: [ {act} ] 中 - [ {msg} ]')
            self.fail_flag += 1

    def check_json_path_value(self, path, exp, msg=None):
        """ 检查 某路径的节点值包含期望的内容 """
        node = self.json_value(path)
        if isinstance(node, list):
            content = '响应Json [{path}] 字段，预期值等于 [{a}]，实际值等于 [{b}]'.format(path=path, a=exp, b=node[0])
            try:
                assert node[0] == exp
                self.check_list.append(f'<断言成功> : {content} - [ {msg} ]')
            except:
                self.check_list.append(f'<断言失败> : {content} - [ {msg} ]')
                self.fail_flag += 1
        else:
            self.check_list.append('<断言失败> : 响应Json值验证失败！json节点[{path}]不存在'.format(path=path))
            self.fail_flag += 1

    def check_json_path_value_not_equal(self, path, exp, msg=None):
        node = self.json_value(path)
        if isinstance(node, list):
            content = '响应Json [{path}] 字段，预期值不等于 [{a}]，实际值: [{b}]'.format(path=path, a=exp, b=node[0])
            try:
                assert node[0] != exp
                self.check_list.append(f'<断言成功> : {content} - [ {msg} ]')
            except:
                self.check_list.append(f'<断言失败> : {content} - [ {msg} ]')
                self.fail_flag += 1
        else:
            self.check_list.append('<断言失败> : 响应Json值验证失败！json节点[{path}]不存在'.format(path=path))
            self.fail_flag += 1

    def check_equal_sql_from_map(self, response_data: dict, db_record_single: dict, assert_maps: dict, msg=None):
        """
		批量比对接口返回和数据库值是否相等
			@response_data: 接口返回的json数据（可以处理后传入）
			@db_record_single： 数据库返回的单条record json数据
			@assert_maps： key为接口返回需要比对字段的jsonpath表达式，value为数据库返回需要比对字段的jsonpath表达式
		"""

        if not assert_maps:
            return

        for key, value in assert_maps.items():
            result_api = jsonpath.jsonpath(response_data, key)
            result_sql = jsonpath.jsonpath(db_record_single, value)
            content = "预期接口返回结果中[{key}]对应的值：[{result_api}]" \
                      "和数据库中的[{value}]的值：[{result_sql}]相等".format(key=key, value=value, result_api=result_api,
                                                                            result_sql=result_sql)
            try:
                assert result_api == result_sql
                self.check_list.append(f'<断言成功> : {content} - [ {msg} ]')
            except:
                self.check_list.append(f'<断言失败> : {content} - [ {msg} ]')
                self.fail_flag += 1

    def check_equal_sql_from_fields(self, response_data_user_defined: dict, db_record_single: dict,
                                    fields: List[str] = None, msg=None):
        """
		批量比对接口返回和数据库值是否相等
			@response_data_user_defined: 接口返回数据（需要特殊处理成为一个无嵌套的json数据后传入）
			@db_record_single： 数据库返回的单条record json数据
			@fields： 需要比对的字段名成的list，默认不传，以数据库查询结果字段进行比对
		"""

        if not fields:
            compare_feilds = db_record_single.keys()
        else:
            compare_feilds = fields

        for field in compare_feilds:
            content = "接口返回结果中的{field1}对应的值：{res_reslut}" \
                      "和数据库中的{field2}的值：{sql_result}相等".format(
                field1=field,
                res_reslut=response_data_user_defined.get(field),
                field2=field,
                sql_result=db_record_single.get(field)
            )
            try:
                assert response_data_user_defined.get(field) == db_record_single.get(field)
                self.check_list.append(f'<断言成功> : {content} - [ {msg} ]')
            except:
                self.check_list.append(f'<断言失败> : {content} - [ {msg} ]')
                self.fail_flag += 1

    def check_assert_value_not_in_result(self, assert_value, result, msg=None):
        """
			断言assert_value 不在 result 中
		"""
        content = '预期值[{assert_value}]不在[{result}]中'.format(assert_value=assert_value, result=result)
        try:
            assert assert_value not in result
            self.check_list.append(f'<断言成功> : {content} - [ {msg} ]')
        except:
            self.check_list.append(f'<断言失败> : {content} - [ {msg} ]')
            self.fail_flag += 1

    def check_fail(self, msg):
        """ 主动断言失败 """
        check_res = f'<断言失败> : {msg} \n'
        info_log(check_res)
        self.check_list.append(check_res)
        self.fail_flag += 1

    def check_pass(self, msg):
        """ 主动断言成功 """
        check_res = f'<断言成功> : {msg} \n'
        info_log(check_res)
        self.check_list.append(check_res)

    def show_request_log(self):
        """ 日志记录：接口请求信息 """
        info_log(f"用例名称[name] === %s\n" % self.name)
        info_log(f"请求地址[url] === %s\n" % self.url)
        info_log(f"请求方式[method] === %s\n" % self.method)
        if self.params:
            info_log(f"请求参数[params] === %s\n" % self.params)
        if self.body_type:
            info_log(f"正文体类型[body_type] === %s\n" % self.body_type)
        if self.headers:
            info_log(f"请求头文件[headers] === %s\n" % self.headers)
        if self.body:
            info_log(f"请求正文体[body] === %s\n" % json.dumps(self.body, ensure_ascii=False))

    def show_response_log(self):
        """ 日志记录：接口响应信息 """
        info_log(f"响应状态码 === %s\n" % self.status_code)
        info_log(f"响应时间(ms) === %s\n" % self.response_times)
        info_log(f"响应体[body] === %s\n" % self.response_body)

    def show_check_log(self):
        """ 日志记录：验证点信息 """
        for i, check_info in enumerate(self.check_list):
            info_log(f"检查点[{i + 1}] === {check_info}\n")

    def get_case_result(self):
        """ 获取用例执行结果 """
        self.show_request_log()
        self.show_response_log()
        self.show_check_log()
        if self.fail_flag == 0:
            self.result = "接口验证成功"
            info_log(f"测试结果 === 接口验证成功\n")
        else:
            self.result = "接口验证失败"
            info_log(f"测试结果 === 接口验证失败\n")

    def assert_and_show_checkpoint(self):
        """ 用例断言并显示检查点结果 """
        print("\n")
        for each in self.check_list: print(each)
        assert self.fail_flag == 0


if __name__ == '__main__':
    host = "http://10.168.0.10:32498"

    # ------- POST 请求 -------
    # 配置请求参数
    url = f"{host}/api/user/login"
    method = "POST"
    body = {"username": "xiaochunfei", "password": "fxc_whale"}
    body_type = BodyType.JSON
    client = HttpClient()
    client.set_url(url=url)
    client.set_method(method=method)
    client.set_body_type(body_type=body_type)
    client.set_body(data=body)
    # 发送请求
    client.send()
    # 获取响应信息
    print(client.res_to_json())
    # 添加检查点
    client.check_status_code(exp=200)
    client.check_response_less_than(exp=100)
    client.check_json_value(node_name="message", exp="登录成功")
    # 获取用例执行结果
    client.get_case_result()
    for each in client.check_list: print(each)
    print(f"测试结果：{client.result}")
    # 获取token
    token = client.json_value(path="$..data.token")[0]
    print(f"token ----- {token}")

    print("\n ---------------------- \n")

    # ------- GET 请求 -------
    url = f"{host}/api/dashboard/product_test_res"
    method = "GET"
    client2 = HttpClient()
    client2.set_url(url=url)
    client2.set_method(method=method)
    client2.set_header(key="Access-Token", value=token)
    params = {"projectName": "android_xueqiu_app"}
    client2.set_params(params=params)

    # 发送请求
    client2.send()
    # 获取响应信息
    print(client2.res_to_json())
    # 添加检查点
    client2.check_status_code(exp=200)
    client2.check_response_less_than(exp=1000)
    client.check_json_value(node_name="message", exp="success")
    # 获取用例执行结果
    client2.get_case_result()
    for each in client2.check_list: print(each)
    print(f"测试结果：{client.result}")

# 发送请求
# client.send()
# print(client.res)
# print(client.res_to_json())
# # print(client.status_code)
# # print(client.response_times)
# print(client.response_body)
# # print(client.response_cookie)
# # print(client.res_to_json)
# print(client.json_value(path="$..message"))
# # client.check_status_code(exp=200)
# # client.check_response_less_than(exp=100)
# # client.check_response_body_equal(exp={"code": 20001})
# # client.check_response_body_contains(exp="登录")
# client.check_json_value(node_name="message", exp="你好")
# # client.check_json_path_value(path="$..code", exp=2222)
# # 获取用例执行结果
# client.get_case_result()
# print(client.check_list)
# print(client.result)
