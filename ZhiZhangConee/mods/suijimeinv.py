import requests

class SuijiMeinv:
    async def main(self, msg, nub):
        if msg.raw_message == "#看看美女":
            return {'try': 'image', 'text': self.get_url(), 'nub': nub}


    def get_url(self):
        url = "https://v2.xxapi.cn/api/meinvpic"
        payload = {}
        headers = {
            'User-Agent': 'xiaoxiaoapi/1.0.0'
        }
        response = requests.request("GET", url, headers=headers, data=payload).json()
        print(response["data"])
        url = response["data"]
        tu = requests.get(url,headers=headers)
        with open(r"data/zhizhang/3.jpg", "wb") as f:
            f.write(tu.content)
            f.close()
            return r"data/zhizhang/3.jpg"