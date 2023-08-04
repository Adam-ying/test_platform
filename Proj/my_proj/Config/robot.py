import json
import time

import requests


class FeishuRobot:
    def __init__(self, webhook, header):
        self.webhook = webhook
        self.header = header

    def post_to_robot(self, info_head, info_content, info_url):
        data = {
            "msg_type": "interactive",
            "card": {
                "elements": [{
                    "tag": "div",
                    "text": {
                        "content": info_content,
                        "tag": "lark_md"
                    }
                }, {
                    "actions": [{
                        "tag": "button",
                        "text": {
                            "content": '详细问题please click here',
                            "tag": "lark_md"
                        },
                        "url": info_url,
                        "type": "default",
                        "value": {}
                    }],
                    "tag": "action"
                }],
                "header": {
                    "title": {
                        "content": info_head,
                        "tag": "plain_text"
                    }
                }
            }
        }

        # print(type(data))
        # print(type(json.dumps(data)))

        response = requests.request('Post', self.webhook, headers=self.header, data=json.dumps(data))
        return response

if __name__ == '__main__':
    webhook = 'https://open.feishu.cn/open-apis/bot/v2/hook/985dbc42-2509-4f91-9e68-9f71f155dabc'
    header = {'Content-Type': 'application/json'}
    robot = FeishuRobot(webhook, header)
    info_url = 'https://carlsberg.stage.meetwhale.com/vap/entry'
    info_title = '测试标题头'
    info_content = '测试内容'
    res = robot.post_to_robot(info_title, info_content, info_url)
    # print(res)
    # time.sleep(5)
