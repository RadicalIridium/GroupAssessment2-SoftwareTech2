"""

"""
from collections import deque

class Node:
    def __init__(self, val):
        self.value = val
        self.left = None
        self.right = None

    def __repr__(self):
        return f"Node({self.value})"
    
class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, val):
        self.root = self._insert(self.root, val)
    
    def _insert(self, root, val):
        if root is None:
            return Node(val)
        if val < root.value:
            root.left = self._insert(root.left, val)
        else:
            root.right = self._insert(root.right, val)
        return root
    

    def search(self, val):
        return self._search(self.root, val)
    
    def _search(self, root, val):
        if root is None or root.value == val:
            return root
        if val < root.value:
            return self._search(root.left, val)
        return self._search(root.right, val)    
    
    def inorder(self):
        return self._inorder(self.root)
    
    def _inorder(self, root):
        if root is None:
            return []
        return ( 
            self._inorder(root.left)
            + [root.value]
            + self._inorder(root.right)
        )
    
    def inorder_nodes(self):
        result = []
        self._inorder_nodes(self.root, result)
        return result

    def _inorder_nodes(self, root, result):
        if root is None:
            return
        self._inorder_nodes(root.left, result)
        result.append(root)
        self._inorder_nodes(root.right, result)

    def preorder(self):
        return self._preorder(self.root)
    
    def _preorder(self, root):
        if root is None:
            return []
        return (
            [root.value]
            + self._preorder(root.left)
            + self._preorder(root.right)
        )
    
    def preorder_nodes(self):
        result = []
        self._preorder_nodes(self.root, result)
        return result

    def _preorder_nodes(self, root, result):
        if root is None:
            return
        result.append(root)
        self._preorder_nodes(root.left, result)
        self._preorder_nodes(root.right, result)

    def postorder(self):
        return self._postorder(self.root)

    def _postorder(self, root):
        if root is None:
            return []
        return (
            self._postorder(root.left)
            + self._postorder(root.right)
            + [root.value]
        )
    
    def postorder_nodes(self):
        result = []
        self._postorder_nodes(self.root, result)
        return result

    def _postorder_nodes(self, root, result):
        if root is None:
            return
        self._postorder_nodes(root.left, result)
        self._postorder_nodes(root.right, result)
        result.append(root)

    def count_nodes(self):
        return self._count_nodes(self.root)

    def _count_nodes(self, root):
        if root is None:
            return 0
        return 1 + self._count_nodes(root.left) + self._count_nodes(root.right)
    
    def height(self):
        return self._height(self.root)
    
    def _height(self, root):
        if root is None:
            return 0
        return 1 + max(self._height(root.left), self._height(root.right))
    
    def _find_min(self, root):
        current = root
        while current.left:
            current = current.left
        return current
    
    def delete(self, val):
        self.root = self._delete_node(self.root, val)

    def _delete_node(self, root, val):
        if root is None:
            return None
        if val < root.value:
            root.left = self._delete_node(root.left, val)
        elif val > root.value:
            root.right = self._delete_node(root.right, val)
        else:
            # Node with 1 or no child
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            # Node with two children
            temp = self._find_min(root.right)
            root.value = temp.value
            root.right = self._delete_node(root.right, temp.value)
        return root

    def level_order_nodes(self):
        if not self.root:
            return []
        
        result = []
        queue = deque([self.root])

        while queue:
            node = queue.popleft()
            result.append(node)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return result
    

    
    def __repr__(self):
        return f"BinaryTree({self.level_order_nodes()})"
    
    #Adding Some Animation Functions for the Visualiser
    def insert_with_path(self, val):
        path = []
        self.root = self._insert_with_path(self.root, val, path)
        return path
    
    def _insert_with_path(self, root, val, path):
        if root is None:
            path.append(None)  
            return Node(val)

        path.append(root.value)

        if val < root.value:
            root.left = self._insert_with_path(root.left, val, path)
        else:
            root.right = self._insert_with_path(root.right, val, path)

        return root 
    
    def find_insert_path(self, val):
        path = []
        current = self.root

        while current:
            path.append(current)
            if val < current.value:
                if current.left is None:
                    break
                current = current.left
            
            else:
                if current.right is None:
                    break
                current = current.right

        path.append(None)
        return path