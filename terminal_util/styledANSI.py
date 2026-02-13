from typing import Any

class Foreground:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    LIGHT_BLACK = '\033[90m'
    LIGHT_RED = '\033[91m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_YELLOW = '\033[93m'
    LIGHT_BLUE = '\033[94m'
    LIGHT_MAGENTA = '\033[95m'
    LIGHT_CYAN = '\033[96m'
    LIGHT_WHITE = '\033[97m'
    RESET = '\033[39m'
    class hexColor:
        def __call__(self, **kwargs) -> str:
            return self.format(**kwargs)
        def format(self, **kwargs) -> str:
            if 'r' in kwargs.keys() and 'g' in kwargs.keys() and 'b' in kwargs.keys():
                r = kwargs['r']
                g = kwargs['g']
                b = kwargs['b']
            elif 'hex' in kwargs.keys():
                if kwargs['hex'][0] == '#':
                    hex_str = kwargs['hex'][1:]
                elif len(kwargs['hex']) == 6:
                    hex_str = kwargs['hex']
                else:
                    raise ValueError('Invalid hex color code')
                r = int(hex_str[:2], 16)
                g = int(hex_str[2:4], 16)
                b = int(hex_str[4:], 16)
            return f'\033[38;2;{r};{g};{b}m'
    class gray:
        def __call__(self, level: int) -> str:
            return self.format(level)
        def format(self, level: int) -> str:
            if level < 0 or level > 15:
                raise ValueError('Invalid gray level')
            return f'\033[38;5;{level+232}m'
    class rgb666:
        def __call__(self, **kwargs) -> str:
            return self.format(**kwargs)
        def format(self, **kwargs) -> str:
            if 'r' in kwargs.keys() and 'g' in kwargs.keys() and 'b' in kwargs.keys():
                r = kwargs['r']
                g = kwargs['g']
                b = kwargs['b']
            elif 'hex' in kwargs.keys():
                r = int(kwargs['hex'][1:3])
                g = int(kwargs['hex'][3:5])
                b = int(kwargs['hex'][5:])
            return f'\033[38;5;{int(r)*36+int(g)*6+int(b)+16}m'
    class leagcy16c:
        def __call__(self, color_code: int) -> str:
            return self.format(color_code)
        def format(self, color_code: int) -> str:
            if color_code < 0 or color_code > 15:
                raise ValueError('Invalid color code')
            return f'\033[38;5;{color_code+16}m'
    
class Background:
    BLACK = '\033[40m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BLUE = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN = '\033[46m'
    WHITE = '\033[47m'
    LIGHT_BLACK = '\033[100m'
    LIGHT_RED = '\033[101m'
    LIGHT_GREEN = '\033[102m'
    LIGHT_YELLOW = '\033[103m'
    LIGHT_BLUE = '\033[104m'
    LIGHT_MAGENTA = '\033[105m'
    LIGHT_CYAN = '\033[106m'
    LIGHT_WHITE = '\033[107m'
    RESET = '\033[49m'
    class hexColor:
        def __call__(self, **kwargs) -> str:
            return self.format(**kwargs)
        def format(self, **kwargs) -> str:
            if 'r' in kwargs.keys() and 'g' in kwargs.keys() and 'b' in kwargs.keys():
                r = kwargs['r']
                g = kwargs['g']
                b = kwargs['b']
            elif 'hex' in kwargs.keys():
                if kwargs['hex'][0] == '#':
                    hex_str = kwargs['hex'][1:]
                elif len(kwargs['hex']) == 6:
                    hex_str = kwargs['hex']
                else:
                    raise ValueError('Invalid hex color code')
                r = int(hex_str[:2], 16)
                g = int(hex_str[2:4], 16)
                b = int(hex_str[4:], 16)
            return f'\033[48;2;{r};{g};{b}m'
    class gray:
        def __call__(self, level: int) -> str:
            return self.format(level)
        def format(self, level: int) -> str:
            if level < 0 or level > 15:
                raise ValueError('Invalid gray level')
            return f'\033[48;5;{level+232}m'
    class rgb666:
        def __call__(self, **kwargs) -> str:
            return self.format(**kwargs)
        def format(self, **kwargs) -> str:
            if 'r' in kwargs.keys() and 'g' in kwargs.keys() and 'b' in kwargs.keys():
                r = kwargs['r']
                g = kwargs['g']
                b = kwargs['b']
            elif 'hex' in kwargs.keys():
                r = int(kwargs['hex'][1:3])
                g = int(kwargs['hex'][3:5])
                b = int(kwargs['hex'][5:])
            return f'\033[48;5;{int(r)*36+int(g)*6+int(b)+16}m'
    class leagcy16c:
        def __call__(self, color_code: int) -> str:
            return self.format(color_code)
        def format(self, color_code: int) -> str:
            if color_code < 0 or color_code > 15:
                raise ValueError('Invalid color code')
            return f'\033[48;5;{color_code+16}m'

class Style:
    BOLD = '\033[1m'
    CANECL_BOLD = '\033[21m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    CANECL_UNDERLINE = '\033[24m'
    UPLINE = '\033[53m'
    CANECL_UPLINE = '\033[55m'
    BLINK = '\033[5m'
    QUICKLY_BLINK = '\033[6m'
    CANECL_BLINK = '\033[25m'
    HIDDEN = '\033[8m'
    DELETE = '\033[9m'
    REVERSE = '\033[7m'
    CANECL_REVERSE = '\033[27m'
    RESET = '\033[0m'

class Special:
    ENABLE_VIRTUAL_TERMINAL = '\033[?1049h'
    DISABLE_VIRTUAL_TERMINAL = '\033[?1049l'
    SET_ALT_BUFFER = '\033[?1049h'
    SET_MAIN_BUFFER = '\033[?1049l'

class Cursor:
    LF_UP = '\033[H'
    GOTO = '\033[{0};{1}H'
    class GOTO:
        def format(x: int | str, y: int | str, use_H_suffix: bool = True) -> str:
            return f'\033[{y+1};{x+1}{"H" if use_H_suffix else "f"}'
    UP = '\033[A'
    DOWN = '\033[B'
    RIGHT = '\033[C'
    LEFT = '\033[D'
    HIDE = '\033[?25l'
    SHOW = '\033[?25h'
    POS_SAVE = '\033[s'
    POS_RESTORE = '\033[u'

class Input:
    ENABLE_INPUT_ECHO = '\033[?12h'
    DISABLE_INPUT_ECHO = '\033[?12l'
    ENABLE_APPLY_KEYBOARD = '\033[?1h'
    DISALBE_APPLY_KEYBOARD = '\033[?1l'
    DISABLE_AUTO_CHANGE_LINE = '\033[20h'
    RESET_AUTO_CHANGE_LINE = '\033[20l'
    EMABLE_MOUSE_REPORT = '\033[?1002h'
    DISALBE_MOUSE_REPORT = '\033[?1002l'

class Query:
    TERMINAL_SIZE = '\033[18t'
    CURSOR_POS = '\033[6n'
    TERMINAL_TYPE = '\033[0c'

class Screen:
    CLEAR_ALL = '\033[2J'
    CLEAR_BEFORE = '\033[1J'
    CLEAR_AFTER = '\033[0J'
    CLEAR_AFTER_LINE = '\033[K'
    ENABLE_BACKUP_BUFFER = '\033[?1049h'
    DISBALE_BACKUP_BUFFER = '\033[?1049l'

class OTS:
    def __call__(self, link: str, text: str=None) -> str:
        text = text if text else link
        return self.format(link, text)
    def format(self, link: str, text: str) -> str:
        return f'\033]8;;{link}\007{text}\033]8;;\007'

class WindowsTerminalFeatures:
    BLINK_TAB = '\033]35;flash\007'
    class SET_TITLE:
        def __call__(self, title: str) -> str:
            return self.format(title)
        def format(self, title: str) -> str:
            return f'\033]0;{title}\007'
    class SET_ICON_NAME:
        def __call__(self, icon_name: str) -> str:
            return self.format(icon_name)
        def format(self, icon_name: str) -> str:
            return f'\033]1;{icon_name}\007'
    