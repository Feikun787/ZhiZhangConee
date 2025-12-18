
#创建插件类
class AiYuying():
    #特殊初始化
    def __init__(self,s):
        self.s = s
    #方法实现
    async def ai_yuying(self,msg,nub):
        text = None
        if msg.raw_message == "语音帮助":
            text = "语言格式————ai合成语音:文本"
            return {'try': 'text', "text": text, 'nub': nub}
        if str(msg.raw_message).split(":")[0] == "ai合成语音":
            await self.sen_ai_sing(msg,str(msg.raw_message).split(':')[-1])
            return {'try': 'text', "text": '语音合成完毕', 'nub': nub}
    #语音合成逻辑
    async def sen_ai_sing(self,msg,text):
        a = await self.api.get_ai_characters(msg.group_id, 1)
        print(a)
        a = a['data'][0]['characters'][5]['character_id']
        await self.api.get_ai_record(msg.group_id, a, text)