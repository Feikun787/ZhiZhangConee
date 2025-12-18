import random


class RockPs():
    async def rock_ps(self, msg, nub):
        if msg.raw_message == "猜拳帮助":
            text = "格式————智障猜拳:石头？剪刀？布"
            return {'try': 'text', "text": text, 'nub': nub}
        if str(msg.raw_message).split(':')[0] == "智障猜拳":
            a = str(msg.raw_message).split(':')
            """1石头   2剪刀   3布"""
            xuanze = 0
            pin = '哎嘿，平局？'
            shu = '啊！我输了'
            yin = "哈哈！我赢了！"
            my_xuanze = random.randrange(1, 4)
            if len(a) == 2:
                if a[-1] == "石头":
                    xuanze = 1
                    if my_xuanze == 1:
                        text = pin
                    elif my_xuanze == 2:
                        text = shu
                    else:
                        text = yin
                elif a[-1] == '剪刀':
                    xuanze = 2
                    if my_xuanze == 1:
                        text = yin
                    elif my_xuanze == 2:
                        text = pin
                    else:
                        text = shu
                elif a[-1] == '布':
                    xuanze = 3
                    if my_xuanze == 1:
                        text = yin
                    elif my_xuanze == 2:
                        text = shu
                    else:
                        text = pin
                else:
                    text = f"猜拳里面没有{a[-1]}哦"
            if text == yin and nub == 1:
                await self.api.set_group_ban(msg.group_id, msg.user_id, 60)
                text = '你输了，给我寄！！'
            return {'try': 'text', "text": text, 'nub': nub}