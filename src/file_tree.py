import os
from abc import ABC, abstractmethod

class FileSystemNode(ABC):
    def __init__(self, name, path):
        self.name = name
        self.path = path

    @abstractmethod
    def mount(self):
        pass

    @abstractmethod
    def print(self, prefix='    ', is_last=True):
        pass

class FileNode(FileSystemNode):
    def mount(self):
        # Files do not have children, so nothing to mount
        pass

    def print(self, prefix='    ', is_last=True):
        connector = '└── ' if is_last else '├── '
        print(prefix + connector + self.name)


class FolderNode(FileSystemNode):
    def __init__(self, name, path):
        super().__init__(name, path)
        self.children = []

    def mount(self):
        items = sorted([item for item in os.listdir(self.path) if not item.startswith('.')])
        for item in items:
            full_path = os.path.join(self.path, item)
            if os.path.isdir(full_path):
                node = FolderNode(item, full_path)
                node.mount()
            else:
                node = FileNode(item, full_path)
            self.children.append(node)

    def print(self, prefix='    ', is_last=True):
        connector = '└── ' if is_last else '├── '
        print(prefix + connector + self.name)
        if self.children:
            new_prefix = prefix + ('    ' if is_last else '│   ')
            for idx, child in enumerate(self.children):
                is_last_child = idx == len(self.children) - 1
                child.print(new_prefix, is_last_child)

class RootNode(FolderNode):
    def print(self, prefix='', is_last=True):
        print(self.name)
        if self.children:
            for idx, child in enumerate(self.children):
                is_last_child = idx == len(self.children) - 1
                child.print(is_last=is_last_child)
