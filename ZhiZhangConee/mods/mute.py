from plugins.ZhiZhangConee.universl.permission import Permission

class Mute:
    async def mute(self,msg,nub):
        text = None
        if msg.raw_message == '禁言帮助':
            text = "格式————@xxx 禁言:阿拉伯数字"
        if str(msg.raw_message).split(']')[-1].split(':')[0] == ' 禁言':
            if Permission.quanxian(msg.user_id) == 0 or Permission.quanxian(msg.user_id) == 1:#权限设置
                mubiao = str(msg.raw_message).split('=')[-1].split(']')[0]
                try:
                    a= await self.api.set_group_ban(msg.group_id,mubiao,60*int(msg.raw_message.split(']')[-1].split(':')[-1]))
                    text = "禁言失败"
                except Exception as e:
                    text = "禁言失败"
                if a['status'] == 'ok':
                    text = f'{mubiao}已经禁言{(msg.raw_message.split(']')[-1].split(':')[-1])}分钟'
            else:
                text = "权限不足"
        if text:
            return {'try': 'text', "text": text, 'nub': nub}