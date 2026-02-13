import sys
import os
import msvcrt  # Windows 专属，用于无缓冲读取字符

def enable_mouse_mode():
    """发送ANSI转义序列启用鼠标模式（按钮+移动事件）"""
    # 启用 1002 模式：捕获按下/释放 + 按住移动
    sys.stdout.write("\x1b[?1002h")
    # 可选：启用 1003 模式，捕获所有鼠标移动（无论是否按键）
    # sys.stdout.write("\x1b[?1003h")
    sys.stdout.flush()

def disable_mouse_mode():
    """关闭鼠标模式，恢复终端默认状态"""
    sys.stdout.write("\x1b[?1002l")
    # 对应关闭 1003 模式
    # sys.stdout.write("\x1b[?1003l")
    sys.stdout.flush()

def parse_mouse_event(data):
    """解析XTerm鼠标协议事件数据"""
    if len(data) < 6 or data[0] != "\x1b" or data[1] != "[":
        return None
    
    # XTerm 鼠标事件格式：ESC [ M <b> <x+32> <y+32>
    # b = 按键状态，x/y = 坐标（均偏移32，解析时需减回）
    b = ord(data[3]) - 32
    x = ord(data[4]) - 32
    y = ord(data[5]) - 32

    button = "未知"
    if b & 0x03 == 0:
        button = "释放"
    elif b & 0x03 == 1:
        button = "左键按下"
    elif b & 0x03 == 2:
        button = "中键按下"
    elif b & 0x03 == 3:
        button = "右键按下"
    
    # 判断是否为移动事件（b的第6位为1表示移动）
    is_move = (b & 0x40) != 0
    event_type = "移动" if is_move else "点击"
    
    return {
        "type": event_type,
        "button": button,
        "x": x,
        "y": y
    }

def main():
    try:
        # 启用鼠标监听
        enable_mouse_mode()
        print("鼠标监听已启用（按 Ctrl+C 或 ESC 键退出）...")
        print("格式：[事件类型] [按键] (x, y)")
        
        while True:
            # 关键：msvcrt.kbhit() 检测是否有字符输入（非阻塞）
            if msvcrt.kbhit():
                # msvcrt.getch() 读取单个字符（无缓冲，实时返回）
                c = msvcrt.getch().decode('latin-1')  # 解码兼容特殊字符
                # 退出条件：Ctrl+C（ASCII 3）或 ESC（ASCII 27）
                if ord(c) == 3 or ord(c) == 27:
                    break
                # 检测鼠标事件起始标记（ESC 字符）
                if c == "\x1b":
                    # 读取剩余4个字符（组成完整鼠标事件）
                    rest = ""
                    for _ in range(4):
                        if msvcrt.kbhit():
                            rest += msvcrt.getch().decode('latin-1')
                        else:
                            rest += ""
                    # 解析并输出鼠标事件
                    event = parse_mouse_event(c + rest)
                    if event:
                        # \r 用于覆盖当前行输出，保持界面整洁
                        print(f"\r[{event['type']}] {event['button']} ({event['x']}, {event['y']}) ", end="")
    except KeyboardInterrupt:
        # 捕获 Ctrl+C 异常，保证后续清理代码执行
        pass
    finally:
        # 无论正常退出还是异常退出，都关闭鼠标模式并恢复终端
        disable_mouse_mode()
        print("\n鼠标监听已关闭")

if __name__ == "__main__":
    main()