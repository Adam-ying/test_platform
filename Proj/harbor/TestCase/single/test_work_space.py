import pytest
from Common.http_client import HttpClient, BodyType
from Proj.harbor.Config.robot import FeishuRobot


class TestWorkSpace:
    def setup(self):
        self.hc = HttpClient()
        # self.robot = FeishuRobot()

    def teardown(self):
        self.hc.get_case_result()

    @pytest.mark.SMOKING_BY_HARBOR
    def test_getDocList(self, common_request, case_name, case_data, case_expect):
        # 配置发送请求的参数
        api_params = {
            "case_name": case_name,
            "method": case_data['method'],
            "url": case_data['url'],
            "body_type": BodyType.JSON,
            "body": {
                "search_req": {
                    "offset": case_data["offset"],
                    "limit": case_data['limit'],
                    "user_id": case_data["user_id"],
                    "company_id": case_data["company_id"],
                    "space": case_data["space"],
                    "order_by": case_data["order_by"],
                    "order_by_type": case_data["order_by_type"],
                    "condition": case_data["condition"]
                },
                "enable_group": False
            }
        }

        # 发送请求
        common_request.send_http_requests(hc=self.hc, data=api_params)

        # 添加基础检查点
        self.hc.check_status_code(exp=201, msg="检查http响应码")
        self.hc.check_response_less_than(exp=2000, msg="检查响应时间")
        self.hc.check_json_path_node_not_existent(path='error', msg='检查响应中是否包含错误信息')

        # 添加业务检查点
        self.hc.json_value(path='$.files')

        # 单接口断言并显示检查点结果
        self.hc.assert_and_show_checkpoint()

    @pytest.mark.SMOKING_BY_HARBOR
    def test_getFolderChildren(self, common_request, case_name, case_data, case_expect):
        api_params = {
            "case_name": case_name,
            "method": case_data['method'],
            "url": case_data['url'],
            "body_type": BodyType.JSON,
            "body": {
                "search_req": {
                    "order_by": case_data['order_by'],
                    "order_by_type": case_data['order_by_type'],
                    "user_id": case_data['user_id'],
                    "limit": case_data['limit'],
                    "offset": case_data['offset'],
                    "tag_ids": case_data['tag_ids'],
                    "condition": case_data['condition'],
                    "space": case_data['space'],
                    "company_id": case_data['company_id']
                }
            }

        }

        common_request.send_http_requests(hc=self.hc, data=api_params)

        # 添加基础检查点
        self.hc.check_status_code(exp=201, msg="检查http响应码")
        self.hc.check_response_less_than(exp=2000, msg="检查响应时间")
        self.hc.check_json_path_node_not_existent(path='error', msg='检查响应中是否包含错误信息')

        # 添加业务检查点
        self.hc.json_value(path='$.files')

        # 单接口断言并显示检查点结果
        self.hc.assert_and_show_checkpoint()

    @pytest.mark.SMOKING_BY_HARBOR
    def test_getArchivedList1(self, common_request, case_name, case_data, case_expect):
        api_params = {
            "case_name": case_name,
            "url": case_data['url'],
            "method": case_data['method'],
            "body_type": BodyType.JSON,
            "body": {
                "limit": 50,
                "offset": 0,
                "company_id": "c53ac779-662f-4e2b-a63d-5fd351f0ef51",
                "user_id": "3606081813914904576w",
                "cond": {
                    "type": "RES",
                    "order_by": "UpdateTime",
                    "sort": "Desc",
                    "scope": "null",
                    "doc_type": {}
                }
            }
        }

        common_request.send_http_requests(hc=self.hc, data=api_params)

        self.hc.check_status_code(exp=201, msg="检查http响应码")
        self.hc.check_response_less_than(exp=2000, msg="检查响应时间")
        self.hc.check_json_path_node_not_existent(path="error", msg='检查响应中是否包含错误信息')

        # 添加业务检查点
        self.hc.json_value(path='$.files')

        # 单接口断言并显示检查点结果
        self.hc.assert_and_show_checkpoint()

    def test_getArchivedList2(self, common_request, case_name, case_data, case_expect):
        api_params = {
            "case_name": case_name,
            "method": case_data['method'],
            "url": case_data['url'],
            "body_type": BodyType.JSON,
            "body": {

                "limit": 60,
                "offset": 0,
                "cond": {
                    "type": "FOLDER",
                    "order_by": "UpdateTime",
                    "order_by_type": "DESC",
                    "scope": 'null',
                    "doc_type": {}

                }
            }
        }

        common_request.send_http_requests(hc=self.hc, data=api_params)

        self.hc.check_status_code(exp=201, msg="检查http响应码")
        self.hc.check_response_less_than(exp=2000, msg="检查响应时间")
        self.hc.check_json_path_node_not_existent("error", '检查响应中是否包含错误信息')

        self.hc.json_value(path='$.files')

        self.hc.assert_and_show_checkpoint()



if __name__ == "__main__":
    pytest.main()
