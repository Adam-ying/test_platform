import os
import time
import allure
import pytest
from Common.http_client import HttpClient, BodyType
from Proj.my_proj.Config.robot import FeishuRobot
from Util.tools import del_path_files, login, del_report_files
from playwright.sync_api import sync_playwright


class TestCast:

    def setup(self):
        self.hc = HttpClient()  # 初始化 用例检查对象
        self.webhook = 'https://open.feishu.cn/open-apis/bot/v2/hook/985dbc42-2509-4f91-9e68-9f71f155dabc'
        self.header = {'Content-Type': 'application/json'}
        self.url = 'https://carlsberg.stage.meetwhale.com/vap/entry'
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.username = '18340378802'
        self.password = 'aA879736402'

    def teardown(self):
        self.hc.get_case_result()  # 获取用例执行结果并显示日志
        self.browser.close()
        self.playwright.stop()

    @allure.severity("critical")
    @allure.epic("项目名称：首页数据概览")
    @allure.feature("cast")
    @allure.story("测试cast首页是否可以打开；测试数据概览中数据与数据库是否一致")
    @allure.issue('https://whale-alivia.stage.meetwhale.com/vap/audio-video-analysis')
    @allure.testcase('https://whales.feishu.cn/sheets/Az4HsU8sIhsqXotHYuAcV1din5f?sheet=c2ab2d')
    @pytest.mark.SMOKING_BY_my_proj
    def test_getDataEvaluate(self, common_request, case_name, case_data, case_expect):
        """
            单接口配置步骤：1.配置接口参数、2.发送请求、3.添加基础检查点、4.添加业务检查点、5.单接口断言并显示检查点结果
        """
        # 1.配置接口参数
        api_params = {
            "case_name": case_name,
            "method": case_data['method'],
            "url": case_data['url'],
            "body_type": BodyType.JSON,
            "body": {
                "base": {
                    "type": "VisualAngleCommerce",
                    "user_id": "3606081813914904576w",
                    "company_id": "3641857710273712640",
                    "start_time": 1688572800,
                    "end_time": 1689177599,
                    "douyin_no": "wusu868688",
                    "target_interval": "TARGET_INTERVAL_DAY"
                }
            },
            "params": None
        }

        # 登陆cast首页用于allure网页报告的截图
        page = login(self.username, self.password, self.page)
        if page.url == self.url:
            pass
        else:
            page.locator("img").nth(2).click()
            page.hover('//*[@class="ant-dropdown-menu-submenu-title"]')
            page.get_by_text("嘉士伯").click()
            page.get_by_role("button", name="确 定").click()
            page.wait_for_timeout(3000)

        allure.attach(page.screenshot(), '概览首页', allure.attachment_type.PNG)

        """
            2.发送请求（ hc=检查点对象, data=接口参数字典, query=接口请求体 ）
            common_request定义在项目的Proj/Zdemo/conftest.py中，其中的 init_common_request方法实例化了Proj/Zdemo/Config/common_request.py中的CommonRequest类
            并传入了env（默认stage）参数
            其中发送的本体send_http_request来自于你在项目中定义的：Proj/Marketing_Center/Config/common_request.py
        """
        common_request.send_http_request_by_other(hc=self.hc, data=api_params)

        """
            3.添加基础检查点
            检查点方法，如check_status_code，定义在Common/http_client.py 的 check_status_code方法
        """
        self.hc.check_status_code(exp=201, msg="检查http响应码")  # 检查http响应码是否为200
        self.hc.check_response_less_than(exp=2000, msg="检查响应时间")  # 检查响应时间是否小于等于2秒
        self.hc.check_json_path_node_not_existent(path="errors",
                                                  msg="检查响应中是否包含错误信息")  # 检查：响应信息中是否不存在'errors'节点内容
        if self.hc.status_code != 201:
            robot = FeishuRobot(self.webhook, self.header)
            robot.post_to_robot(api_params.get('case_name'), f"检查响应码为{self.hc.status_code}",
                                "https://carlsberg.stage.meetwhale.com/graphql")

        # 4.添加业务检查点
        self.hc.check_json_path_value_not_none(path="$.items")

        # 5.单接口断言并显示检查点结果
        self.hc.assert_and_show_checkpoint()

    # 【概览】漏斗指标
    @allure.severity("critical")
    @allure.epic("项目名称：首页数据概览")
    @allure.feature("cast")
    @pytest.mark.SMOKING_BY_my_proj
    def test_getFunnelViewData(self, common_request, case_name, case_data, case_expect):
        # 1.配置接口参数
        api_data = {
            "case_name": case_name,
            "method": case_data['method'],
            "url": case_data['url'],
            "body_type": BodyType.JSON,
            "body": {
                "funnel_view_type": case_data['funnel_view_type'],  # 不同指标，有4次请求
                "douyin_no": "wusu868688",
                "start_time": 1688572800,
                "end_time": 1689177599
            },
            "params": None
        }
        # 2.发送请求（ hc=检查点对象, data=接口参数字典, query=接口请求体 ）
        common_request.send_http_request_by_other(hc=self.hc, data=api_data)

        # 3.添加基础检查点
        self.hc.check_status_code(exp=201, msg="检查http响应码")  # 检查http响应码是否为200 有的是不一定是200
        self.hc.check_response_less_than(exp=2000, msg="检查响应时间")  # 检查响应时间是否小于等于2秒
        self.hc.check_json_path_node_not_existent(path="errors",
                                                  msg="检查响应中是否包含错误信息")  # 检查：响应信息中是否不存在'errors'节点内容
        if self.hc.status_code != 201:
            alert = FeishuRobot()
            title = "【概览】漏斗指标接口报错"
            content = f"getFunnelViewData接口状态码返回不对"
            alert.post_to_robot(title, content)

        # 4.添加业务检查点
        res = self.hc.json_value(path='$.items[?(@.display_name)]')
        # res_list = []
        # for i in res:
        #     if i['value'] == "0":
        #         res_list.append(i['display_name'])
        # # 去除不要告警的指标
        # no_list = ['曝光-成交率（人数）', '观看-成交率（人数）', '曝光-观看率（人数）', '观看-商品曝光率（人数）',
        #            '商品曝光-点击率（人数）', '商品点击-成交率（人数）', '曝光-互动率（人数）', '曝光-观看率（人数）',
        #            '观看-互动率（人数）', '曝光-关注率（人数）', '观看-关注率（人数）', '曝光-加团率（人数）',
        #            '观看-加团率（人数）']
        # for j in no_list:
        #     if j in res_list:
        #         res_list.remove(j)
        # if len(res_list) != 0:
        #     alert = FeishuAlert()
        #     title = "【概览】漏斗指标为0"
        #     content = f"数据为0的指标有{str(res_list)}"
        #     alert.post_to_robot(title, content)
        # 5.单接口断言并显示检查点结果
        self.hc.assert_and_show_checkpoint()


if __name__ == "__main__":
    pytest.main()
