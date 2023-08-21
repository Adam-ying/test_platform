import time

import pytest
from Common.http_client import HttpClient, BodyType
from Proj.harbor.Config.config_api import QA
import allure


class TestQA:
    id = None
    comment_id = None

    def setup(self):
        self.hc = HttpClient()

    def teardown(self):
        self.hc.get_case_result()

    @pytest.mark.SMOKING_BY_HARBOR
    @allure.feature('harbor')
    @allure.story('检验问答库中的源数据')
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

    @pytest.mark.SMOKING_BY_HARBOR
    @allure.feature('harbor')
    @allure.story('检验问答库中的架构')
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

    @pytest.mark.SMOKING_BY_HARBOR
    @allure.feature('harbor')
    @allure.story('检验问答库中的创建问题')
    def test_createMaterial(self, common_request, case_name, case_data, case_expect):
        api_params = {
            "case_name": case_name,
            "method": case_data["method"],
            "url": case_data["url"],
            "body_type": BodyType.JSON,
            "body": {
                "name": "测测",
                "content_info": {
                    "content_module": {
                        "content": "[{\"insert\":\"测测\"},{\"attributes\""
                                   ":{\"title\":true},\"insert\":\"\\n\"},{\"insert\":\"收拾收拾\\n\"}]"
                    },
                    "type": 24
                },
                "source": 8
            }
        }

        common_request.send_http_requests(hc=self.hc, data=api_params)

        self.hc.check_status_code(exp=201, msg="检查http响应码")
        self.hc.check_response_less_than(exp=2000, msg="检查响应时间")
        self.hc.check_json_path_node_not_existent(path='error', msg='检查响应中是否包含错误信息')

        # 添加业务检查点
        self.__class__.id = self.hc.json_value(path='$.info.id')[0]

        # 单接口断言并显示检查点结果
        self.hc.assert_and_show_checkpoint()

    @pytest.mark.SMOKING_BY_HARBOR
    @allure.feature('harbor')
    @allure.story('检验问答库详情页创建评论')
    def test_createComment(self, common_request, case_name, case_data, case_expect):
        api_params = {
            "case_name": case_name,
            "json": {
                "create": {
                    "objectId": self.__class__.id,
                    "detail": "{\"name\":\"\",\"originContent\":[{\"insert\":\"123123123\\n\"}],\"content\":\"[{\\\"insert\\\":\\\"123123123\\\\n\\\"}]\"}",
                    "nickName": "应涛",
                    "avatar": "https://wos.meetwhale.com/2e8_TyM6-cCDV74jAteXs",
                    "type": 3,
                    "root_comment": "",
                    "upper_comment": "",
                    "properties": "",
                    "link": "https://whale-alivia.stage.meetwhale.com/assets-new/detail/3786449762877786368?space=Private&from=docQa",
                    "rich_text_delta": "{\"name\":\"\",\"originContent\":[{\"insert\":\"123123123\\n\"}],\"content\":\"[{\\\"insert\\\":\\\"123123123\\\\n\\\"}]\"}",
                    "reply_user_id": "",
                    "reply_nick_name": "",
                    "imgs": []
                }
            }
        }

        common_request.send_http_request(hc=self.hc, data=api_params, query=QA.createComment)

        self.hc.check_status_code(exp=200, msg="检查http响应码")
        self.hc.check_response_less_than(exp=2000, msg="检查响应时间")
        self.hc.check_json_path_node_not_existent(path='error', msg='检查响应中是否包含错误信息')

        self.__class__.comment_id = self.hc.json_value('$.data.createComment.id')[0]

        self.hc.assert_and_show_checkpoint()

    @pytest.mark.SMOKING_BY_HARBOR
    @allure.feature('harbor')
    @allure.story('检验问答库详情页评论是否加入到评论区')
    def test_getComments(self, common_request, case_name, case_data, case_expect):
        api_params = {
            "case_name": case_name,
            "method": case_data['method'],
            "url": case_data["url"],
            "body_type": BodyType.JSON,
            "body": {
                "object_id": self.__class__.id,
                "object_type": "RESOURCE",
                "comment_type": "GLOBAL_TYPE",
                "limit": -1,
                "page": 0,
                "asc": True,
                "order_by": "",
                "company_id": "",
                "user_id": ""
            }
        }

        common_request.send_http_requests(hc=self.hc, data=api_params)

        self.hc.check_status_code(exp=201, msg="检查http响应码")
        self.hc.check_response_less_than(exp=2000, msg="检查响应时间")
        self.hc.check_json_path_node_not_existent(path='error', msg='检查响应中是否包含错误信息')

        total_comments = set(self.hc.json_value('$..comment[?(@.id)][id]'))

        assert self.__class__.comment_id in total_comments

        self.hc.assert_and_show_checkpoint()

    @pytest.mark.SMOKING_BY_HARBOR
    @allure.feature('harbor')
    @allure.story('检验问答库详情页编辑问答的内容')
    def test_updateMaterial(self, common_request, case_name, case_data, case_expect):
        api_params = {
            "case_name": case_name,
            "method": case_data['method'],
            "url": case_data['url'],
            'body_type': BodyType.JSON,
            'body': {
                "resource_id": self.__class__.id,
                "content_info": {
                    "content_module": {
                        "content": "[{\"insert\":\"测测1\"},{\"attributes\":{\"title\":true},\"insert\":\"\\n\"},{\"insert\":\"收拾收拾123\\n\"}]",
                        "name": "测测1"
                    },
                    "type": 24
                },
                "source": 8
            }
        }

        common_request.send_http_requests(hc=self.hc, data=api_params)

        self.hc.check_status_code(exp=201, msg="检查http响应码")
        self.hc.check_response_less_than(exp=2000, msg="检查响应时间")
        self.hc.check_json_path_node_not_existent(path='error', msg='检查响应中是否包含错误信息')

        self.hc.json_value(path='$.info')

        self.hc.assert_and_show_checkpoint()

    @pytest.mark.SMOKING_BY_HARBOR
    @allure.feature('harbor')
    @allure.story('检验问答库详情页编辑问答的内容是否成功')
    def test_operateResource(self, common_request, case_name, case_data, case_expect):
        api_params = {
            "case_name": case_name,
            "method": case_data['method'],
            "url": case_data['url'],
            'body_type': BodyType.JSON,
            'body': {
                "name": "测测1",
                "res_ids": [
                    self.__class__.id
                ],
                "type": "Rename",
                "doc_type": "RES",
                "unsend_rename": True
            }
        }

        common_request.send_http_requests(hc=self.hc, data=api_params)

        self.hc.check_status_code(exp=201, msg="检查http响应码")
        self.hc.check_response_less_than(exp=2000, msg="检查响应时间")
        self.hc.check_json_path_node_not_existent(path='error', msg='检查响应中是否包含错误信息')

        assert self.hc.json_value(path='$.success_ids[0]')

        self.hc.assert_and_show_checkpoint()

    @pytest.mark.SMOKING_BY_HARBOR
    @allure.feature('harbor')
    @allure.story('检验问答库详情页编辑问答的内容标题同步列表页')
    def test_resourceTaskDetail(self, common_request, case_name, case_data, case_expect):
        api_params = {
            "case_name": case_name,
            "json": {
                "req": {
                    "id": self.__class__.id,
                    "user_id": "3606081813914904576w",
                    "company_id": "c53ac779-662f-4e2b-a63d-5fd351f0ef51"
                }
            }
        }

        time.sleep(1)

        common_request.send_http_request(hc=self.hc, data=api_params, query=QA.resourceTaskDetail)

        self.hc.check_status_code(exp=200, msg="检查http响应码")
        self.hc.check_response_less_than(exp=2000, msg="检查响应时间")
        self.hc.check_json_path_node_not_existent(path='error', msg='检查响应中是否包含错误信息')

        self.hc.json_value(path='$.data')

        self.hc.assert_and_show_checkpoint()

    @pytest.mark.SMOKING_BY_HARBOR
    @allure.feature('harbor')
    @allure.story('检验问答库详情页删除问答')
    def test_operateResource_delete(self, common_request, case_name, case_data, case_expect):
        api_params = {
            "case_name": case_name,
            "json": {
                "req": {
                    "type": "Delete",
                    "company_id": "c53ac779-662f-4e2b-a63d-5fd351f0ef51",
                    "res_ids": [
                        self.__class__.id
                    ]
                }
            }
        }

        common_request.send_http_request(hc=self.hc, data=api_params, query=QA.resourceTaskDetailDelete)

        self.hc.check_status_code(exp=200, msg="检查http响应码")
        self.hc.check_response_less_than(exp=2000, msg="检查响应时间")
        self.hc.check_json_path_node_not_existent(path='error', msg='检查响应中是否包含错误信息')

        res = self.hc.json_value(path='$.data.operateResource.code')[0]

        assert res == 0

        self.hc.assert_and_show_checkpoint()

    # 由于不知道什么原因 最后一个用例无法在allure报告上生成 所以加了一个用例用于最后一个防止不生成用例
    @pytest.mark.SMOKING_BY_HARBOR
    @allure.feature('harbor')
    @allure.story('最后的')
    def test_final(self, common_request, case_name, case_data, case_expect):
        pass


if __name__ == "__main__":
    pytest.main()
