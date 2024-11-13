import os

class FileChecker:
    def __init__(self, file_path, cwd_abs, ignore_paths_abs):
        self.file_path = file_path
        self.cwd_abs = cwd_abs
        self.ignore_paths_abs = ignore_paths_abs
        self.warning = None

    def is_displayable(self):
        # Check if file exists and is within the tree
        if not self.file_path.startswith(self.cwd_abs):
            self.warning = f"Warning: '{self.get_relative_path()}' is not under the specified cwd."
            return False
        if not os.path.isfile(self.file_path):
            self.warning = f"Warning: '{self.get_relative_path()}' does not exist or is not a file."
            return False
        # Check if the file is not under an ignored path
        for ignore_path in self.ignore_paths_abs:
            if self.file_path.startswith(ignore_path):
                self.warning = f"Warning: '{self.get_relative_path()}' was not displayed (it is under an ignored path)."
                return False
        # File is displayable
        return True

    def get_warning(self):
        return self.warning

    def get_relative_path(self):
        return os.path.relpath(self.file_path, self.cwd_abs)

class FilePrinter:
    def __init__(self, file_path, cwd_abs):
        self.file_path = file_path
        self.cwd_abs = cwd_abs

    def print_content(self):
        rel_path = os.path.relpath(self.file_path, self.cwd_abs)
        print(f"\n./{rel_path}")
        print('```')
        try:
            with open(self.file_path, 'r') as f:
                content = f.read()
            print(content)
        except Exception as e:
            print(f"Error reading file '{rel_path}': {e}")
        print('```')

class FileContentManager:
    def __init__(self, specified_files_abs, cwd_abs, ignore_paths_abs):
        self.specified_files_abs = specified_files_abs
        self.cwd_abs = cwd_abs
        self.ignore_paths_abs = ignore_paths_abs
        self.displayed_files = set()

    def process_files(self):
        for file_path in self.specified_files_abs:
            checker = FileChecker(file_path, self.cwd_abs, self.ignore_paths_abs)
            if checker.is_displayable():
                printer = FilePrinter(file_path, self.cwd_abs)
                printer.print_content()
                self.displayed_files.add(file_path)
            else:
                print(checker.get_warning())
