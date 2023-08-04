import pytest
from Common.http_client import HttpClient
from Proj.Zdemo.Config.config_api import Module_Name


class TestModuleName:

    def setup(self):
        self.hc = HttpClient()  # 初始化 用例检查对象

    def teardown(self):
        self.hc.get_case_result()  # 获取用例执行结果并显示日志

    # graphql接口
    @pytest.mark.SMOKING_BY_Zdemo
    def test_demo_single(self, common_request, case_name, case_data, case_expect):
        """
            单接口配置步骤：1.配置接口参数、2.发送请求、3.添加基础检查点、4.添加业务检查点、5.单接口断言并显示检查点结果
        """
        # 1.配置接口参数
        api_params = {
            "case_name": case_name,
            "json": {"show_case_rule_list_req": {"limit": case_data['limit'], "offset": 0, "showcase_type_filter": [],
                                                 "rule_status_filter": []}}
        }
        """
            2.发送请求（ hc=检查点对象, data=接口参数字典, query=接口请求体 ）
            common_request定义在项目的Proj/Zdemo/conftest.py中，其中的 init_common_request方法实例化了Proj/Zdemo/Config/common_request.py中的CommonRequest类
            并传入了env（默认stage）参数
            其中发送的本体send_http_request来自于你在项目中定义的：Proj/Marketing_Center/Config/common_request.py
        """
        common_request.send_http_request(hc=self.hc, data=api_params, query=Module_Name.ruleList)

        """
            3.添加基础检查点
            检查点方法，如check_status_code，定义在Common/http_client.py 的 check_status_code方法
        """
        self.hc.check_status_code(exp=200, msg="检查http响应码")  # 检查http响应码是否为200
        self.hc.check_response_less_than(exp=2000, msg="检查响应时间")  # 检查响应时间是否小于等于2秒
        self.hc.check_json_path_node_not_existent(path="errors", msg="检查响应中是否包含错误信息")  # 检查：响应信息中是否不存在'errors'节点内容

        # 4.添加业务检查点
        shop_id_list = self.hc.json_value(path=f"$..items[?(@.id=='{case_data['shop_id']}')]")  # 过滤出需要的shop_id数据内容列表
        # [{'id': '19554', 'operator_name': 'SI接口测试', 'showcase_type': 'SHOWCASE_TYPE_WELCOME' ....}]
        act_operator_name = shop_id_list[0].get('operator_name')
        self.hc.check_assert_equal(arg1=case_expect['exp_operator_name'], arg2=act_operator_name, msg="operator_name 检查通过")

        # 5.单接口断言并显示检查点结果
        self.hc.assert_and_show_checkpoint()

