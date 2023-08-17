import time

import pytest
from Common.http_client import HttpClient, BodyType
import allure

class TestDownload:
    id = None
    def setup(self):
        self.hc = HttpClient()

    def teardown(self):
        self.hc.get_case_result()


    @pytest.mark.SMOKING_BY_HARBOR
    @allure.feature('harbor')
    @allure.story('检验工作空间中下载')
    def test_operateResource(self, common_request, case_name, case_data, case_expect):
        api_params = {
            "case_name": case_name,
            "method": case_data['method'],
            "url": case_data['url'],
            "body_type": BodyType.JSON,
            "body": {
                "type": "Download",
                "res_ids": case_data["res_ids"],
                "folder_ids": case_data["folder_ids"]
            }
        }
        common_request.send_http_requests(hc=self.hc, data=api_params)

        self.hc.check_status_code(exp=201, msg="检查http响应码")
        self.hc.check_response_less_than(exp=3000, msg="检查响应时间")
        self.hc.check_json_path_node_not_existent(path='error', msg="检查响应中是否包含错误信息")

        self.__class__.id = self.hc.json_value(path='$.id')[0]



        self.hc.assert_and_show_checkpoint()
    @pytest.mark.SMOKING_BY_HARBOR
    @allure.feature('harbor')
    @allure.story('检验工作空间中下载是否成功')
    def test_getDownloadStatusHarbor(self, common_request, case_name, case_data, case_expect):


        api_params = {
            "case_name": case_name,
            "method": case_data["method"],
            "url": case_data['url'],
            "body_type": BodyType.JSON,
            "body": {
                "id": self.__class__.id
            }
        }
        common_request.send_http_requests(hc=self.hc, data=api_params)

        self.hc.check_status_code(exp=201, msg="检查http响应码")
        self.hc.check_response_less_than(exp=10000, msg="检查响应时间")
        self.hc.check_json_path_node_not_existent(path='error', msg="检查响应中是否包含错误信息")

        statu = self.hc.json_value(path='$.status')

        t1 = time.time()
        t2 = time.time()

        while t2 - t1 < 30 and statu[0] == 0:
            common_request.send_http_requests(hc=self.hc, data=api_params)

            self.hc.check_status_code(exp=201, msg="检查http响应码")
            self.hc.check_response_less_than(exp=2000, msg="检查响应时间")
            self.hc.check_json_path_node_not_existent(path='error', msg="检查响应中是否包含错误信息")

            statu = self.hc.json_value(path='$.status')
            time.sleep(3)
            t2 = time.time()

        self.hc.assert_and_show_checkpoint()

        assert statu[0] == 3


    @pytest.mark.SMOKING_BY_HARBOR
    @allure.feature('harbor')
    @allure.story('最后的')
    def test_final(self, common_request, case_name, case_data, case_expect):
        pass



if __name__ == "__main__":
    pytest.main()
