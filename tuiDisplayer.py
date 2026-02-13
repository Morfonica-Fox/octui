import keyListener as kl
from terminal_util.consoleScreen import get_terminal_size, clear_console
import sys
import terminal_util.styledANSI as styledANSI
import mouseTracker as mt
from terminal_util.winFeatures.realColor import *
from widgets.errors import *
from widgets.basic import *

class Displayer:
    def __init__(self, addressBarStyle: dict={'dir': styledANSI.Foreground.LIGHT_BLACK, 'name': styledANSI.Foreground.LIGHT_BLUE}):
        self._children = {}
        self.lastDisplayedWidgetPath = ''
        self.lastDisplayedWidgetDir = ''
        self.lastDisplayedWidgetName = ''
        self._addressBarStyle = addressBarStyle
    
    def add_child(self, child: Widget):
        self._children[child.get_full_path()] = child
    
    def remvoe_child(self, path):
        if path in self._children:
            del self._children[path]
    
    def display(self, child: Widget=None):
        self.lastDisplayedWidgetPath = child.get_full_path()
        self.lastDisplayedWidgetDir = child.get_dir_path()
        self.lastDisplayedWidgetName = child.get_name()
        text, pos = child.display()
        dirStyle, nameStyle = self._addressBarStyle['dir'], self._addressBarStyle['name']
        sys.stdout.write(''.join((styledANSI.Cursor.HIDE,
                                  styledANSI.Cursor.LF_UP,
                                  #styledANSI.Screen.CLEAR_ALL
        ))) # 清屏(已禁用), 设置光标位置, 隐藏光标
        term_y, term_x = get_terminal_size()
        sys.stdout.write('\n'.join([' '*term_x]*term_y)) # 填充屏幕 用于取代清屏
        sys.stdout.write(''.join((styledANSI.Cursor.HIDE,
                                  styledANSI.Cursor.LF_UP,
                                  #styledANSI.Screen.CLEAR_ALL
        ))) # 清屏(已禁用), 设置光标位置, 隐藏光标
        sys.stdout.write(''.join((dirStyle,
                                  self.lastDisplayedWidgetDir,
                                  styledANSI.Style.RESET,
                                  nameStyle,
                                  self.lastDisplayedWidgetName,
                                  styledANSI.Style.RESET,
        ))) # 显示地址栏
        sys.stdout.write(styledANSI.Cursor.GOTO.format(x=pos[0]+2, y=pos[1]+1))
        sys.stdout.write(text)
        sys.stdout.flush()
    
    @property
    def addressBarStyle(self):
        return self._addressBarStyle
    
    @addressBarStyle.setter
    def addressBarStyle(self, value):
        if type(value) is not dict:
            raise TypeError('addressBarStyle must be a dict')
        self._addressBarStyle = value
    
    @addressBarStyle.deleter
    def addressBarStyle(self):
        self._addressBarStyle = {'dir': styledANSI.Foreground.LIGHT_BLACK, 'name': styledANSI.Foreground.LIGHT_BLUE}
    
    @property
    def children(self):
        return self._children
    
    @children.setter
    def children(self, value):
        self._children = value
    
    @children.deleter
    def children(self):
        self._children = {}

if __name__ == '__main__': # 测试代码
    try:
        test_root = BaseWidget()
        test_node1 = BaseWidget("node1", parent=test_root)
        test_node2 = BaseWidget("node2", parent=test_root)
        test_node3 = BaseWidget("node3", parent=test_node2)
        test_node4 = Node("node4", parent=test_node3) # Node = BaseWidget
        test_widget = Widget("test_widget", parent=test_node4, width=10, height=3)
        test_widget2 = Widget("test_widget2", parent=test_node4, width=10, height=3)
        
        enable_virtual_terminal()
        
        clear_console(with_command=True)
        
        displayer = Displayer()
        displayer.add_child(test_widget)
        displayer.display(test_widget)

        input()
        
        displayer.addressBarStyle = {'dir': styledANSI.Foreground.LIGHT_RED, 'name': styledANSI.Foreground.LIGHT_GREEN}
        displayer.display(test_widget2)
        
        input()
    finally:
        print(styledANSI.Cursor.SHOW)