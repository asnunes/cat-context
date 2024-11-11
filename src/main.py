#!/usr/bin/env python3
import os
import sys
import argparse
from file_tree import RootNode

def main():
    parser = argparse.ArgumentParser(description='Recursively print the file tree.')
    parser.add_argument('--cwd', type=str, default=os.getcwd(),
                        help='Change the current working directory.')
    parser.add_argument('--ignore-path', action='append', default=[],
                        help='Paths to ignore in the file tree (relative to cwd or absolute).')
    args = parser.parse_args()

    cwd = args.cwd
    if not os.path.isdir(cwd):
        print(f"Error: Directory '{cwd}' does not exist.")
        sys.exit(1)
    # Get absolute path
    cwd_abs = os.path.abspath(cwd)

    ignore_paths_abs = []
    for p in args.ignore_path:
        if os.path.isabs(p):
            ignore_paths_abs.append(os.path.abspath(p))
        else:
            ignore_paths_abs.append(os.path.abspath(os.path.join(cwd_abs, p)))

    root_name = '/' + os.path.basename(cwd_abs)

    root_node = RootNode(root_name, cwd_abs)
    root_node.mount(ignore_paths=ignore_paths_abs)
    root_node.print()

if __name__ == '__main__':
    main()
