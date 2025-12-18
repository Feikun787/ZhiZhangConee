import requests
import json
import os
class AgeSetu:
    def __init__(self):
        # 定义消息映射字典
        self.message_mapping = {
            "#看看二次元美女": "https://moe.jitsu.top/api",
            "#看看原神美女": "https://api.suyanw.cn/api/ys/",
            "#看看腿": "https://api.lolimi.cn/API/meizi/api.php?type=image",
            "#看看二次元美女2": "https://api.lolimi.cn/API/meizi/api.php?type=image",
            "#原神r18": "https://image.anosu.top/pixiv/direct?r18=1&keyword=arknights",
            "#看看帅哥":"https://www.cunyuapi.top/handsome"
        }
    async def main(self, msg, nub):
        # 检查消息是否在映射字典中
        if msg.raw_message in self.message_mapping:
            url = self.message_mapping[msg.raw_message]
            # 如果是#看看帅哥
            if msg.raw_message == "#看看帅哥":
                url = json.loads(requests.get(url).text)["img"]
            text =[
                {"type": "text", "data": {"text": "看吧涩批" if msg.raw_message != "#看看帅哥" else "看吧女涩批"}},
                {"type": "image", "data": {"file": f"{os.getcwd()}/"+self.get_age(url)}}
                    ]
            return {'try': 'rtf', 'text': text, 'nub': nub}
        return None
    def get_age(self, url):
        headers = {
            'Authorization': "Bearer 0c5d5f0c-d0c5-4c5d-b0c5-5fd0c5f5d0c5",
            'content-type': "application/json"
        }
        data = requests.get(url, headers=headers)
        with open(r"plugins/ZhiZhangConee/data/4.jpg", "wb") as f:
            f.write(data.content)
            f.close()
            return r"plugins/ZhiZhangConee/data/4.jpg"

