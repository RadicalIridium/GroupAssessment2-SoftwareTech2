"""
Module, created with assitance of W6 tutorial work, Online resources, and AI assistance for Animation utility functions.
"""


class Node:
    def __init__(self, val):
        self.value = val
        self.next = None

    def __repr__(self):
        return f"Node({self.value})"

class LinkedList:
    def __init__(self):
        self.head = None

    def to_nodes(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(current)
            current = current.next
        return nodes
    
    def length(self):
        return len(self.to_nodes())
    
    def __repr__(self):
        return "->".join(str(node.value) for node in self.to_nodes()) + "-> None"
    
    def insert(self, val, index):
        new_node = Node(val)
        
        if index <= 0 or self.head is None:
            new_node.next = self.head
            self.head = new_node
            return
        
        current = self.head
        for _ in range(index - 1):
            if current.next is None:
                break
            current = current.next

        new_node.next = current.next
        current.next = new_node
        return new_node
    
    def find_insert_traverse_path(self, index):
        path = []
        current = self.head
        steps = min(index, self.length())   # clamp to list length
        for _ in range(steps):
            if current is None:
                break
            path.append(current)
            current = current.next
        return path
    
    def find_by_value(self, val):
        current = self.head
        while current:
            if current.value == val:
                return current
            current = current.next
        return None
    
    def find_search_path(self, val):
        path = []
        current = self.head
        while current:
            path.append(current)
            if current.value == val:
                break
            current = current.next
        return path
    
    def delete_by_value(self, val):
        if self.head is None:
            return False
        
        if self.head.value == val:
            self.head = self.head.next
            return True
        
        current = self.head
        while current.next:
            if current.next.value == val:
                current.next = current.next.next
                return True
            current = current.next
        
        return False
    
    def get_reverse_steps(self):
        steps = []
        prev = None
        current = self.head

        while current:
            next_node = current.next
            steps.append((prev, current, next_node))
            prev = current
            current = next_node

        return steps
    
    def reverse(self):
        prev = None
        current = self.head

        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        self.head = prev