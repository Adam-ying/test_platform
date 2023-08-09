import pytest
from Common.http_client import HttpClient



class TestWorkSpace:
    def setup(self):
        self.hc = HttpClient()

    def teardown(self):
        self.hc.get_case_result()

    @pytest.mark.SMOKING_BY_HARBOR
    def test_getDocList(self, common_request, case_name, case_data, case_except):
        # 配置发送请求的参数
        api_params = {
            "case_name": case_name,
            "method": case_data['method'],
            "url": case_data['url'],
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
        common_request.send_http_requests(self.hc, api_params)

