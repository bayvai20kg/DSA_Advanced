class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.values = []
        self.children = []

class BTree:
    def __init__(self, order):
        self.root = BTreeNode(True)
        self.order = order 
        self.min_keys = (order // 2) - 1 if order % 2 == 0 else order // 2
        self.max_keys = order - 1

    def search(self, k, node=None):
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys) and node.keys[i] == k:
            return node.values[i]
        if node.leaf:
            return None
        return self.search(k, node.children[i])

    def insert(self, key, value):
        root = self.root
        if len(root.keys) == self.max_keys:
            temp = BTreeNode()
            self.root = temp
            temp.children.insert(0, root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, key, value)
        else:
            self._insert_non_full(root, key, value)

    def _insert_non_full(self, node, key, value):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            node.values.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                node.values[i + 1] = node.values[i]
                i -= 1
            node.keys[i + 1] = key
            node.values[i + 1] = value
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == self.max_keys:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def _split_child(self, parent, i):
        order = self.order
        mid = order // 2
        child = parent.children[i]
        new_node = BTreeNode(child.leaf)
        
        parent.keys.insert(i, child.keys[mid])
        parent.values.insert(i, child.values[mid])
        parent.children.insert(i + 1, new_node)

        new_node.keys = child.keys[mid + 1:]
        new_node.values = child.values[mid + 1:]
        child.keys = child.keys[:mid]
        child.values = child.values[:mid]

        if not child.leaf:
            new_node.children = child.children[mid + 1:]
            child.children = child.children[:mid + 1]

    def delete(self, key):
        node = self._find_node(self.root, key)
        if node is not None:
            i = node.keys.index(key)
            node.values[i] = None 
            return True
        return False

    def _find_node(self, node, k):
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys) and node.keys[i] == k:
            return node
        if node.leaf:
            return None
        return self._find_node(node.children[i], k)

    def get_all_values(self, node=None, result=None):
        if result is None:
            result = []
        if node is None:
            node = self.root
        
        for i in range(len(node.keys)):
            if not node.leaf:
                self.get_all_values(node.children[i], result)
            if node.values[i] is not None:
                result.append(node.values[i])
        
        if not node.leaf:
            self.get_all_values(node.children[len(node.keys)], result)
        return result

    def get_tree_text(self, node=None, level=0):
        """Hàm đệ quy để xuất cấu trúc cây B-Tree thành chuỗi văn bản"""
        if node is None:
            node = self.root
        
        result = ""
        indent = "        " * level # Thụt lề theo độ sâu của nhánh
        
        # Chỉ hiển thị các key thực sự (khác None)
        valid_keys = [str(k) for i, k in enumerate(node.keys) if node.values[i] is not None]
        keys_str = " | ".join(valid_keys)
        
        if valid_keys or level == 0:
            node_type = "Lá" if node.leaf else "Nhánh"
            if level == 0:
                node_type = "Gốc"
            result += f"{indent}➔ {node_type}: [{keys_str}]\n"
            
        if not node.leaf:
            for child in node.children:
                result += self.get_tree_text(child, level + 1)
                
        return result
