# 登录接口
class Login_Token:
    GET_TOKEN = "mutation getToken($username: String!, $password: String!) {\n  getToken(username: $username, " \
                "password: $password, app_client: 1) {\n    token\n    user {\n      id\n      phone\n      " \
                "nick_name\n      real_name\n      avatar\n      create_time\n      need_login_verify\n      role\n    " \
                "  company_id\n      company_slug\n      shop_ids\n      company {\n        id\n        name\n        " \
                "logo\n      }\n      new_permissions\n      roles {\n        id\n        name\n        description\n  " \
                "      create_time\n        role_type\n        permissions {\n          id\n          name\n          " \
                "description\n          method\n          status\n          create_time\n        }\n      }\n      " \
                "shop_ids\n      company_list\n    }\n    auth {\n      tabs {\n        id\n        name\n        " \
                "path\n        sort\n        icon\n        is_nav\n        parent_id\n        app_id\n        " \
                "parent_app\n      }\n      employee_id\n      is_super\n      is_admin\n      is_wanning\n    }\n  " \
                "}\n}\n "


# 模块名(类名) - 接口名(类属性)
class QA:
    resourceQaService_getResourceQaList = "query resourceQaService_getResourceQaList($req: Qa_ResourceQaListReq) {\n  resourceQaService_getResourceQaList(req: $req) {\n    resource_qa {\n      name\n      tags {\n        id\n        name\n      }\n      like_num\n      browse_num\n      owner_id\n      publish_time\n      newest_answer_time\n      publish_status\n      doc_id\n      resource_id\n      top_status\n      selected_status\n      answerers\n    }\n    total\n  }\n}\n"
    tableModel = "query tableModel($request: ListFieldsByObjIdReq) {\n  tableModel(request: $request) {\n    fields {\n      field_id\n      compares\n      setting {\n        id\n        name\n        en_name\n        desc\n        key\n        field_type\n        filter_order\n        table_order\n        desc\n        en_desc\n        sort_order\n        enum_value {\n          value: key\n          text: value\n        }\n        must\n        edit_type\n        enum_map\n        display_type\n        enum_items {\n          key\n          value\n          desc\n          en_value\n          en_desc\n          meta {\n            color\n          }\n        }\n        config\n        sort_list_order\n        group_list_order\n      }\n    }\n    permission\n  }\n}\n"
