import requests
import re
import os
from plugins.ZhiZhangConee.universl.io_json import json_file
from plugins.ZhiZhangConee.universl.permission import Permission
class TouxiangBaiLiaoQingBaoAnBiao:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54"
        }
    async def main(self, msg, nub):
        text = None
        if str(msg.raw_message).split(" ")[-1].split(":")[0] == '表情合成':
            try:
                qq_number = re.search(r'qq=(\d+)', str(msg)).group(1)
            except:
                qq_number = msg.raw_message.split(":")[1].split("=")[1].split("]")[0]
            if not qq_number or type(qq_number) != str:
                return {'try': 'text', 'text': '出错了呀，笨蛋', 'nub': nub}
            elif Permission.quanxian(qq_number) == 0 and Permission.quanxian(msg.user_id) != 0:
                return {'try': 'text', 'text': '禁止调戏主人', 'nub': nub}
            try:
                int(qq_number)
            except:
                return {'try': 'text', 'text': '请输入正确的QQ号', 'nub': nub}
            a = self.tou_get_img2(qq_number,str(msg.raw_message).split(":")[-1])
            return {'try': 'image' if a!=None else 'text' , 'text': a if a!=None else '服务暂未开启 ，联系主人开启后重试', 'nub': nub}


    def tou_get_img(self, qq_number):
        url = f"https://q.qlogo.cn/headimg_dl?dst_uin={qq_number}&spec=640"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            with open(f"plugins/ZhiZhangConee/data/10.png", "wb") as f:
                f.write(response.content)
            return r"plugins/ZhiZhangConee/data/10.png"
        else:
            return None

    def tou_get_img2(self, qq_number,name):
        url = json_file.get_json(r"plugins\ZhiZhangConee\data\url.json")["touxiang_url"]
        url = url+r"/generate_meme"
        data = {
            'image_path': os.getcwd()+"\\"+self.tou_get_img(qq_number),
            'meme_type': f'{name}',
            "id":qq_number,
            'circle': True
        }
        try:
            a = requests.post(url, json=data)
        except:
            return None
        if a.status_code!=200:
            return None

        with open(r'plugins/ZhiZhangConee/data/1.gif', 'wb') as f:
            f.write(a.content)
            f.close()
            return r"plugins\ZhiZhangConee\data\1.gif"
