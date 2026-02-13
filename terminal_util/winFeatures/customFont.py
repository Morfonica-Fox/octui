import ctypes
from ctypes import wintypes

# Windows API 常量
STD_OUTPUT_HANDLE = -11
FW_DONTCARE = 0
PROOF_QUALITY = 2

# 结构体定义
class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

class CONSOLE_FONT_INFOEX(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("nFont", ctypes.c_ulong),
        ("dwFontSize", COORD),
        ("FontFamily", ctypes.c_uint),
        ("FontWeight", ctypes.c_uint),
        ("FaceName", ctypes.c_wchar * 32)
    ]

class SMALL_RECT(ctypes.Structure):
    _fields_ = [("Left", ctypes.c_short), ("Top", ctypes.c_short),
                ("Right", ctypes.c_short), ("Bottom", ctypes.c_short)]

class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [("dwSize", COORD), ("dwCursorPosition", COORD),
                ("wAttributes", ctypes.c_ushort), ("srWindow", SMALL_RECT),
                ("dwMaximumWindowSize", COORD)]

# 加载 kernel32 库
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

# 函数声明 (吐槽一下: **的微软这写的什么鬼api 我真就fuck了)
GetStdHandle = kernel32.GetStdHandle
GetStdHandle.argtypes = [wintypes.DWORD]
GetStdHandle.restype = wintypes.HANDLE

GetCurrentConsoleFontEx = kernel32.GetCurrentConsoleFontEx
GetCurrentConsoleFontEx.argtypes = [wintypes.HANDLE, wintypes.BOOL, ctypes.POINTER(CONSOLE_FONT_INFOEX)]
GetCurrentConsoleFontEx.restype = wintypes.BOOL

SetCurrentConsoleFontEx = kernel32.SetCurrentConsoleFontEx
SetCurrentConsoleFontEx.argtypes = [wintypes.HANDLE, wintypes.BOOL, ctypes.POINTER(CONSOLE_FONT_INFOEX)]
SetCurrentConsoleFontEx.restype = wintypes.BOOL

GetConsoleScreenBufferInfo = kernel32.GetConsoleScreenBufferInfo
GetConsoleScreenBufferInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(CONSOLE_SCREEN_BUFFER_INFO)]
GetConsoleScreenBufferInfo.restype = wintypes.BOOL

SetConsoleWindowInfo = kernel32.SetConsoleWindowInfo
SetConsoleWindowInfo.argtypes = [wintypes.HANDLE, wintypes.BOOL, ctypes.POINTER(SMALL_RECT)]
SetConsoleWindowInfo.restype = wintypes.BOOL

SetConsoleScreenBufferSize = kernel32.SetConsoleScreenBufferSize
SetConsoleScreenBufferSize.argtypes = [wintypes.HANDLE, COORD]
SetConsoleScreenBufferSize.restype = wintypes.BOOL

class TerminalSettings:
    def __init__(self):
        self.hconsole = GetStdHandle(STD_OUTPUT_HANDLE)
        self.original_font = self._get_current_font()
        self.original_window_size = self._get_current_window_size()

    def _get_current_font(self):
        """获取当前字体设置（用于恢复）"""
        font = CONSOLE_FONT_INFOEX()
        font.cbSize = ctypes.sizeof(font)
        if GetCurrentConsoleFontEx(self.hconsole, False, ctypes.byref(font)):
            return font
        return None

    def _get_current_window_size(self):
        """获取当前窗口大小（用于恢复）"""
        info = CONSOLE_SCREEN_BUFFER_INFO()
        if GetConsoleScreenBufferInfo(self.hconsole, ctypes.byref(info)):
            return (info.srWindow, info.dwSize)
        return None

    def set_font(self, face_name="Consolas", size=16):
        """设置终端字体和字号（size 是字体高度，单位：像素）"""
        if not self.hconsole:
            return False
        
        font = CONSOLE_FONT_INFOEX()
        font.cbSize = ctypes.sizeof(font)
        font.FaceName = face_name
        font.dwFontSize = COORD(size // 2, size)  # 宽高比约 1:2（等宽字体）
        font.FontFamily = 54  # FF_DONTCARE
        font.FontWeight = FW_DONTCARE
        
        return SetCurrentConsoleFontEx(self.hconsole, False, ctypes.byref(font))

    def set_window_size(self, width, height):
        """设置窗口大小（width: 列数，height: 行数）"""
        if not self.hconsole:
            return False
        
        # 设置缓冲区大小（必须大于等于窗口大小）
        buffer_size = COORD(width, height)
        if not SetConsoleScreenBufferSize(self.hconsole, buffer_size):
            return False
        
        # 设置窗口显示区域
        window_rect = SMALL_RECT(0, 0, width - 1, height - 1)
        return SetConsoleWindowInfo(self.hconsole, True, ctypes.byref(window_rect))

    def restore_defaults(self):
        """恢复原始设置"""
        # 恢复字体
        if self.original_font:
            SetCurrentConsoleFontEx(self.hconsole, False, ctypes.byref(self.original_font))
        
        # 恢复窗口大小
        if self.original_window_size:
            window_rect, buffer_size = self.original_window_size
            SetConsoleScreenBufferSize(self.hconsole, buffer_size)
            SetConsoleWindowInfo(self.hconsole, True, ctypes.byref(window_rect))

