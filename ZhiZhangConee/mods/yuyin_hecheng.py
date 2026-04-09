import os
import requests
from datetime import datetime


class YuyinHecheng:
    async def main(self, msg, nub):
        text = None

        if msg.raw_message == "语音帮助2":
            text = """语音合成使用说明：
发送"语音合成:要合成的内容"即可生成语音
例如：语音合成:你好世界"""
            return {'try': 'text', "text": text, 'nub': nub}

        if str(msg.raw_message).startswith("语音合成:"):
            content = msg.raw_message.split(":", 1)[1].strip()

            if not content:
                text = "请输入要合成的内容"
                return {'try': 'text', "text": text, 'nub': nub}

            if len(content) > 200:
                text = "合成内容不能超过200字"
                return {'try': 'text', "text": text, 'nub': nub}

            try:
                filename = "plugins/ZhiZhangConee/mods/logs/tts_output.mp3"

                os.makedirs(os.path.dirname(filename), exist_ok=True)

                tts_url = f"https://fanyi.baidu.com/gettts?lan=zh&text={requests.utils.quote(content)}&spd=5&source=web"

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }

                response = requests.get(tts_url, headers=headers, timeout=10)

                if response.status_code == 200 and len(response.content) > 100:
                    with open(filename, 'wb') as f:
                        f.write(response.content)

                    text = "语音合成成功！"
                    return {'try': 'record', "text": '/plugins/ZhiZhangConee/mods/logs/tts_output.mp3', 'nub': nub}
                else:
                    text = "语音合成失败，请稍后重试"
                    return {'try': 'text', "text": text, 'nub': nub}

            except Exception as e:
                text = f"语音合成出错：{str(e)}"
                return {'try': 'text', "text": text, 'nub': nub}

        return None
