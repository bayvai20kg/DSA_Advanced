"""
Radix Trie (Patricia Trie) implementation for English Dictionary.
Each node stores a compressed prefix string to reduce memory usage.
"""

class RadixNode:
    def __init__(self, label=""):
        self.label = label          # Compressed edge label
        self.children = {}          # char -> RadixNode
        self.is_end = False         # Marks end of a word
        self.definition = None      # Word definition (only set at leaf/end nodes)

    def __repr__(self):
        return f"RadixNode(label={self.label!r}, is_end={self.is_end})"


class RadixTrie:
    """
    Radix Trie (Compressed Trie) data structure.
    Supports insert, delete, and search operations.
    """

    def __init__(self):
        self.root = RadixNode("")
        self.size = 0

    # ------------------------------------------------------------------ #
    #  HELPER: find common prefix length between two strings              #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _common_prefix_len(a: str, b: str) -> int:
        i = 0
        while i < len(a) and i < len(b) and a[i] == b[i]:
            i += 1
        return i

    # ------------------------------------------------------------------ #
    #  INSERT                                                              #
    # ------------------------------------------------------------------ #
    def insert(self, word: str, definition: str) -> bool:
        """
        Insert (word, definition) into the trie.
        Returns True if a NEW word was added, False if it already existed
        (definition is updated in that case).
        """
        word = word.lower().strip()
        if not word:
            return False

        node = self.root
        remaining = word

        while remaining:
            first_char = remaining[0]

            if first_char not in node.children:
                # No matching child – create new leaf
                new_node = RadixNode(remaining)
                new_node.is_end = True
                new_node.definition = definition
                node.children[first_char] = new_node
                self.size += 1
                return True

            child = node.children[first_char]
            cp = self._common_prefix_len(remaining, child.label)

            if cp == len(child.label):
                # Full match with the edge label – go deeper
                remaining = remaining[cp:]
                if not remaining:
                    # Word ends exactly at this node
                    if child.is_end:
                        child.definition = definition  # update
                        return False
                    else:
                        child.is_end = True
                        child.definition = definition
                        self.size += 1
                        return True
                node = child
            else:
                # Partial match – split the edge
                common = child.label[:cp]
                old_suffix = child.label[cp:]
                new_suffix = remaining[cp:]

                # Shrink existing child
                child.label = old_suffix
                split_node = RadixNode(common)
                split_node.children[old_suffix[0]] = child
                node.children[first_char] = split_node

                if new_suffix:
                    # New word diverges here
                    leaf = RadixNode(new_suffix)
                    leaf.is_end = True
                    leaf.definition = definition
                    split_node.children[new_suffix[0]] = leaf
                    self.size += 1
                else:
                    # Word ends at the split node
                    split_node.is_end = True
                    split_node.definition = definition
                    self.size += 1
                return True

        return False

    # ------------------------------------------------------------------ #
    #  SEARCH                                                              #
    # ------------------------------------------------------------------ #
    def search(self, word: str):
        """
        Returns the definition string if found, else None.
        """
        word = word.lower().strip()
        node = self.root
        remaining = word

        while remaining:
            first_char = remaining[0]
            if first_char not in node.children:
                return None
            child = node.children[first_char]
            cp = self._common_prefix_len(remaining, child.label)
            if cp < len(child.label):
                return None
            remaining = remaining[cp:]
            node = child

        return node.definition if node.is_end else None

    # ------------------------------------------------------------------ #
    #  DELETE                                                              #
    # ------------------------------------------------------------------ #
    def delete(self, word: str) -> bool:
        """
        Delete a word from the trie.
        Returns True if the word was found and removed, False otherwise.
        Merges nodes where possible to keep the trie compressed.
        """
        word = word.lower().strip()

        def _delete(node: RadixNode, remaining: str):
            """
            Recursive helper.  Returns True if the current node should be
            removed from its parent's children dict.
            """
            if not remaining:
                if not node.is_end:
                    return False  # word not found
                node.is_end = False
                node.definition = None
                self.size -= 1
                # Remove this node if it has no children
                return len(node.children) == 0

            first_char = remaining[0]
            if first_char not in node.children:
                return False  # word not found

            child = node.children[first_char]
            cp = self._common_prefix_len(remaining, child.label)
            if cp < len(child.label):
                return False  # word not found

            should_remove = _delete(child, remaining[cp:])

            if should_remove:
                del node.children[first_char]
                # Merge: if current node now has exactly one child,
                # is not a word-end, and is not root – merge with child
                if (not node.is_end and len(node.children) == 1
                        and node is not self.root):
                    only_child = next(iter(node.children.values()))
                    node.label += only_child.label
                    node.is_end = only_child.is_end
                    node.definition = only_child.definition
                    node.children = only_child.children
            return False

        result = _delete(self.root, word)
        return result or True  # _delete returns False at root level; check size instead

    # ------------------------------------------------------------------ #
    #  UTILITY: collect all words (for display)                           #
    # ------------------------------------------------------------------ #
    def all_words(self):
        """Returns a sorted list of (word, definition) tuples."""
        results = []

        def _traverse(node: RadixNode, prefix: str):
            prefix += node.label
            if node.is_end:
                results.append((prefix, node.definition))
            for child in node.children.values():
                _traverse(child, prefix)

        for child in self.root.children.values():
            _traverse(child, "")

        return sorted(results, key=lambda x: x[0])

    # ------------------------------------------------------------------ #
    #  UTILITY: visualise trie structure (ASCII)                          #
    # ------------------------------------------------------------------ #
    def visualize(self) -> str:
        lines = ["Radix-Trie Structure:", "=" * 40]

        def _draw(node: RadixNode, prefix: str, is_last: bool, indent: str):
            connector = "└── " if is_last else "├── "
            label_display = repr(node.label) if node.label else "(root)"
            marker = " ●" if node.is_end else ""
            lines.append(f"{indent}{connector}{label_display}{marker}")
            child_indent = indent + ("    " if is_last else "│   ")
            children = list(node.children.values())
            for i, child in enumerate(children):
                _draw(child, prefix + node.label, i == len(children) - 1, child_indent)

        children = list(self.root.children.values())
        for i, child in enumerate(children):
            _draw(child, "", i == len(children) - 1, "")

        lines.append("=" * 40)
        lines.append(f"Total words: {self.size}")
        return "\n".join(lines)