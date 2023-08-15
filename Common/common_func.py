from Util.tools import project_path
import os, yaml


def read_yaml_params(params_file, test_func_name):
    """
        读取用例参数配置文件
        params_file：用例参数文件
        test_func_name：测试函数名称
        return：返回用例函数名称对应的 数据字典列表

        备注：yml文件以 "---" 来区分多个文档
             若某用例函数需要多个参数化配置，则使用"---"来配置多个同名用例函数名称 进行参数化
    """
    res_data = []
    try:
        with open(params_file, encoding="utf-8") as f:
            document_list = list(yaml.load_all(f, Loader=yaml.Loader))  # 获取文档字典列表
            for document_dict in document_list:
                for key, value in document_dict.items():
                    if key == test_func_name:
                        res_data.append({test_func_name: value})
            return res_data
    except Exception as e:
        # print(f"e -------- {e}")
        return res_data


if __name__ == '__main__':
    yml_file = os.path.join(project_path(), "Proj", "harbor", "Params", "stage", "test_work_space.yml")
    print(yml_file)
    test_func_name = "test_getDocList"
    with open(yml_file, encoding="utf-8") as f:
        document_list = list(yaml.load_all(f, Loader=yaml.Loader))  # 获取文档字典列表

    # res_list = read_yaml_params(yml_file, test_func_name)
    # print(res_list)
    # case_name_list = []
    # for each in res_list:
    #     print(each)
    #     for item in each.values():
    #         print(item)
    #         case_name_list.append(item.get("case_name"))
    # print(case_name_list)
