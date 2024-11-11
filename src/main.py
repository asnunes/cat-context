#!/usr/bin/env python3
import os
import sys
import argparse
from file_tree import RootNode

def main():
    parser = argparse.ArgumentParser(description='Recursively print the file tree.')
    parser.add_argument('--cwd', type=str, default=os.getcwd(),
                        help='Change the current working directory.')
    args = parser.parse_args()

    cwd = args.cwd
    if not os.path.isdir(cwd):
        print(f"Error: Directory '{cwd}' does not exist.")
        sys.exit(1)
    # Get absolute path
    cwd_abs = os.path.abspath(cwd)
    root_name = '/' + os.path.basename(cwd_abs)

    root_node = RootNode(root_name, cwd_abs)
    root_node.mount()
    root_node.print()

if __name__ == '__main__':
    main()
