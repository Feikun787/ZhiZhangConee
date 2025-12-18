import random


class DaWon:
    async def dawon(self,msg,nub):
        text = None
        if msg.raw_message == "打我":#定义触发词
            if nub == 1:
                await self.api.post_group_msg(msg.group_id, at=msg.user_id, text=text)
            else:
                await self.api.post_private_msg(msg.user_id, text=text)
            renping = random.randrange(1,9)#生成随机数
            jinyan = 0
            text = f'你今天的人品是{renping}'
            if nub == 1:
                await self.api.post_group_msg(msg.group_id, at=msg.user_id, text=text)
            else:
                await self.api.post_private_msg(msg.user_id, text=text)
            for i in range(renping):#循环打人
                jinyan += 60
                text = f'第{i+1}拳'
                if nub == 1:
                    await self.api.set_group_ban(msg.group_id,msg.user_id,jinyan)
                    if nub == 1:
                        await self.api.post_group_msg(msg.group_id, at=msg.user_id, text=text)
                    else:
                        await self.api.post_private_msg(msg.user_id, text=text)
            text = '够了吗？'
        if text:
            return {'try': 'text', "text": text, 'nub': nub}