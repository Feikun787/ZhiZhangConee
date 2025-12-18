from plugins.ZhiZhangConee.handlers.get_handler import Handler
from ncatbot.plugin import CompatibleEnrollment
from ncatbot.plugin_system import( NcatBotPlugin,command_registry,
                                   filter_registry)
#from ncatbot.core import GroupMessage
from ncatbot.utils import get_log
from ncatbot.core import (
    GroupMessage,
    PrivateMessage, MessageChain,
    PrivateMessageEvent,GroupMessageEvent
)

_log = get_log()
bot = CompatibleEnrollment
class ZhiZhangConee(NcatBotPlugin):
    name = "ZhiZhangConee" # 插件名
    version = "2.5" # 插件版本


    async def on_load(self):
        self.data = {}
        if "nu" not in self.data:
            try:
                with open("plugins/ZhiZhangConee/help.txt", "r", encoding="utf-8") as f:
                    self.data["count"] = f.read()
            except FileNotFoundError:
                # 如果文件不存在，使用默认帮助文本
                self.data["count"] = """自动回复：更多关键词等你发现
Kepp：请说kepp帮助
天气查询：输入天气帮助
猜拳：请输入猜拳帮助
打我：输入打我
赞我：输入赞我
禁言：禁言帮助
猜数字：猜数字帮助
机器人管理：输入管理帮助
智障模拟存钱：存钱帮助
ai聊天：输入ai聊天帮助
颜色反转：引用图片加图片反转
py代码运行:运行帮助
"""
            self.data['nub'] = 0
        else:
            pass
        print(self.data["count"])
    #进群退群提示
    @bot.notice_event
    async def on_notice(self, msg):
        text = None
        print( msg)
        if msg['post_type'] == "notice":
            if msg['notice_type'] == "group_increase":
                text = f"{msg['user_id']}欢迎加入群聊"
            elif msg['notice_type'] == "group_decrease":
                text = f"{msg['user_id']}退群了"
        if text:
            await self.api.post_group_msg(msg['group_id'], text=text)
    # 私聊回调
    @bot.private_event
    async def oon_private_message(self, event: PrivateMessage):
        # 定义的回调函数
        await self.on_msg(event,0)

    # 群聊回调
    @bot.group_event
    async def oon_group_event(self, event: GroupMessage):
        # 定义的回调函数
        await self.on_msg(event,1)
    async def on_msg(self,msg,nub):
        text = self.data["count"]
        text2 = None
        if msg.raw_message == "智障帮助":
            text2 = {'try':'text','text':text,'nub' : nub}
        a = Handler(msg,nub,self.api)
        datas = await a.main()
        if datas:
            await self.set_print( msg, datas)
        elif text2:
            await self.set_print(msg, text2)
        return

    async def set_print(self, msg, text):
        if text['try'] == 'text':
            if text['nub'] == 1:
                await self.api.post_group_msg(msg.group_id, at=msg.user_id, text=text['text'])
            else:
                await self.api.post_private_msg(msg.user_id, text=text['text'])
        elif text['try'] == 'image':
            if text['nub'] == 1:
                await self.api.post_group_msg(msg.group_id, image=f"{text['text']}")
            else:
                await self.api.post_private_msg(msg.user_id, image=f"{text['text']}")
        elif text['try'] == 'video':
            if text['nub'] == 1:
                await self.api.post_group_file(msg.group_id,video = 'D:\\trss2\\nacbot\\'+text['text'])
            else:
                await self.api.post_private_file(msg.user_id,video = 'D:\\trss2\\nacbot\\'+text['text'])
        elif text['try'] == 'rtf':
            text['text'] = MessageChain(text['text'])
            if text['nub'] == 1:
                await self.api.post_group_msg(msg.group_id, at=msg.user_id, rtf=text['text'])
            else:
                await self.api.post_private_msg(msg.user_id, rtf=text['text'])