import subprocess
from plugins.ZhiZhangConee.universl.permission import Permission
import re

from plugins.ZhiZhangConee.mods.PythonSandbox import PythonSandbox

class Idea:
    async def main(self,msg,nub):
        text = None
        if msg.raw_message == '运行帮助':
            text = '#python:换行加代码'
        if str(msg.raw_message).split(':')[0] == '#python':
            if Permission.quanxian(msg.user_id) == 0:

                    #text = "该功能正在维护,可怜的作者正在加班修bug……"
                    #text = '考虑安全问题，该功能已经被作者禁用，敬请期待其他功能！'
                    #return {'try': 'text', "text": text, 'nub': nub}
                text,b = self.idea(msg)
                if b:
                    text = str(b)
                else:
                    pass
            if text:
                return {'try': 'text', "text": text, 'nub': nub}
            return {'try': 'text', "text": '权限不够', 'nub': nub}


    def idea(self,msg):
        sdx = PythonSandbox(timeout=15, memory_limit=50)
        output_file = 'plugins/ZhiZhangConee/mods/example.py'  # 生成的Python文件

        chinese_code = msg.raw_message

        chinese_code = self.fix_code_encoding_efficient(chinese_code)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chinese_code)

        print(f"翻译完成，生成的Python文件为 {output_file}")

        # 运行生成的Python文件
        print(chinese_code)
        try:
            return sdx.execute_code(chinese_code)
        except Exception as e:
            print(f"运行时出错: {e}")
            return str(e),None

    import re

    def fix_code_encoding_efficient(self, code_text):
        """
        增强版：修复编码并检测危险代码
        """
        # 先修复编码，以便准确检测
        replacement_map = {
            '&#91;': '[', '&#93;': ']', '&lt;': '<', '&gt;': '>',
            '&#60;': '<', '&#62;': '>',  # 额外的数字编码
            '&amp;': '&', '&quot;': '"', '&#39;': "'", '&#34;': '"',
            '&#40;': '(', '&#41;': ')', '&#123;': '{', '&#125;': '}',
            '&#96;': '`', '&#126;': '~'
        }

        pattern = re.compile('|'.join(re.escape(key) for key in replacement_map.keys()))
        fixed_code = pattern.sub(lambda m: replacement_map[m.group(0)], code_text)

        # 检测危险代码
        if self.is_code_dangerous(fixed_code):
            return "print('代码包含危险内容，已阻止执行请勿使用os、subprocess等系统模块')"

        return fixed_code

    def is_code_dangerous(self, code_text):
        """
        严格检测危险代码模式
        """
        # 移除注释和字符串，避免误检测
        cleaned_code = self.remove_comments_and_strings(code_text)

        # 危险模式检测
        danger_patterns = [
            # 模块导入
            r'^\s*import\s+(os|subprocess|sys|shutil|ctypes|__import__)\s*$',
            r'^\s*from\s+(os|subprocess|sys|shutil|ctypes|__import__)\s+import',

            # 危险函数调用
            r'\b(os|subprocess|__import__).*?',
            r'\b(os|subprocess|__import__)\.\w*\s*\(',
            r'\b(eval|exec|execfile|compile|__import__)\s*\(',
            r'\b(open|file|input|raw_input|__import__)\s*\(',
            r'\b(system|popen|call|run|spawn|__import__)\s*\(',

            # 文件系统操作
            r'\b(remove|unlink|rmdir|removedirs|rename|replace)\s*\(',
            r'\b(mkdir|makedirs|chdir|listdir|walk)\s*\(',

            # 进程操作
            r'\b(kill|terminate|wait|communicate)\s*\(',

            # 网络相关（可选）
            r'\b(socket|urllib|requests|httplib)\.',

            # 反射相关
            r'\b(getattr|setattr|delattr|hasattr)\s*\(',
            r'\b(globals|locals|vars)\s*\(',
        ]

        for pattern in danger_patterns:
            if re.search(pattern, cleaned_code, re.IGNORECASE | re.MULTILINE):
                return True

        return False

    def remove_comments_and_strings(self, code_text):
        """
        移除注释和字符串内容，避免误检测
        """
        # 移除单行注释
        code_no_comments = re.sub(r'#.*$', '', code_text, flags=re.MULTILINE)

        # 移除多行字符串（简单版本）
        code_no_strings = re.sub(r'(""".*?"""|\'\'\'.*?\'\'\')', '', code_no_comments, flags=re.DOTALL)
        code_no_strings = re.sub(r'(".*?"|\'.*?\')', '', code_no_strings)

        return code_no_strings
