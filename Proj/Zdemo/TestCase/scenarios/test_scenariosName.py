import pytest
from Proj.Zdemo.Config.config_api import Module_Name
from Common.http_client import HttpClient
from Common.scenarios_check import ScenariosCheck


class TestScenariosName:

    def setup(self):
        self.sc = ScenariosCheck()  # 初始化 场景用例检查对象

    def teardown(self):
        self.sc.get_scenario_case_result()  # 获取 场景用例执行结果

    @pytest.mark.SMOKING_BY_Zdemo
    def test_demo_scenarios_01(self, common_request, case_name, case_data, case_expect):
        """
            接口1：新增接口（ 验证新增成功，并获取新增记录的id ）
            接口2：查询接口（ 通过新增的id进行查询，验证新增的数据能够查询到 ）
            接口3：删除接口（ 通过新增的id进行删除，验证删除成功 ）
            接口4：查询接口（ 通过新增的id进行查询，验证无法查询到相应的数据）

            场景配置步骤：
            1.配置场景用例名称
            2.每个接口的配置步骤（ 整体放入'try-exception'中捕获异常情况并作异常标记 ）
             （1）配置接口参数
             （2）初始化'接口检查对象'并发送请求
             （3）添加基础检查点
             （4）添加业务检查点
             （5）'场景用例检查对象'添加'接口检查对象'
            3.场景断言并显示检查点结果
        """
        # 配置场景用例名称
        self.sc.add_scenarios_name(scenarios_name=case_name)
        try:
            # -------------------------------- 接口1 新增接口 --------------------------------
            # 配置接口参数
            api_params = {
                "case_name": "新增接口",
                "json": {"show_case_rule_list_req": {"limit": 10, "offset": 0, "showcase_type_filter": [],
                                                     "rule_status_filter": []}}
            }
            # 初始化'接口检查对象'并发送请求
            hc = HttpClient()
            common_request.send_http_request(hc=hc, data=api_params, query=Module_Name.ruleList)
            # 添加基础检查点
            hc.check_status_code(200)
            hc.check_response_less_than(exp=2000)
            # 添加业务检查点
            shop_id_list = hc.json_value(path=f"$..items[?(@.id=='19554')]")  # 过滤出需要的shop_id数据内容列表
            act_operator_name = shop_id_list[0].get('operator_name')
            hc.check_assert_equal(arg1=case_expect['exp_operator_name'], arg2=act_operator_name, msg="operator_name 检查通过")
            # '场景用例检查对象'添加'接口检查对象'
            self.sc.add_api_hc(hc=hc)

            # 获取新增的 id
            #id = hc.json_value("$.data.id")[0]
            id = "3641686349625898752"

            # -------------------------------- 接口2 查询接口 --------------------------------
            # 配置接口参数
            api_params = {
                "case_name": "查询接口",
                "json": {
                    "filters": {"app_client": 1, "user_id": "3604747655774140928", "company_id": id},
                    "form_slug": "bitable_device",
                    "offset": 0,
                    "limit": -1
                }
            }
            # 初始化'接口检查对象'并发送请求
            hc = HttpClient()
            common_request.send_http_request(hc=hc, data=api_params, query=Module_Name.searchFormValue)
            # 添加基础检查点
            hc.check_status_code(200)
            hc.check_response_less_than(exp=2000)
            # 添加业务检查点
            # 检查点1：店铺是否存在
            shop_name_jp = f"$..items[?(@.shop_id=='{case_data['shop_id']}')].shop_name"  # 获取店铺名列表
            shop_name_list = hc.json_value(path=shop_name_jp)
            if shop_name_list:
                hc.check_json_path_value_not_none(path=shop_name_jp, msg=f"期望的<{shop_name_list[0]}>店铺存在")
                # 检查点2：店铺中的设备状态是否在线
                sp_name_jp = f"$..items[?(@.shop_id=='{case_data['shop_id']}')].sp_name"  # 获取设备名列表
                sp_name_list = hc.json_value(path=sp_name_jp)
                for sp_name in sp_name_list:
                    act_sp_status = hc.json_value(path=f"$..items[?(@.sp_name=='{sp_name}')].status")[0]
                    hc.check_assert_equal(arg1=act_sp_status, arg2=case_expect['exp_sp_status'],
                                          msg=f"检查<{shop_name_list[0]}>店铺下的<{sp_name}>设备状态是否在线")
            else:
                hc.check_assert_equal(arg1=case_data['shop_id'], arg2=None, msg=f"期望的<{case_data['shop_id']}>店铺ID存在")
            # '场景用例检查对象'添加'接口检查对象'
            self.sc.add_api_hc(hc=hc)

        except Exception as e:
            self.sc.add_error_flag()

        # 场景断言并显示检查点结果
        self.sc.assert_and_show_checkpoint()

    def test_demo_scenarios_02(self, common_request, case_name, case_data, case_expect):
        """
            接口1：新增接口（ 验证新增成功，并获取新增记录的id ）
            接口2：查询接口（ 通过新增的id进行查询，验证新增的数据能够查询到 ）
            接口3：删除接口（ 通过新增的id进行删除，验证删除成功 ）
            接口4：查询接口（ 通过新增的id进行查询，验证无法查询到相应的数据）

            场景配置步骤：
            1.配置场景用例名称
            2.每个接口的配置步骤（ 整体放入'try-exception'中捕获异常情况并作异常标记 ）
             （1）配置接口参数
             （2）初始化'接口检查对象'并发送请求
             （3）添加基础检查点
             （4）添加业务检查点
             （5）'场景用例检查对象'添加'接口检查对象'
            3.场景断言并显示检查点结果
        """
        # 配置场景用例名称
        self.sc.add_scenarios_name(scenarios_name=case_name)
        try:
            # -------------------------------- 接口1 新增接口 --------------------------------
            # 配置接口参数
            api_params = {
                "case_name": "新增接口",
                "json": {"show_case_rule_list_req": {"limit": 10, "offset": 0, "showcase_type_filter": [],
                                                     "rule_status_filter": []}}
            }
            # 初始化'接口检查对象'并发送请求
            hc = HttpClient()
            common_request.send_http_request(hc=hc, data=api_params, query=Module_Name.ruleList)
            # 添加基础检查点
            hc.check_status_code(200)
            hc.check_response_less_than(exp=2000)
            # 添加业务检查点
            shop_id_list = hc.json_value(path=f"$..items[?(@.id=='19554')]")  # 过滤出需要的shop_id数据内容列表
            if shop_id_list:
                act_operator_name = shop_id_list[0].get('operator_name')
                hc.check_assert_equal(arg1=case_expect['exp_operator_name'], arg2=act_operator_name, msg="operator_name 检查通过")
                # '场景用例检查对象'添加'接口检查对象'
                self.sc.add_api_hc(hc=hc)

            # 获取新增的 id
            # id = hc.json_value("$.data.id")[0]
            id = "3641686349625898752"

            # -------------------------------- 接口2 查询接口 --------------------------------
            # 配置接口参数
            api_params = {
                "case_name": "查询接口",
                "json": {
                    "filters": {"app_client": 1, "user_id": "3604747655774140928", "company_id": id},
                    "form_slug": "bitable_device",
                    "offset": 0,
                    "limit": -1
                }
            }
            # 初始化'接口检查对象'并发送请求
            hc = HttpClient()
            common_request.send_http_request(hc=hc, data=api_params, query=Module_Name.searchFormValue)
            # 添加基础检查点
            hc.check_status_code(200)
            hc.check_response_less_than(exp=2000)
            # 添加业务检查点
            # 检查点1：店铺是否存在
            # shop_name_jp = f"$..items[?(@.shop_id=='{case_data['shop_id']}')].shop_name"  # 获取店铺名列表
            # if shop_name_jp:
            #     shop_name_list = hc.json_value(path=shop_name_jp)
            #     if shop_name_list:
            #         hc.check_json_path_value_not_none(path=shop_name_jp, msg=f"期望的<{shop_name_list[0]}>店铺存在")
            #         # 检查点2：店铺中的设备状态是否在线
            #         sp_name_jp = f"$..items[?(@.shop_id=='{case_data['shop_id']}')].sp_name"  # 获取设备名列表
            #         sp_name_list = hc.json_value(path=sp_name_jp)
            #         for sp_name in sp_name_list:
            #             act_sp_status = hc.json_value(path=f"$..items[?(@.sp_name=='{sp_name}')].status")[0]
            #             hc.check_assert_equal(arg1=act_sp_status, arg2=case_expect['exp_sp_status'],
            #                                   msg=f"检查<{shop_name_list[0]}>店铺下的<{sp_name}>设备状态是否在线")
            #     else:
            #         hc.check_assert_equal(arg1=case_data['shop_id'], arg2=None, msg=f"期望的<{case_data['shop_id']}>店铺ID存在")
            #     # '场景用例检查对象'添加'接口检查对象'
            #     self.sc.add_api_hc(hc=hc)

        except Exception as e:
            self.sc.add_error_flag()

        # 场景断言并显示检查点结果
        self.sc.assert_and_show_checkpoint()