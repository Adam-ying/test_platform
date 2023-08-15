import pytest
from Common.http_client import HttpClient, BodyType
from Proj.harbor.Config.config_api import QA


class TestQA:
    def setup(self):
        self.hc = HttpClient()

    def teardown(self):
        self.hc.get_case_result()

    def test_resourceQaService_getResourceQaList(self, common_request, case_name, case_data, case_expect):
        api_params = {
            "case_name": case_name,
            "json": {
                "req": {
                    "offset": 0,
                    "limit": 100,
                    "condition": {
                        "and": True,
                        "operator": []
                    },
                    "common_column": "All"
                }
            }
        }

        common_request.send_http_request(hc=self.hc, data=api_params,
                                         query=QA.resourceQaService_getResourceQaList)

        # 添加基础检查点
        self.hc.check_status_code(exp=200, msg="检查http响应码")
        self.hc.check_response_less_than(exp=2000, msg="检查响应时间")
        self.hc.check_json_path_node_not_existent(path='error', msg='检查响应中是否包含错误信息')

        # 添加业务检查点
        self.hc.json_value(path='$.data')

        # 单接口断言并显示检查点结果
        self.hc.assert_and_show_checkpoint()

    def test_tableModel(self, common_request, case_name, case_data, case_expect):
        api_params = {
            "case_name": case_name,
            "json": {
                "request": {
                    "form_slug": "alivia_content_qa"
                }
            }
        }

        common_request.send_http_request(hc=self.hc, data=api_params, query=QA.tableModel)

        self.hc.check_status_code(exp=200, msg="检查http响应码")
        self.hc.check_response_less_than(exp=2000, msg="检查响应时间")
        self.hc.check_json_path_node_not_existent(path='error', msg='检查响应中是否包含错误信息')

        # 添加业务检查点
        self.hc.json_value(path='$.data')

        # 单接口断言并显示检查点结果
        self.hc.assert_and_show_checkpoint()


if __name__ == "__main__":
    pytest.main()
