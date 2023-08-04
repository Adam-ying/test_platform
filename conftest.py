import pytest
from Util.logger_util import info_log
import time, os
from Util.tools import project_path
from Common.common_func import read_yaml_params
from Util.tools import del_path_files, del_report_files


@pytest.fixture(scope="session", autouse=True)
def proj_config():
    """ 记录 整个项目执行起止时间（项目维度执行一次）"""
    info_log(f"项目开始时间：{time.time()}\n\n")
    yield
    info_log(f"项目结束时间：{time.time()}")


@pytest.fixture(scope="function", autouse=True)
def case_config():
    """ 记录 每个用例执行起止时间（每一个用例都会执行）"""
    info_log(f"用例开始时间：{time.time()}\n")
    yield
    info_log(f"用例结束时间：{time.time()}\n\n")


def pytest_addoption(parser):
    """ 注册自定义参数到配置对象 """
    parser.addoption("--execute-env", action="store", default="stage", choices=["test", "stage", "prod"], help="执行环境")
    parser.addoption("--case-name", action="store", default=None, help="用例名称")


def pytest_collection_modifyitems(items):
    """
        测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
        ( 解决 用例名称 ids=[] 显示乱码的问题 )
    """
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode-escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')



def pytest_generate_tests(metafunc):
    """
        使用钩子配置 用例参数化数据

        metafunc.fixturenames:  参数化收集时的参数名称
        metafunc.module:        使用参数名称进行参数化的测试用例所在的模块d对象
        metafunc.config:        测试用例会话
        metafunc.function:      测试用例对象,即函数或方法对象
        metafunc.cls:           测试用例所属的类的类对象
    """
    # 获取命令行参数
    env = metafunc.config.getoption("--execute-env")      # 执行环境
    case_name = metafunc.config.getoption("--case-name")  # 指定运行的用例名称

    # 正在运行的测试函数的函数名或方法名(类名.函数名)
    current_func_name_str = metafunc.function.__qualname__
    current_func_name = current_func_name_str.split(".")[-1]

    # 正在运行的测试函数所在模块的名字(项目名.TestCase.scenarios.模块(py)名)
    current_function_in_module_name_str = metafunc.module.__dict__['__name__']
    tmp_list = current_function_in_module_name_str.split(".")
    # 这里避免metafunc方法中pro_name可能为Proj目录名，最终去../Proj/Proj/..目录下去寻找params，导致无法拿到用例名称的问题
    pro_name = tmp_list[0] if tmp_list[0] != 'Proj' else tmp_list[1] # 项目名称
    module_name = tmp_list[-1]  # 模块名称

    # 获取用例参数yml文件
    params_file = os.path.join(project_path(), "Proj", pro_name, "Params", env, f"{module_name}.yml")
    res_data = read_yaml_params(params_file=params_file, test_func_name=current_func_name)
    all_case_parametrize = []  # 所有测试函数的参数化的测试数据（ 用例名称、测试数据、预期结果 ）
    case_parametrize = []
    for data in res_data:
        params = data.get(current_func_name)
        # print(params)
        case_parametrize.clear()
        case_parametrize.append(params['case_name'])
        if params.get("case_data"):
            case_parametrize.append(params['case_data'])
        else:
            case_parametrize.append(dict())
        if params.get("case_expect"):
            case_parametrize.append(params['case_expect'])
        else:
            case_parametrize.append(dict())
        all_case_parametrize.append(tuple(case_parametrize))


    # 若指定运行的用例名称存在，则过滤掉其他的参数化用例数据
    if case_name:
        all_case_parametrize = list(filter(lambda x: x[0] == case_name, all_case_parametrize))

    # 在测试用例运行前，对测试函数进行参数化设置。
    metafunc.parametrize("case_name, case_data, case_expect", all_case_parametrize)

    # 垃圾回收
    del all_case_parametrize
    del case_parametrize

    # 删除allure生成的源文件
    del_path_files(os.path.join(project_path(), "Proj", pro_name, "Temps",))

    # -------------------------- 上述整合配置的原型如下 --------------------------
    # metafunc.parametrize("case_name, case_data, case_expect",
    #                      [("获取某产品的测试执行结果_01", {'projectName': 'Digital_Intelligence_web'}, {'exp_code': 1000}),
    #                       ('获取某产品的测试执行结果_02', {'projectName': 'Digital_Intelligence_web'}, {'exp_code': 1001})])

