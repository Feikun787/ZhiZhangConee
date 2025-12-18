import ast
import builtins
import gc
import ast
import builtins
import gc
import re as r
import threading
import time
import types
from types import FunctionType
from threading import Thread, Event
import sys

from requests import request
#铰

class PythonSandbox:
    def __init__(self, timeout=10, memory_limit=100):
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.safe_builtins = self.create_safe_builtins()

    def should_sanitize_submodule(self, submodule_name):
        """判断是否应该清理子模块"""
        dangerous_modules = {'os', 'sys', 'subprocess', 'ctypes', 'shutil', 'socket'}

        if any(dangerous in submodule_name for dangerous in dangerous_modules):
            return True

        # 限制模块嵌套深度
        if submodule_name.count('.') > 5:
            return False

        return True

    def sanitize_module(self, module, module_name):
        """清理模块中的危险属性"""
        dangerous_patterns = [
            'os', 'sys', 'subprocess', 'ctypes', 'shutil', 'socket',
            'eval', 'exec', 'input', 'file', '__builtins__',
            '__import__', 'globals', 'locals', '_name_', '_getattribute_'
        ]

        cleaned_count = 0
        all_attrs = list(dir(module))

        for attr_name in all_attrs:
            # 特别处理 __import__ 属性
            if attr_name == '__import__':
                try:
                    delattr(module, attr_name)
                    cleaned_count += 1
                    continue
                except (AttributeError, TypeError):
                    pass

            if attr_name.startswith('__') and attr_name.endswith('__'):
                continue

            try:
                attr_value = getattr(module, attr_name)

                should_delete = False

                # 检查属性名是否危险
                if any(dangerous in attr_name.lower() for dangerous in dangerous_patterns):
                    should_delete = True
                # 检查模块类型属性
                elif isinstance(attr_value, types.ModuleType):
                    module_name_str = getattr(attr_value, '__name__', '')
                    if any(dangerous in module_name_str for dangerous in dangerous_patterns):
                        should_delete = True
                # 检查可调用对象
                elif callable(attr_value) and hasattr(attr_value, '__name__'):
                    func_name = getattr(attr_value, '__name__', '')
                    if any(dangerous in func_name for dangerous in dangerous_patterns):
                        should_delete = True

                if should_delete:
                    try:
                        delattr(module, attr_name)
                        cleaned_count += 1
                    except (AttributeError, TypeError):
                        pass

            except Exception:
                continue

        return cleaned_count

    def create_safe_builtins(self):
        """创建安全的内置函数集合"""
        allowed_builtins = {
            'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes',
            'callable', 'chr', 'complex', 'dict', 'dir', 'divmod', 'enumerate',
            'filter', 'float', 'format', 'frozenset', 'hash', 'hex', 'id',
            'int', 'iter', 'len', 'list', 'map', 'max', 'min', 'next',
            'object', 'oct', 'ord', 'pow', 'print', 'range', 'repr', 'reversed',
            'round', 'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type',
            'zip', '__import__'
        }

        safe_builtins = {}
        for name in allowed_builtins:
            if hasattr(builtins, name):
                safe_builtins[name] = getattr(builtins, name)

        orig_import = builtins.__import__

        # 添加到 create_safe_builtins 方法中
        def safe_getattr(obj, name, default=None):
            """安全的 getattr，防止访问危险属性"""
            dangerous_attrs = ['__import__', '__loader__', '__spec__', '__file__', '__cached__']
            if name in dangerous_attrs:
                raise AttributeError(f"访问属性 {name} 被禁止")
            return getattr(obj, name, default)

        safe_builtins['getattr'] = safe_getattr

        def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
            allowed_modules = {
                'math', 'random', 'datetime', 'time', 'json', 're',
                'collections', 'itertools', 'functools', 'operator'
            }

            dangerous_modules = {'os', 'sys', 'subprocess', 'ctypes', 'socket'}

            if name in dangerous_modules:
                raise ImportError(f"禁止导入危险模块: {name}")

            if name not in allowed_modules:
                raise ImportError(f"禁止导入模块: {name} (不在白名单中)")

            module = orig_import(name, globals, locals, fromlist, level)

            # 更彻底地清理模块
            #self.sanitize_module(module, name)

            # 额外保护：确保模块没有 __import__ 属性
            if hasattr(module, '__import__'):
                try:
                    delattr(module, '__import__')
                except:
                    pass

            return module

        safe_builtins['__import__'] = safe_import
        return safe_builtins

    def set_memory_limit(self):
        """设置内存限制"""
        try:
            pass
        except:
            pass

    def ast_security_check(self, code):
        """AST语法树安全检查"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return False, "语法错误"

        dangerous_nodes = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    if func_name in ['eval', 'exec', 'open', 'input', '__loader__', 'load_module', '__spec__','__getattribute__']:
                        dangerous_nodes.add(f"危险函数调用: {func_name}")
                # 检查属性链调用，如 a.b.c()
                elif isinstance(node.func, ast.Attribute):
                    attr_chain = []
                    current = node.func
                    while isinstance(current, ast.Attribute):
                        attr_chain.append(current.attr)
                        current = current.value
                    attr_chain.reverse()
                    chain_str = '.'.join(attr_chain)
                    if any(dangerous in chain_str for dangerous in ['__import__', '__loader__']):
                        dangerous_nodes.add(f"危险属性链调用: {chain_str}")

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in ['os', 'sys', 'subprocess', 'ctypes', 'shutil']:
                        dangerous_nodes.add(f"危险模块导入: {alias.name}")

            elif isinstance(node, ast.ImportFrom):
                if node.module and any(dangerous in node.module for dangerous in
                                       ['os', 'sys', 'subprocess', 'ctypes', 'shutil']):
                    dangerous_nodes.add(f"危险模块导入: {node.module}")

        if dangerous_nodes:
            return False, f"安全检查失败: {', '.join(dangerous_nodes)}"

        return True, "安全检查通过"

    def ast_detect_loader(self, code):
        """AST检测加载器模式"""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Attribute):
                    if node.attr in ['__loader__', 'load_module', '__spec__']:
                        parent = getattr(node, 'parent', None)
                        if parent and isinstance(parent, ast.Call):
                            return True

                if (isinstance(node, ast.Subscript) and
                        isinstance(node.value, ast.Attribute) and
                        node.value.attr == '__dict__'):
                    return True

                if isinstance(node, ast.Str):
                    if any(keyword in node.s for keyword in
                           ['__loader__', 'load_module', '__spec__']):
                        return True

        except:
            pass
        return False

    def ast_detect_loader2(self, code):
        """AST语法树检测，更难绕过"""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Attribute):
                    if node.attr in ['__loader__', 'load_module', '__spec__', 'get_data', 'get_code', 'get_source',
                                     '__dict__']:
                        return True
                if isinstance(node, ast.Str):
                    if any(keyword in node.s for keyword in
                           ['__loader__', 'load_module', '__spec__', 'get_data', 'get_code', 'get_source', '__dict__']):
                        return True
        except:
            pass
        return False

    def execute_code(self, code):
        self.a = 0
        """在沙箱中执行代码"""
        if self.ast_detect_loader(code) or self.ast_detect_loader2(code):
            return None, "检测到危险的模块加载模式"
        safe, message = self.ast_security_check(code)
        if not safe:
            return None, message

        local_vars = {}
        global_vars = {'__builtins__': self.safe_builtins}

        result = [None]
        error = [None]
        timeout_event = Event()

        def run_code():
            try:
                self.set_memory_limit()
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = captured_stdout = StringIO()
                sys.stderr = captured_stderr = StringIO()

                try:
                    exec(code, global_vars, local_vars)
                    output = captured_stdout.getvalue()
                    errors = captured_stderr.getvalue()

                    if errors:
                        result[0] = f"执行完成，但有警告:\n{output}\n---\n{errors}" if output else f"执行警告:\n{errors}"
                    else:
                        result[0] = output or "代码执行完成（无输出）"

                finally:
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr

            except Exception as e:
                error[0] = f"执行错误: {str(e)}"
            finally:
                timeout_event.set()

        thread = Thread(target=run_code)
        thread.daemon = True
        thread.start()

        thread.join(self.timeout)

        if thread.is_alive():
            timeout_event.set()
            return None, f"执行超时（超过{self.timeout}秒）"

        if error[0]:
            return None, error[0]

        return result[0], None


class SecurePythonSandbox2(PythonSandbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loader_blacklist = {'os', 'sys', 'subprocess', 'ctypes'}

    def detect_loader_pattern(self, code):
        """检测加载器绕过模式"""
        patterns = [
            r'__loader__', r'load_module', r'__spec__',
            r'\.get_data', r'\.get_code', r'\.get_source'
        ]
        return any(r.search(pattern, code) for pattern in patterns)


class StringIO:
    def __init__(self):
        self.content = []

    def write(self, text):
        self.content.append(str(text))

    def getvalue(self):
        return ''.join(self.content)

    def flush(self):
        pass
