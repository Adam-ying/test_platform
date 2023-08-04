import os

# 文件夹/文件路径处理
BaseDTR = os.path.dirname(os.path.dirname(__file__))
extract_yaml_path = os.path.join(BaseDTR, "Proj/oms/TestData/extract.yaml")

grpc_json_path = os.path.join(BaseDTR, "Proj/Grpc_Test/TestData/mapV2GameServiceStub_data.json")
login_account_json_path = os.path.join(BaseDTR, "Proj/account_center/TestData/login_account_center.json")

# Space_Intelligence 项目配置START

# SI TestData json文件配置
# SI_token_data_json_path = os.path.join(BaseDTR, "Proj/Space_Intelligence/Common/SI_token_data.json")
# DI_home_data_json_path = os.path.join(BaseDTR, "Proj/Space_Intelligence/Digital_Intelligence/TestData/test_home_data"
#                                                ".json")
#
# # SI 环境路径配置
# SI_base_prod_url = "https://whale-alivia.meetwhale.com/graphql"  # 帷幄测试Prod环境
# SI_base_stage_url = "https://whale-alivia.stage.meetwhale.com/graphql"  # 帷幄测试Stage环境
# SI_shop_stage_url = "https://whaleshop.stage.meetwhale.com/graphql"  # Whale帷幄Stage环境
# SI_tuhu_stage_url = "https://tuhu.stage.meetwhale.com/graphql"  # 途虎养车阿里云Stage环境
# SI_tuhu_tx_url = "https://alivia-tx.meetwhale.com/graphql"  # 途虎养车腾讯云Prod环境

# Space_Intelligence 项目配置END

# key值很多地方引用，谨慎修改(公共url配置)
URL_ENV_CONFIG = {
    "whale-alivia": {
        "prod": "https://whale-alivia.meetwhale.com/graphql",
        "stage": "https://whale-alivia.stage.meetwhale.com/graphql"
    },
    "whalewhale": {
        "prod": "https://whalewhale.meetwhale.com/graphql",
        "stage": "https://whalewhale.stage.meetwhale.com/graphql"
    },
    "whaleshop": {
        "stage": "https://whaleshop.stage.meetwhale.com/graphql"
    },
    "tuhu": {
        "stage": "https://tuhu.stage.meetwhale.com/graphql"
    },
    "alivia-tx": {
        "prod": "https://alivia-tx.meetwhale.com/graphql"
    },
    "wop": {
        "stage": "https://stardust.stage.meetwhale.com/graphql",
        "prod": "https://stardust.meetwhale.com/graphql"
    },
    "whale-account-center":{
        "stage": "https://whale-account-center.stage.meetwhale.com/user/login",
    }
}

# 环境路径管理
# 生产环境
# base_url = "https://whale-alivia.develop.meetwhale.com/graphql"

# product环境
# base_url = "https://whaleshop.meetwhale.com/graphql"

# stage环境
base_url = "https://whale-alivia.stage.meetwhale.com/graphql"

# 测试demo环境
# base_url = "https://demo.develop.meetwhale.com/graphql"

# 多云架构项目
account_center_base_url = "https://whale-account-center.develop.meetwhale.com"
account_database_config = {"database": 'account_center', "user": 'postgres', "password": 'Buzhongyao123',
                           "host": 'postgres.develop.meetwhale.com', "port": 5432}

# 测试报告聚合平台日志接入接口(线上)
reporter_api_online = "http://10.168.0.10:32498/api/import/execution_data"
reporter_api_online_2 = "http://10.168.0.10:30854/api/import/execution_data"

# 测试报告聚合平台日志接入接口(本地docker)
reporter_api_local = "http://localhost:1180/api/import/execution_data"

# 机器人webhook地址配置
webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/f24b7bf2-b70c-42f3-9e04-a0e1afe30fa3"

if __name__ == '__main__':
    print(BaseDTR)
