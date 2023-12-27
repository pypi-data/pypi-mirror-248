class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def print_tree(self, level=0, is_last=False):
        prefix = "│   " * level  # Prefix for indentation
        connector = "└── " if is_last else "├── "

        print(prefix + connector + self.data)

        for i, child in enumerate(self.children):
            child.print_tree(level + 1, i == len(self.children) - 1)
