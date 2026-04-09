import os
from plugins.ZhiZhangConee.universl.permission import Permission


class Jietu:
    async def main(self, msg, nub):
        text = None

        if msg.raw_message == "截图帮助":
            text = """截图功能说明：
发送"截图"命令可以进行屏幕截图
需要管理员权限
注意：锁屏状态下可能无法正常截图"""
            return {'try': 'text', "text": text, 'nub': nub}

        if msg.raw_message == "截图":
            if Permission.quanxian(msg.user_id) == 0 or Permission.quanxian(msg.user_id) == 1:
                try:
                    from PIL import ImageGrab
                    import ctypes
                    import time

                    filename = "plugins/ZhiZhangConee/mods/logs/screenshot.png"

                    os.makedirs(os.path.dirname(filename), exist_ok=True)

                    user32 = ctypes.windll.user32
                    kernel32 = ctypes.windll.kernel32

                    is_locked = user32.GetForegroundWindow() == 0

                    if is_locked:
                        text = "检测到系统已锁屏，无法进行截图\n请先解锁屏幕后再试"
                        return {'try': 'text', "text": text, 'nub': nub}

                    time.sleep(0.1)

                    screenshot = ImageGrab.grab(all_screens=False)

                    if screenshot.getbbox() is None or screenshot.getcolors(1):
                        text = "截图失败：屏幕内容为空，可能处于锁屏或休眠状态"
                        return {'try': 'text', "text": text, 'nub': nub}

                    screenshot.save(filename)

                    text = f"截图成功！"

                    return {'try': 'image', "text": filename, 'nub': nub}
                except ImportError:
                    text = "缺少PIL库，请安装：pip install Pillow"
                    return {'try': 'text', "text": text, 'nub': nub}
                except Exception as e:
                    text = f"截图失败：{str(e)}"
                    return {'try': 'text', "text": text, 'nub': nub}
            else:
                text = "权限不足，需要管理员权限才能使用截图功能"
                return {'try': 'text', "text": text, 'nub': nub}

        return None
