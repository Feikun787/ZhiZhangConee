import requests
class Zepp:
    async def zepp(self,msg,nub):
        text = None
        if msg.raw_message == "kepp帮助":
            text = """格式__kepp:keep账号:密码:步数"""
        if str(msg.raw_message).split(':')[0] == "zepp":
            a = str(msg.raw_message).split(':')
            text = self.kepp(a[1],a[2],a[-1])
        if text:
            return {'try':'text',"text":text,'nub':nub}

    def kepp(self,username, password, step):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }

        a = f'https://api.jiuhunwl.cn/api/yd_api.php?username={username}&password={password}&step={step}'
        a = requests.get(a, headers=headers).text.split(">")[-1]
        #a = dict(a)
        a = a.split(": ")
        if a[1].split(',')[0] == "200":
            b = f"账号：{a[3].split(',')[0]}\n步数：{a[4].split(',')[0]}\n"
        else:
            b = f"错误码：{a[1].split(',')[0]}"
        return b
    #https://api.jiuhunwl.cn/api/yd_api.php?username=3451263590@qq.com&password=333822lclzy&step={step}