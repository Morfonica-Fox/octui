class BaseWidget:
    def __init__(self, name='', info='', parent=None):
        self.name = name
        self.info = info
        self.isroot = not parent
        if parent:
            parent.add_child(self)
        self.parent = parent
        self.children = {}
    
    def add_child(self, child):
        self.children[child.name] = child
    
    def remvoe_child(self, name):
        if name in self.children:
            del self.children[name]
    
    def get_child(self, name):
        if name in self.children:
            return self.children[name]

    def get_children(self):
        return self.children
    
    def get_parent(self):
        return self.parent
    
    def get_full_path(self):
        if self.isroot:
            return f'{self.name}/'
        return f'{self.parent.get_full_path()}{self.name}/'
    
    def get_dir_path(self):
        if self.isroot:
            return f'{self.name}/'
        return f'{self.parent.get_full_path()}'
    
    def get_name(self):
        return self.name
    
    def get_info(self):
        return self.info
    
    def __repr__(self):
        return self.name
    
    def __getitem__(self, key):
        return self.children[key]
    
    def __setitem__(self, key, child):
        self.children[key] = child
        
    def __delitem__(self, key):
        del self.children[key]
    
    def __str__(self):
        return f'{self.name}({self.info})'
    
    def __repo__(self):
        return f'{self.get_dir_path()}/{self.name}'
    
    def __del__(self):
        if self.parent:
            self.parent.remvoe_child(self.name)

Node = BaseWidget

class Widget(BaseWidget):
    def __init__(self, name='', info='', parent: BaseWidget=None, width=5, height=1, style=None):
        super().__init__(name, info, parent)
    
    def display(self):
        return 'Default Widget', (0, 0)