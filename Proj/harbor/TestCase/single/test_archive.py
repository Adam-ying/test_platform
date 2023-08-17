import pytest
from Common.http_client import HttpClient, BodyType
import allure

class TestArchive:
    def setup(self):
        self.hc = HttpClient()

    def teardown(self):
        self.hc.get_case_result()
    @pytest.mark.SMOKING_BY_HARBOR
    @allure.feature('harbor')
    @allure.story('检验归档操作')
    def test_batchUpdateArchiveStatus(self, common_request, case_name, case_data, case_expect):
        api_params = {
            "case_name": case_name,
            "method": case_data['method'],
            "url": case_data["url"],
            "body_type": BodyType.JSON,
            "body": {
                "resource_ids": case_data['resource_ids'],
                "folder_ids": case_data['folder_ids'],
                "status": case_data['status']
            }
        }

        common_request.send_http_requests(hc=self.hc, data=api_params)

        self.hc.check_status_code(exp=201, msg="检查http响应码")
        self.hc.check_response_less_than(exp=2000, msg="检查响应时间")
        self.hc.check_json_path_node_not_existent(path='error', msg='检查响应中是否包含错误信息')

        self.hc.json_value(path='$.success_ids')

        self.hc.assert_and_show_checkpoint()

    @pytest.mark.SMOKING_BY_HARBOR
    @allure.feature('harbor')
    @allure.story('最后的')
    def test_final(self, common_request, case_name, case_data, case_expect):
        pass

if __name__ == "__main__":
    pytest.main()
