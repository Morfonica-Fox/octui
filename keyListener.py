import readchar
import threading
import sys
from sys import platform

KEYS = readchar.key

class argsPlaceholoders:
    key = 'keyListener.argsPlaceholoders.key'

def argsReplacer(datas, args, kwargs):
    for i in range(len(args)):
        if args[i] == argsPlaceholoders.key:
            args[i] = datas["key"]
    for key, value in kwargs.items():
        if value == argsPlaceholoders.key:
            kwargs[key] = datas["key"]
    return args, kwargs

def execFunc(func, args=[], kwargs={}, datas=None):
    rp_args, rp_kwargs = argsReplacer(datas, args, kwargs)
    return func(*rp_args, **rp_kwargs)

class specialKeys:
    exit_hotkey = b'\x03'

class keyListener:
    __doc__ = '''传入参数:
binders: {key:[func: call, *args: list, **kwargs: dict], ...} func可以为lambda表达式
else_binder: (key, func, *args, **kwargs) 按下不在binders中的按键时调用的函数 默认为None
finally_binder: (func, *args, **kwargs) 按下任何按键后调用的函数 默认为None
enabled: bool 是否启用 默认为True
use_msvcrt: bool 是否使用msvcrt模块(如果平台为windows) 默认为False
use_termios: bool 是否使用termios模块(如果平台为linux) 默认为False'''
    def __init__(self, binders={}, else_binder=(), finally_binder=(), enabled=True, use_msvcrt=False, use_termios=False):
        if not (platform in ("win32", "cygwin")) and not platform.startswith(("linux", "darwin", "freebsd", "openbsd")):
            raise NotImplementedError('Unsupported platform | 不支持的平台')
        self.binders = binders
        self._enabled = enabled
        self.use_msvcrt = platform.startswith(("linux", "darwin", "freebsd", "openbsd")) and use_msvcrt
        self.use_termios = platform in ("win32", "cygwin") and use_termios
        self.else_binder = else_binder
        self.finally_binder = finally_binder
    
    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if value and not self._enabled:
            self.detect_thread = threading.Thread(target=self.detect_key_press, name='keyListenerThread', daemon=True)
            self.detect_thread.start()
        self._enabled = value

    def add_binder(self, key, func, args=[], kwargs={}):
        self.binders[key] = [func, args, kwargs]
    def remove_binder(self, key):
        if key in self.binders.keys():
            del self.binders[key]
            return True
    def get_binders(self):
        return self.binders
    def get_binder(self, key):
        if key in self.binders.keys():
            return self.binders[key]
    def set_else_binder(self, func, args, kwargs):
        self.else_binder = (func, args, kwargs)
    def set_finally_binder(self, func, args, kwargs):
        self.finally_binder = (func, args, kwargs)
    def reset_else_binder(self):
        self.else_binder = ()
    def reset_finally_binder(self):
        self.finally_binder = ()
    def trigged_detect(self):
        if self.use_msvcrt and not self.use_termios:
            import msvcrt
            key = msvcrt.getch()
        elif self.use_termios:
            import termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            term = termios.tcgetattr(fd)
            try:
                term[3] &= ~(termios.ICANON | termios.ECHO | termios.IGNBRK | termios.BRKINT)
                termios.tcsetattr(fd, termios.TCSAFLUSH, term)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        else:
            try:
                key = readchar.readkey().encode('utf-8')
            except:
                key = specialKeys.exit_hotkey
        if key == b'\xe0' or key == b'\x03' or key == b'\x00' and self.use_msvcrt:
            key = msvcrt.getch()
        if len(self.finally_binder) > 0: # 按下任何按键后调用的函数
            if len(self.finally_binder) > 2:
                kwargs = dict(self.finally_binder[2])
            else:
                kwargs = {}
            if len(self.finally_binder) == 1:
                args = list(self.finally_binder[1])
            else:
                args = []
            execFunc(self.finally_binder[0], args, kwargs, {"key": key})
        if key in self.binders.keys(): # 按下在binders中的按键时调用的函数
            data = self.binders[key]
            if len(data) > 2:
                kwargs = dict(data[2])
            else:
                kwargs = {}
            if len(data) > 1:
                args = list(data[1])
            else:
                args = []
            execFunc(data[0], args, kwargs, {"key": key})
        if len(self.else_binder) == 1 or len(self.else_binder) == 2: # 按下不在binders中的按键时调用的函数
            if key == self.else_binder[0] and key not in self.binders.keys():
                if len(self.else_binder) > 1:
                    kwargs = dict(self.else_binder[2])
                else:
                    kwargs = {}
                if len(self.else_binder) == 1:
                    args = list(self.else_binder[1])
                else:
                    args = []
                execFunc(self.else_binder[0], args, kwargs, {"key": key})
    def detect_key_press(self):
        while True:
            if self._enabled:
                self.trigged_detect()


if __name__ == '__main__': # 测试代码
    kl = keyListener(finally_binder=(lambda key:print(key), [], {"key": argsPlaceholoders.key}))
