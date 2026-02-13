import shutil
import os

def get_terminal_size():
    size = shutil.get_terminal_size(fallback=(1, 1))
    return size.columns, size.lines

def clear_console(with_command=False):
    if with_command:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        return
    print("\033[H\033[J", end="")