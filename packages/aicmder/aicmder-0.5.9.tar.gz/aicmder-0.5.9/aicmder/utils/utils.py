import types
import packaging.version
import sys
import os
import importlib


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Version(packaging.version.Version):
    '''Extended implementation of packaging.version.Version'''

    def match(self, condition: str) -> bool:
        '''
        Determine whether the given condition are met
        Args:
            condition(str) : conditions for judgment
        Returns:
            bool: True if the given version condition are met, else False
        Examples:
            .. code-block:: python
                Version('1.2.0').match('>=1.2.0a')
        '''
        if not condition:
            return True
        if condition.startswith('>='):
            version = condition[2:]
            _comp = self.__ge__
        elif condition.startswith('>'):
            version = condition[1:]
            _comp = self.__gt__
        elif condition.startswith('<='):
            version = condition[2:]
            _comp = self.__le__
        elif condition.startswith('<'):
            version = condition[1:]
            _comp = self.__lt__
        elif condition.startswith('=='):
            version = condition[2:]
            _comp = self.__eq__
        elif condition.startswith('='):
            version = condition[1:]
            _comp = self.__eq__
        else:
            version = condition
            _comp = self.__eq__

        return _comp(Version(version))

    def __lt__(self, other):
        if isinstance(other, str):
            other = Version(other)
        return super().__lt__(other)

    def __le__(self, other):
        if isinstance(other, str):
            other = Version(other)
        return super().__le__(other)

    def __gt__(self, other):
        if isinstance(other, str):
            other = Version(other)
        return super().__gt__(other)

    def __ge__(self, other):
        if isinstance(other, str):
            other = Version(other)
        return super().__ge__(other)

    def __eq__(self, other):
        if isinstance(other, str):
            other = Version(other)
        return super().__eq__(other)


def load_py_dir(python_dir: str):
    model_basename = os.path.basename(python_dir)
    spec = importlib.util.spec_from_file_location(
        model_basename, os.path.join(python_dir, '__init__.py'))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_py_module(python_path: str, py_module_name: str) -> types.ModuleType:
    '''
    Load the specified python module.

    Args:
        python_path(str) : The directory where the python module is located
        py_module_name(str) : Module name to be loaded
    '''
    sys.path.insert(0, python_path)

    # Delete the cache module to avoid hazards. For example, when the user reinstalls a HubModule,
    # if the cache is not cleared, then what the user gets at this time is actually the HubModule
    # before uninstallation, this can cause some strange problems, e.g, fail to load model parameters.
    if py_module_name in sys.modules:
        sys.modules.pop(py_module_name)

    py_module = importlib.import_module(py_module_name)
    sys.path.pop(0)

    return py_module


# 导入hashlib和threading模块
import hashlib
import threading

# 定义一个FileMonitor类
class FileMonitor:
    # 构造函数，初始化属性
    def __init__(self, filename, callback=[]):
        # 要检测的文件名
        self.filename = filename
        # 文件的初始哈希值
        self.hash_value = self.get_hash(filename)
        # 文件被修改时要调用的函数
        self.callback = callback

    def appendCB(self, cb):
        self.callback.append(cb)

    # 计算文件的哈希值
    def get_hash(self, filename):
        # 打开文件，以二进制模式读取
        with open(filename, "rb") as f:
            # 创建一个md5对象
            md5 = hashlib.md5()
            # 循环读取文件内容，更新md5对象
            while True:
                data = f.read(1024)
                if not data:
                    break
                md5.update(data)
            # 返回文件的哈希值
            return md5.hexdigest()

    # 检测文件的哈希值，并在文件被修改时调用callback函数
    def check_file(self):
        # 循环检测文件的哈希值
        while True:
            try:
                # 获取文件的当前哈希值
                new_hash_value = self.get_hash(self.filename)
                # 如果当前哈希值和初始哈希值不同，说明文件被修改了
                if new_hash_value != self.hash_value:
                    # 调用callback函数
                    if self.callback is not None:
                        if isinstance(self.callback, list):
                            for c in self.callback:
                                c(self.filename)
                        else:
                            self.callback(self.filename)
                    # 更新初始哈希值为当前哈希值
                    self.hash_value = new_hash_value
            except:
                pass

    # 创建一个后台线程，执行check_file方法
    def start(self):
        # 创建一个后台线程，传入check_file方法作为目标函数（target）
        t = threading.Thread(target=self.check_file)
        # 设置线程为守护线程（daemon），这样主程序结束时，线程也会自动结束
        t.setDaemon(True)
        # 启动线程
        t.start()


