import random


class CaiShuZi:
    async def caishuzi(self,msg,nub):
        text = None
        if msg.raw_message == "猜数字帮助":
            text = "格式————猜数字:阿拉伯数字(1-10之间)"
        elif str(msg.raw_message).split(':')[0] == '猜数字':
            shuzi = random.randrange(1,11)
            if shuzi == int(msg.raw_message.split(':')[-1]):
                text = "恭喜你猜对了"
            else:
                try:
                    await self.api.set_group_ban(msg.group_id,msg.user_id,60)
                except Exception as e:
                    pass
                text = '猜错了，给我寄！！'
        if text:
            return {'try': 'text', "text": text, 'nub': nub}