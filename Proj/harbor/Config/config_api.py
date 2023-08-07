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
class Module_Name:
    ruleList = "query ruleList($show_case_rule_list_req: IShowCaseRuleListReq) {\n  ruleList(show_case_rule_list_req: $show_case_rule_list_req) {\n    items {\n      id\n      create_time\n      update_time\n      name\n      showcase_type\n      showcase_rule_status\n      rule_display_status\n      periods {\n        period\n        period_display_status\n      }\n      operator\n      operator_name\n      company_id\n      template_id\n      priority\n      screen_num\n      rule_display_put_status\n      template {\n        template_id\n        template_name\n        resource_ids\n      }\n      source_type\n      rule_size\n      cached_num\n      total_num\n    }\n    total\n    offset\n    limit\n  }\n}\n"
    searchFormValue = "query searchFormValue($form_slug: String, $form_id: String, $filters: JSON, $limit: Int, $offset: Int) {\n  searchFormValue(form_slug: $form_slug, form_id: $form_id, filters: $filters, offset: $offset, limit: $limit) {\n    items\n    total\n    limit\n    offset\n  }\n}\n"
