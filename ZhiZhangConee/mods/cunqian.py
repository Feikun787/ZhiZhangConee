from plugins.ZhiZhangConee.universl.io_json import json_file

class Cunqian:
    async def cunqian(self, msg, nub):
        text = None
        if msg.raw_message == "存钱帮助":
            text = """存钱格式————存钱:金额
    添加目标格式————:存钱目标:金额
    修改目标格式————新的目标:金额
    取钱格式————取钱:金额"""
        if str(msg.raw_message).split(':')[0] == "存钱":
            data = json_file.get_json('plugins/ZhiZhangConee/data/cunqian.json')
            try:
                data[str(msg.user_id)][0] += float(msg.raw_message.split(':')[-1])
                json_file.set_json(data, 'plugins/ZhiZhangConee/data/cunqian.json')
                try:
                    text = (f"已经存入{float(msg.raw_message.split(':')[-1])}金额"
                            f"当前存款:{data[str(msg.user_id)][0]}"
                            f"当前目标:{data[str(msg.user_id)][1]}"
                            f"当前进度:{(float(data[str(msg.user_id)][0]) / float(data[str(msg.user_id)][-1])) * 100}%")
                except Exception as e:
                    text = (f"已经存入{float(msg.raw_message.split(':')[-1])}金额"
                            f"当前存款:{data[str(msg.user_id)][0]}"
                            f"当前目标:{data[str(msg.user_id)][1]}"
                            f"当前进度:{0}%")

            except:
                text = "存入错误，输入错误或者没有定目标"
        elif str(msg.raw_message).split(':')[0] == "取钱":
            data = json_file.get_json('plugins/ZhiZhangConee/data/cunqian.json')
            try:
                data[str(msg.user_id)][0] -= float(msg.raw_message.split(':')[-1])
                json_file.set_json(data, 'plugins/ZhiZhangConee/data/cunqian.json')
                try:
                    text = (f"已经存入{float(msg.raw_message.split(':')[-1])}金额"
                            f"当前存款:{data[str(msg.user_id)][0]}"
                            f"当前目标:{data[str(msg.user_id)][1]}"
                            f"当前进度:{(float(data[str(msg.user_id)][0]) / float(data[str(msg.user_id)][-1])) * 100}%")
                except Exception as e:
                    text = (f"已经存入{float(msg.raw_message.split(':')[-1])}金额"
                            f"当前存款:{data[str(msg.user_id)][0]}"
                            f"当前目标:{data[str(msg.user_id)][1]}"
                            f"当前进度:{0}%")
            except:
                text = "错误，输入错误或者没有定目标"
        elif str(msg.raw_message).split(':')[0] == "存钱目标":
            data = json_file.get_json('plugins/ZhiZhangConee/data/cunqian.json')
            data[str(msg.user_id)] = [0, float(msg.raw_message.split(':')[-1])]
            json_file.set_json(data, 'plugins/ZhiZhangConee/data/cunqian.json')
            text = "已经创建目标了，和小智障一起加油吧"
        elif str(msg.raw_message).split(':')[0] == "新的目标":
            data = json_file.get_json('plugins/ZhiZhangConee/data/cunqian.json')
            try:
                data[str(msg.user_id)][-1] = float(msg.raw_message.split(':')[-1])
                json_file.set_json(data, 'plugins/ZhiZhangConee/data/cunqian.json')
                try:
                    text = (f"已经存入{float(msg.raw_message.split(':')[-1])}金额"
                            f"当前存款:{data[str(msg.user_id)][0]}"
                            f"当前目标:{data[str(msg.user_id)][1]}"
                            f"当前进度:{(float(data[str(msg.user_id)][0]) / float(data[str(msg.user_id)][-1])) * 100}%")
                except Exception as e:
                    text = (f"已经存入{float(msg.raw_message.split(':')[-1])}金额"
                            f"当前存款:{data[str(msg.user_id)][0]}"
                            f"当前目标:{data[str(msg.user_id)][1]}"
                            f"当前进度:{0}%")
            except:
                text = '错误，输入错误或者没有定目标'
        if text:
            return {'try': 'text', "text": text, 'nub': nub}