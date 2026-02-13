import ctypes

STD_OUTPUT_HANDLE = -11
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

def get_console_mode():
    h_out = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    if h_out == -1:
        return None
    mode = ctypes.c_ulong()
    if ctypes.windll.kernel32.GetConsoleMode(h_out, ctypes.byref(mode)):
        return mode.value
    return None

def disable_virtual_terminal():
    h_out = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    if h_out == -1:
        return False
    mode = ctypes.c_ulong()
    if not ctypes.windll.kernel32.GetConsoleMode(h_out, ctypes.byref(mode)):
        return False
    mode.value &= ~ENABLE_VIRTUAL_TERMINAL_PROCESSING
    if ctypes.windll.kernel32.SetConsoleMode(h_out, mode):
        return True
    return False

def enable_virtual_terminal():
    h_out = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    if h_out == -1:
        return False
    mode = ctypes.c_ulong()
    if not ctypes.windll.kernel32.GetConsoleMode(h_out, ctypes.byref(mode)):
        return False
    mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
    if not ctypes.windll.kernel32.SetConsoleMode(h_out, mode):
        return False
    return True

def hex_to_rgb(hex_str: str):
    hex_str = hex_str.lstrip('#')
    r, g, b = tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    return r, g, b

def rgb_to_hex(r: int, g: int, b: int):
    return f'#{r:02x}{g:02x}{b:02x}'
