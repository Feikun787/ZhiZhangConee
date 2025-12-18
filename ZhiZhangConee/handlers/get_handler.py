import json
import importlib
import os


class Handler:
    def __init__(self, msg, nub, api):
        self.msg = msg
        self.nub = nub
        self.api = api

        # 从 JSON 文件加载模块配置
        try:
            config_path = r'plugins/ZhiZhangConee/handlers/ modules_config.json'  # 或使用绝对路径
            with open(config_path, 'r', encoding='utf-8') as f:
                self.modules_config = json.load(f)
        except FileNotFoundError:
            print(f"配置文件未找到")
        except json.JSONDecodeError as e:
            print(f"JSON格式错误: {e}")
        except Exception as e:
            print(f"加载配置文件时发生错误: {e}")

    async def main(self):
        if not self.msg.raw_message:
            self.msg.raw_message = ""

        for config in self.modules_config:
            try:
                module_path = config['module']
                method_name = config['method']
                needs_api = config['needs_api']
                special_init = config['special_init']

                # 动态导入模块和类
                module_name, class_name = module_path.rsplit('.', 1)
                module = importlib.import_module(module_name)
                module_class = getattr(module, class_name)

                # 特殊处理
                if special_init:
                    module_instance = module_class(self)
                else:
                    module_instance = module_class()

                # 设置 api（如果需要）
                if needs_api:
                    module_instance.api = self.api

                # 调用方法
                result = await getattr(module_instance, method_name)(self.msg, self.nub)
                if result:
                    return result
            except Exception as e:
                print(f"模块 {config['module']} 执行出错: {e}")
                continue

        return None
