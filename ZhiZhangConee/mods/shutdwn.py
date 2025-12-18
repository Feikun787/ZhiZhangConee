import os

from plugins.ZhiZhangConee.universl.permission import Permission


class Shutdown:
    async def shutdown(self,msg,nub):
        text = None
        if msg.raw_message == '电脑关机':
            print(Permission.quanxian(msg.user_id))
            if Permission.quanxian(msg.user_id) == 0:
                os.system('shutdown -s -t 120')
                text = "将在两分钟后关机"
            else:
                text = "权限不足"
        if msg.raw_message == "取消关机":
            if Permission.quanxian(msg.user_id) == 0:
                os.system('shutdown -a')
                text = "已取消关机"
            else:
                text = "权限不足"
        if text:
            return {'try': 'text', "text": text, 'nub': nub}
