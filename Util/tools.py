import os
import shutil

# 删除目录下的文件
def del_path_files(path:str):
    file_list = os.listdir(path)

    for file_name in file_list:
        file_path = os.path.join(path, file_name)
        os.remove(file_path)

#删除目录下的部分文件
def del_report_files(path:str, nums:int):
    file_list  = os.listdir(path)
    file_list = sorted(file_list)
    if len(file_list) > nums:
        for i, file_name in enumerate(file_list):
            if i == nums:
                break
            else:
                shutil.rmtree(os.path.join(path, file_name))


# 获取项目路径
def project_path():
    return os.path.dirname(os.path.dirname(__file__))


# 登陆whale首页（需要创建一个为文档测试的文件夹）
def login(username, password, page):
    page.goto("https://whale-login.stage.meetwhale.com/login")
    page.get_by_placeholder("请输入手机号").click()
    page.get_by_placeholder("请输入手机号").fill(username)
    page.get_by_placeholder("请输入密码").click()
    page.get_by_placeholder("请输入密码").fill(password)
    page.get_by_label("我已阅读并同意 服务协议 和 隐私政策").check()
    page.get_by_role("button", name="登 录").click()
    page.wait_for_load_state(state='networkidle')
    return page

if __name__ == "__main__":
    print(project_path())
    print(os.getcwd())
