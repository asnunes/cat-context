#!/usr/bin/env python3
import os
import sys
import argparse
from file_tree import RootNode
from file_content import FileContentManager

def main():
    parser = argparse.ArgumentParser(description='Recursively print the file tree.')
    parser.add_argument('--cwd', type=str, default=os.getcwd(),
                        help='Change the current working directory.')
    parser.add_argument('--ignore-path', action='append', default=[],
                        help='Paths to ignore in the file tree (relative to cwd or absolute).')
    parser.add_argument('file_paths', nargs='*',
                        help='Files to display contents of if they exist in the tree.')
    args = parser.parse_args()

    cwd = args.cwd
    validate_cwd(cwd)
    cwd_abs = os.path.abspath(cwd)

    ignore_paths_abs = get_ignore_paths_abs(args.ignore_path, cwd_abs)
    print_file_tree(cwd_abs, ignore_paths_abs)

    specified_files_abs = get_specified_files_abs(args.file_paths, cwd_abs)
    print_files_content(specified_files_abs, cwd_abs, ignore_paths_abs)

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
    root_name = '/' + os.path.basename(cwd_abs)
    root_node = RootNode(root_name, cwd_abs)
    root_node.mount(ignore_paths=ignore_paths_abs)
    root_node.print()

def get_specified_files_abs(file_paths, cwd_abs):
    specified_files_abs = []
    for p in file_paths:
        if os.path.isabs(p):
            specified_files_abs.append(os.path.abspath(p))
        else:
            specified_files_abs.append(os.path.abspath(os.path.join(cwd_abs, p)))

    return specified_files_abs

def print_files_content(specified_files_abs, cwd_abs, ignore_paths_abs):
    manager = FileContentManager(specified_files_abs, cwd_abs, ignore_paths_abs)
    manager.process_files()


if __name__ == '__main__':
    main()
