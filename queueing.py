class Queue:
    def __init__(self):
        self._items = []
    
    def is_empty(self):
        return self._items == []
    
    def enqueue(self, item, priority: int = -1):
        assert priority >= -1
        assert type(priority) == int
        if priority == -1:
            self._items.append(item)
        else:
            if priority >= len(self._items)-1 :
                self._items.append(item)
            else:
                self._items.insert(priority+1, item)
    
    def dequeue(self, priority: int = 0):
        assert priority >= -1
        assert type(priority) == int
        try:
            return self._items.pop(priority)
        except IndexError:
            return
    
    @property
    def size(self):
        return len(self.items)
    
    @property
    def items(self):
        return self._items