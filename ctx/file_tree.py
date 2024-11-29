import os
from abc import ABC, abstractmethod


class FileSystemNode(ABC):
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    @abstractmethod
    def mount(self, ignore_paths: list[str] = []):
        pass

    @abstractmethod
    def print(self, prefix: str = "    ", is_last: bool = True):
        pass


class FileNode(FileSystemNode):
    def mount(self, ignore_paths: list[str] = []):
        # Files do not have children, so nothing to mount
        pass

    def print(self, prefix="    ", is_last=True):
        connector = "└── " if is_last else "├── "
        print(prefix + connector + self.name)


class FolderNode(FileSystemNode):
    def __init__(self, name: str, path: str):
        super().__init__(name, path)
        self.children = []

    def mount(self, ignore_paths: list[str] = []):
        if os.path.abspath(self.path) in ignore_paths:
            return

        items = sorted(
            [item for item in os.listdir(self.path) if not item.startswith(".")]
        )
        folders, files = self._get_folders_and_files(items, ignore_paths)

        for item in folders:
            full_path = os.path.join(self.path, item)
            node = FolderNode(item, full_path)
            node.mount(ignore_paths=ignore_paths)
            self.children.append(node)

        for item in files:
            full_path = os.path.join(self.path, item)
            node = FileNode(item, full_path)
            self.children.append(node)

    def print(self, prefix: str = "    ", is_last: bool = True):
        connector = "└── " if is_last else "├── "
        print(prefix + connector + self.name)
        if self.children:
            new_prefix = prefix + ("    " if is_last else "│   ")
            for idx, child in enumerate(self.children):
                is_last_child = idx == len(self.children) - 1
                child.print(new_prefix, is_last_child)

    def _get_folders_and_files(
        self, items: list[str], ignore_paths: list[str]
    ) -> tuple[list[str], list[str]]:
        folders = []
        files = []
        for item in items:
            full_path = os.path.join(self.path, item)
            item_abs_path = os.path.abspath(full_path)
            if item_abs_path in ignore_paths:
                continue
            if os.path.isdir(full_path):
                folders.append(item)
            else:
                files.append(item)

        folders.sort()
        files.sort()

        return folders, files


class RootNode(FolderNode):
    def print(self, prefix: str = "", is_last: bool = True):
        print(self.name)
        if self.children:
            for idx, child in enumerate(self.children):
                is_last_child = idx == len(self.children) - 1
                child.print(is_last=is_last_child)
