import os


class FileChecker:
    def __init__(self, file_path, cwd_abs, ignore_paths_abs):
        self.file_path = file_path
        self.cwd_abs = cwd_abs
        self.ignore_paths_abs = ignore_paths_abs
        self.warning = None

    def is_displayable(self):
        if not self._is_within_tree():
            self._append_warning(
                f"'{self.get_relative_path()}' is not under the specified cwd."
            )
            return False

        if not self._exists():
            self._append_warning(f"'{self.get_relative_path()}' does not exist.")
            return False

        if not self._is_file():
            if os.path.isdir(self.file_path):
                self._append_warning(
                    f"'{self.get_relative_path()}' is a directory, not a file."
                )
            else:
                self._append_warning(
                    f"'{self.get_relative_path()}' is not a regular file."
                )
            return False

        if self._is_under_ignored_path():
            self._append_warning(
                f"'{self.get_relative_path()}' is under an ignored path and will not be displayed."
            )
            return False

        return True

    def get_warning(self):
        return self.warning

    def get_relative_path(self):
        return os.path.relpath(self.file_path, self.cwd_abs)

    def _is_within_tree(self):
        return os.path.commonpath([self.file_path, self.cwd_abs]) == self.cwd_abs

    def _exists(self):
        return os.path.exists(self.file_path)

    def _is_file(self):
        return os.path.isfile(self.file_path)

    def _is_under_ignored_path(self):
        for ignore_path in self.ignore_paths_abs:
            if self.file_path.startswith(ignore_path):
                return True
        return False

    def _append_warning(self, warning):
        if self.warning is None:
            self.warning = ""

        self.warning += f"\nWarning: {warning}"


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
        print("```")
        try:
            with open(self.file_path, "r") as f:
                lines = f.readlines()
                total_lines = len(lines)

                # Adjust start_line and end_line
                if start_line is None:
                    start_idx = 0
                else:
                    start_idx = start_line - 1  # Convert to 0-based index

                if end_line is None:
                    end_idx = total_lines
                else:
                    end_idx = end_line  # end_line is inclusive

                # Ensure indices are within bounds
                start_idx = max(0, start_idx)
                end_idx = min(end_idx, total_lines)

                if start_idx >= end_idx:
                    content = ""
                else:
                    content = "".join(lines[start_idx:end_idx])

                print(content)
        except Exception as e:
            print(f"Error reading file '{rel_path}': {e}")
        print("```")


class FileContentManager:
    def __init__(self, specified_files, cwd_abs, ignore_paths_abs):
        self.specified_files = specified_files
        self.cwd_abs = cwd_abs
        self.ignore_paths_abs = ignore_paths_abs
        self.displayed_files = set()

    def process_files(self):
        any_files_displayed = False

        for file_info in self.specified_files:
            file_path = file_info["path"]
            start_line = file_info.get("start_line")
            end_line = file_info.get("end_line")
            checker = FileChecker(file_path, self.cwd_abs, self.ignore_paths_abs)
            if checker.is_displayable():
                printer = FilePrinter(file_path, self.cwd_abs)
                printer.print_content(start_line, end_line)
                self.displayed_files.add(file_path)
                any_files_displayed = True
            else:
                warning = checker.get_warning()
                if warning:
                    print(warning)

        return any_files_displayed
