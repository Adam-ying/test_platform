import os
import time
import pytest
from Proj.my_proj.Config.common_request import CommonRequest
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

