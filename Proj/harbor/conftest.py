import os
import pytest
from Proj.harbor.Config.common_request import CommonRequest
from Util.tools import del_path_files, del_report_files



@pytest.fixture(scope="module", autouse=True, name="common_request")
def init_common_request(request):
    """
        初始化公共接口对象（获取登录token）
        备注：当前项目下 执行每个test_xxx.py文件中的用例前执行一次
    """
    env = request.config.getoption("--execute-env")  # 获取执行环境（从命令行参数）
    common_request = CommonRequest(env=env)
    return common_request


@pytest.fixture(scope="module", autouse=True)
def generate_allure_report(request):
    del_path_files('/Users/edz/PycharmProjects/test_platform/Temps')
    yield
    # 获取当前测试用例的节点对象
    node = request.node
    # 获取节点对象的完整路径
    node_path = node.nodeid
    # 提取出文件名部分
    file_name = os.path.basename(node_path).split(".py")[0]

    os.system('allure generate /Users/edz/PycharmProjects/test_platform/Temps'
              f' -o /Users/edz/PycharmProjects/test_platform/Proj/harbor/Report_{file_name} --clean' )
