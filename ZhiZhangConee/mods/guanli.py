from plugins.ZhiZhangConee.universl.permission import Permission
from plugins.ZhiZhangConee.universl.io_json import json_file

class GuanLiYuan:
    async def guanliyuan(self,msg,nub):
        text = None
        if msg.raw_message == '管理帮助':
            text = "格式————@XX:管理添加or删除"
        if str(msg.raw_message).split(':')[-1] == '管理添加':
            if Permission.quanxian(msg.user_id) == 0:
                mubiao = str(msg.raw_message).split('=')[-1].split(']')[0]
                a = self.add_guanliy(mubiao)
                if a:
                    text = f"{mubiao}已经成为该智障机器人管理员"
                else:
                    text = f"{mubiao}已经是该智障机器人管理员"
            else:
                text = "权限不足"
        elif str(msg.raw_message).split(':')[-1] == '管理删除':
            if Permission.quanxian(msg.user_id) == 0:
                mubiao = str(msg.raw_message).split('=')[-1].split(']')[0]
                a = self.del_guanliy(mubiao)
                if a:
                    text = f"{mubiao}该智障机器人管理员已经删除"
                else:
                    text = f'{mubiao}还不是该智障机器人管理员'
            else:
                text = "权限不足"
        if text:
            return {'try': 'text', "text": text, 'nub': nub}

    #添加管理员
    def add_guanliy(self,id):
        data = json_file.get_json('plugins/ZhiZhangConee/data/ZhiZhangCon_quanxian.json')
        try:
            a = self.add_unique(data['gly_qq'], int(id))
            json_file.set_json(data,'plugins/ZhiZhangConee/data/ZhiZhangCon_quanxian.json')
        except Exception as e:
            a = False
            print(e)
        return a
    #删除管理员
    def del_guanliy(self,id):
        data = json_file.get_json('plugins/ZhiZhangConee/data/ZhiZhangCon_quanxian.json')
        try:
            data['gly_qq'].remove(int(id))
            json_file.set_json(data,'plugins/ZhiZhangConee/data/ZhiZhangCon_quanxian.json')
        except Exception as e:
            return False
        return True

    def add_unique(self,lst, item):
        if item not in lst:
            lst.append(item)
            return True
        else:
            return False

