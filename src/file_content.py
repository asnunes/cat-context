import os

class FileChecker:
    def __init__(self, file_path, cwd_abs, ignore_paths_abs):
        self.file_path = file_path
        self.cwd_abs = cwd_abs
        self.ignore_paths_abs = ignore_paths_abs
        self.warning = None

    def is_displayable(self):
        # Check if file is within the tree
        if not self.file_path.startswith(self.cwd_abs):
            self.warning = f"Warning: '{self.get_relative_path()}' is not under the specified cwd."
            return False
        # Check if the path exists
        if not os.path.exists(self.file_path):
            self.warning = f"Warning: '{self.get_relative_path()}' does not exist."
            return False
        # Check if the path is a file
        if not os.path.isfile(self.file_path):
            if os.path.isdir(self.file_path):
                self.warning = f"Warning: '{self.get_relative_path()}' is a directory, not a file."
            else:
                self.warning = f"Warning: '{self.get_relative_path()}' is not a regular file."
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

    def print_content(self, start_line=None, end_line=None):
        rel_path = os.path.relpath(self.file_path, self.cwd_abs)

        file_info = rel_path
        if start_line is not None:
            file_info += f" from line {start_line}"
            if end_line is not None:
                file_info += f" to line {end_line}"

        print(f"\n./{file_info}")
        print('```')
        try:
            with open(self.file_path, 'r') as f:
                lines = f.readlines()
                total_lines = len(lines)
                # Adjust start_line and end_line
                # Line numbers start from 0 as per user's example
                if start_line is None:
                    start_idx = 0
                else:
                    start_idx = start_line
                if end_line is None:
                    end_idx = total_lines
                else:
                    # Since end_line is inclusive, add 1 to make it exclusive in slicing
                    end_idx = end_line + 1

                # Ensure indices are within bounds
                start_idx = max(0, start_idx - 1)
                end_idx = min(end_idx - 1, total_lines)

                if start_idx >= total_lines:
                    content = ''
                else:
                    content = ''.join(lines[start_idx:end_idx])

                print(content)
        except Exception as e:
            print(f"Error reading file '{rel_path}': {e}")
        print('```')

class FileContentManager:
    def __init__(self, specified_files, cwd_abs, ignore_paths_abs):
        self.specified_files = specified_files
        self.cwd_abs = cwd_abs
        self.ignore_paths_abs = ignore_paths_abs
        self.displayed_files = set()

    def process_files(self):
        for file_info in self.specified_files:
            file_path = file_info['path']
            start_line = file_info.get('start_line')
            end_line = file_info.get('end_line')
            checker = FileChecker(file_path, self.cwd_abs, self.ignore_paths_abs)
            if checker.is_displayable():
                printer = FilePrinter(file_path, self.cwd_abs)
                printer.print_content(start_line, end_line)
                self.displayed_files.add(file_path)
            else:
                print(checker.get_warning())
