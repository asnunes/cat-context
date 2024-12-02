#!/usr/bin/env python3

import os
import sys
import argparse
from cctx.file_tree import RootNode
from cctx.file_content import FileContentManager


def main():
    parser = argparse.ArgumentParser(description="Recursively print the file tree.")
    parser.add_argument(
        "--cwd",
        type=str,
        default=os.getcwd(),
        help="Change the current working directory.",
    )
    parser.add_argument(
        "-ip",
        "--ignore-path",
        action="append",
        default=[],
        help="Paths to ignore in the file tree (relative to cwd or absolute).",
    )
    parser.add_argument(
        "-it",
        "--ignore-tree",
        action="store_true",
        help="Ignore the entire tree and only display specified files.",
    )
    parser.add_argument(
        "file_paths",
        nargs="*",
        help="Files to display contents of if they exist in the tree.",
    )
    args = parser.parse_args()

    cwd = args.cwd
    validate_cwd(cwd)
    cwd_abs = os.path.abspath(cwd)

    ignore_paths_abs = get_ignore_paths_abs(args.ignore_path, cwd_abs)
    ignore_tree = args.ignore_tree
    if not ignore_tree:
        print_file_tree(cwd_abs, ignore_paths_abs)

    specified_files_abs = get_specified_files(args.file_paths, cwd_abs)
    files_displayed = print_files_content(
        specified_files_abs, cwd_abs, ignore_paths_abs
    )

    if args.ignore_tree and not files_displayed:
        print("Warning: No content to display.")


def validate_cwd(cwd):
    if not os.path.isdir(cwd):
        print(f"Error: Directory '{cwd}' does not exist.")
        sys.exit(1)


def get_ignore_paths_abs(ignore_paths, cwd_abs):
    ignore_paths_abs = []
    for p in ignore_paths:
        if os.path.isabs(p):
            ignore_paths_abs.append(os.path.abspath(p))
        else:
            ignore_paths_abs.append(os.path.abspath(os.path.join(cwd_abs, p)))
    return ignore_paths_abs


def print_file_tree(cwd_abs, ignore_paths_abs):
    root_name = "/" + os.path.basename(cwd_abs)
    root_node = RootNode(root_name, cwd_abs)
    root_node.mount(ignore_paths=ignore_paths_abs)
    root_node.print()


def get_specified_files(file_paths, cwd_abs):
    specified_files = []
    for p in file_paths:
        # Parse line numbers if present
        path = p
        start_line = None
        end_line = None
        if ":" in p:
            parts = p.rsplit(":", 2)
            # parts can be [path], [path, start], or [path, start, end]
            if len(parts) == 2:
                path, start_line_str = parts
                end_line_str = None
            elif len(parts) == 3:
                path, start_line_str, end_line_str = parts
            else:
                print(f"Error: Invalid line number format in '{p}'.")
                sys.exit(1)
            # Convert line numbers to integers
            try:
                if start_line_str != "":
                    start_line = int(start_line_str)
                else:
                    start_line = None
                if end_line_str is not None and end_line_str != "":
                    end_line = int(end_line_str)
                else:
                    end_line = None
            except ValueError:
                print(
                    f"Error: Invalid line number format in '{p}'. Line numbers must be integers."
                )
                sys.exit(1)
        else:
            path = p

        # Get absolute path
        if os.path.isabs(path):
            abs_path = os.path.abspath(path)
        else:
            abs_path = os.path.abspath(os.path.join(cwd_abs, path))

        specified_files.append(
            {"path": abs_path, "start_line": start_line, "end_line": end_line}
        )

    return specified_files


def print_files_content(specified_files_abs, cwd_abs, ignore_paths_abs):
    manager = FileContentManager(specified_files_abs, cwd_abs, ignore_paths_abs)
    files_displayed = manager.process_files()
    return files_displayed


if __name__ == "__main__":
    main()
