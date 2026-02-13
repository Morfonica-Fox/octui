import ctypes
import queueing
import threading

# 定义Windows控制台API常量喵
STD_INPUT_HANDLE = -10
ENABLE_MOUSE_INPUT = 0x0010
ENABLE_QUICK_EDIT_MODE = 0x0040
ENABLE_EXTENDED_FLAGS = 0x0080

# 定义鼠标事件类型喵
MOUSE_EVENT = 0x0002
MOUSE_MOVED = 0x0001          # 移动事件
MOUSE_WHEELED = 0x0004        # 滚轮事件
MOUSE_HWHEELED = 0x0008       # 水平滚轮事件

# 定义鼠标按钮状态常量喵
FROM_LEFT_1ST_BUTTON_PRESSED = 0x0001  # 左键
RIGHTMOST_BUTTON_PRESSED = 0x0002     # 右键
FROM_LEFT_2ND_BUTTON_PRESSED = 0x0004 # 中键
FROM_LEFT_3RD_BUTTON_PRESSED = 0x0008 # 第四个按钮
FROM_LEFT_4TH_BUTTON_PRESSED = 0x0010 # 第五个按钮

# 定义控制台坐标结构喵
class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

# 定义鼠标事件记录结构喵
class MOUSE_EVENT_RECORD(ctypes.Structure):
    _fields_ = [
        ("dwMousePosition", COORD),
        ("dwButtonState", ctypes.c_ulong),    # 按钮状态
        ("dwControlKeyState", ctypes.c_ulong),# 控制键状态
        ("dwEventFlags", ctypes.c_ulong)      # 事件标志
    ]

# 定义输入事件联合体喵
class InputEventUnion(ctypes.Union):
    _fields_ = [
        ("MouseEvent", MOUSE_EVENT_RECORD),
    ]

# 定义输入记录结构喵
class INPUT_RECORD(ctypes.Structure):
    _fields_ = [
        ("EventType", ctypes.c_ushort),
        ("Event", InputEventUnion)
    ]

# 加载kernel32库喵
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

# 定义最主要的类喵
class WindowsMouseTracker:
    def __init__(self, runself=True):
        # 喵喵喵 这应该就不用写注释了吧
        self.running = runself
        self.hstdin = kernel32.GetStdHandle(STD_INPUT_HANDLE)
        self.queue = queueing.Queue()
        self.enable_mouse_input()
    
    def __del__(self):
        # 析构函数喵
        self.uninstall()
    
    def stop(self):
        # 停止运行喵
        self.running = False
        self.thread.join()
    
    def uninstall(self):
        # 卸载喵
        self.disable_mouse_input()
        self.running = False
        self.thread.join()
    
    def install(self):
        # 安装喵
        self.enable_mouse_input()

    def enable_mouse_input(self):
        # 保存当前控制台模式以备还原喵
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(self.hstdin, ctypes.byref(mode))
        
        # 配置控制台模式以接收所有鼠标事件喵
        new_mode = mode.value | ENABLE_MOUSE_INPUT | ENABLE_EXTENDED_FLAGS
        new_mode &= ~ENABLE_QUICK_EDIT_MODE  # 禁用快速编辑模式喵(反Windows Terminal系控制台用的)
        kernel32.SetConsoleMode(self.hstdin, new_mode)

    def disable_mouse_input(self):
        # 还原控制台模式喵
        kernel32.SetConsoleMode(self.hstdin, ENABLE_EXTENDED_FLAGS | ENABLE_QUICK_EDIT_MODE)

    def set_cursor_position(self, x, y):
        # 设置光标位置喵(其实也可以用ansi来着)
        coord = COORD(x, y)
        kernel32.SetConsoleCursorPosition(kernel32.GetStdHandle(-11), coord)

    def get_button_state(self, state):
        # 解析鼠标按钮状态喵
        return [state & FROM_LEFT_1ST_BUTTON_PRESSED != 0, 
                state & RIGHTMOST_BUTTON_PRESSED != 0, 
                state & FROM_LEFT_2ND_BUTTON_PRESSED != 0, 
                state & FROM_LEFT_3RD_BUTTON_PRESSED != 0, 
                state & FROM_LEFT_4TH_BUTTON_PRESSED != 0]

    def get_control_keys(self, state):
        # 解析控制键状态喵
        return [state & 0x01 != 0, 
                state & 0x02 != 0, 
                state & 0x04 != 0, 
                state & 0x08 != 0, 
                state & 0x10 != 0]

    def parse_mouse_event(self, event):
        # 解析鼠标事件记录喵
        x = event.dwMousePosition.X
        y = event.dwMousePosition.Y
        
        delta = 0
        hdelta = 0
        
        # 确定事件类型
        if event.dwEventFlags == MOUSE_WHEELED:
            # 提取滚轮值（高16位）
            wheel_data = (event.dwButtonState >> 16)
            delta = wheel_data if wheel_data < 32768 else wheel_data - 65536
        elif event.dwEventFlags == MOUSE_HWHEELED:
            # 提取水平滚轮值（高16位）
            wheel_data = (event.dwButtonState >> 16)
        
        return {
            "x": x,
            "y": y,
            "buttons": self.get_button_state(event.dwButtonState),
            "control_keys": self.get_control_keys(event.dwControlKeyState),
            "delta": delta,
            "hdelta": hdelta
        }

    def read_events(self):
        # 读取鼠标事件喵
        buf_size = ctypes.c_ulong(1)
        read = ctypes.c_ulong(0)
        event = INPUT_RECORD()
        
        kernel32.ReadConsoleInputW(
            self.hstdin,
            ctypes.byref(event),
            buf_size,
            ctypes.byref(read)
        )
        
        if read.value > 0 and event.EventType == 0x0002:  # 鼠标事件
            return self.parse_mouse_event(event.Event.MouseEvent)
        return None
    
    def run_loop(self):
        # 运行循环喵
        while self.running:
            try:
                event = self.read_events()
                if event:
                    self.queue.enqueue(event)
            except:
                pass
    
    def run(self):
        # 单独启动线程进行循环喵
        self.thread = threading.Thread(target=self.run_loop)
        self.thread.start()
    
    def get_event(self, default=None, blocking: bool = False):
        # 获取下一个事件喵
        while True:
            event = self.queue.dequeue()
            if event:
                return event
            elif not self.running or not blocking:
                return default

if __name__ == "__main__": # 测试代码
    import os
    import sys
    os.system("cls")
    tracker = WindowsMouseTracker()
    tracker.run()
    try:
        while True:
            print(tracker.get_event(blocking=True))
    finally:
        tracker.stop()
        tracker.uninstall()
        sys.exit()
