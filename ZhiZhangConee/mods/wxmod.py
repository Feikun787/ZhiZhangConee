from plugins.ZhiZhangConee.mods import wxbz


class WxMod():
    async def main(self,msg,nub):
        if str(msg.raw_message) == "八字帮助":
            return {'try': 'text', 'text':"八字查询:生日（2000.1.1.1）", 'nub': nub}
        if str(msg.raw_message).split(":")[0] == "八字查询":
            return {'try': 'text', 'text':wxbz.main2(str(msg.raw_message).split(":")[1]), 'nub': nub}
        return None
