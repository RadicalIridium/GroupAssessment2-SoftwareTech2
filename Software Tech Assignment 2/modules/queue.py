

class Queue:
    def __init__(self):
        self._data = []

    def enqueue(self, val):
        self._data.append(val)
    
    def dequeue(self):
        if not self.is_empty():
            return self._data.pop(0)
        raise IndexError("pop from empty queue")
    
    def peek(self):
        if not self.is_empty():
            return self._data[0]
        raise IndexError("peek from empty queue")
    
    def is_empty(self):
        return len(self._data) == 0
    
    def size(self):
        return len(self._data)
    
    def __repr__(self):
        return f"Queue({self._data})"

