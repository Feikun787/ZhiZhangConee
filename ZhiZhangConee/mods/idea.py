import subprocess
from plugins.ZhiZhangConee.universl.permission import Permission
import re

from plugins.ZhiZhangConee.mods.PythonSandbox import PythonSandbox


class Idea:
    async def main(self, msg, nub):
        text = None
        if msg.raw_message == '运行帮助':
            text = '#python:换行加代码'
        if str(msg.raw_message).split(':')[0] == '#python':
            if Permission.quanxian(msg.user_id) == 0 or Permission.quanxian(msg.user_id) == 1:

                # text = "该功能正在维护,可怜的作者正在加班修bug……"
                # text = '考虑安全问题，该功能已经被作者禁用，敬请期待其他功能！'
                # return {'try': 'text', "text": text, 'nub': nub}
                text, b = self.idea(msg)
                if b:
                    text = str(b)
                else:
                    pass
            if text:
                return {'try': 'text', "text": text, 'nub': nub}
            return {'try': 'text', "text": '权限不够', 'nub': nub}

    def idea(self, msg):
        sdx = PythonSandbox(timeout=15, memory_limit=50)
        output_file = 'plugins/ZhiZhangConee/mods/example.py'  # 生成的Python文件

        chinese_code = msg.raw_message

        chinese_code, inputs = self.extract_inputs(chinese_code)

        chinese_code = self.fix_code_encoding_efficient(chinese_code)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chinese_code)

        print(f"翻译完成，生成的Python文件为 {output_file}")

        print(chinese_code)
        try:
            if inputs:
                return sdx.execute_code_with_inputs(chinese_code, inputs)
            else:
                return sdx.execute_code(chinese_code)
        except Exception as e:
            print(f"运行时出错: {e}")
            return str(e), None

    def extract_inputs(self, code_text):
        """
        从代码末尾提取输入内容
        格式: 检查输入:内容1，内容2，内容3
        返回: (清理后的代码, 输入列表)
        """
        inputs = []

        pattern = r'\n?检查输入:(.+)$'
        match = re.search(pattern, code_text, re.DOTALL)

        if match:
            input_str = match.group(1).strip()
            code_without_inputs = code_text[:match.start()]

            parts = re.split(r'[，,]', input_str)
            inputs = [part.strip() for part in parts if part.strip()]

            return code_without_inputs, inputs

        return code_text, []

    import re

    def fix_code_encoding_efficient(self, code_text):
        """
        增强版：修复编码并检测危险代码
        """
        replacement_map = {
            '&#91;': '[', '&#93;': ']', '&lt;': '<', '&gt;': '>',
            '&#60;': '<', '&#62;': '>',  # 额外的数字编码
            '&amp;': '&', '&quot;': '"', '&#39;': "'", '&#34;': '"',
            '&#40;': '(', '&#41;': ')', '&#123;': '{', '&#125;': '}',
            '&#96;': '`', '&#126;': '~'
        }

        pattern = re.compile('|'.join(re.escape(key) for key in replacement_map.keys()))
        fixed_code = pattern.sub(lambda m: replacement_map[m.group(0)], code_text)

        if self.is_code_dangerous(fixed_code):
            return "print('代码包含危险内容，已阻止执行请勿使用os、subprocess等系统模块')"

        return fixed_code

    def is_code_dangerous(self, code_text):
        """
        严格检测危险代码模式
        """
        cleaned_code = self.remove_comments_and_strings(code_text)

        danger_patterns = [
            r'^\s*import\s+(os|subprocess|sys|shutil|ctypes|__import__)\s*$',
            r'^\s*from\s+(os|subprocess|sys|shutil|ctypes|__import__)\s+import',

            r'\b(os|subprocess|__import__).*?',
            r'\b(os|subprocess|__import__)\.\w*\s*\(',
            r'\b(eval|exec|execfile|compile|__import__)\s*\(',
            r'\b(open|file|__import__)\s*\(',
            r'\b(system|popen|call|run|spawn|__import__)\s*\(',

            r'\b(remove|unlink|rmdir|removedirs|rename|replace)\s*\(',
            r'\b(mkdir|makedirs|chdir|listdir|walk)\s*\(',

            r'\b(kill|terminate|wait|communicate)\s*\(',

            r'\b(socket|urllib|requests|httplib)\.',

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
        code_no_comments = re.sub(r'#.*$', '', code_text, flags=re.MULTILINE)

        code_no_strings = re.sub(r'(""".*?"""|\'\'\'.*?\'\'\')', '', code_no_comments, flags=re.DOTALL)
        code_no_strings = re.sub(r'(".*?"|\'.*?\')', '', code_no_strings)

        return code_no_strings
