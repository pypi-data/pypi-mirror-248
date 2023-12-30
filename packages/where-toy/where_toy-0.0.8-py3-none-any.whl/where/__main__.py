""" Utility to locate python modules from the command line """

import sys
import argparse

from .utils import where_module


def main():
    parser = argparse.ArgumentParser(description=__doc__, prog='python -mwhere')
    parser.add_argument('-t', '--tree', action='store_true', help="print package contents as a tree")
    parser.add_argument('module', help="module or package name")

    options = parser.parse_args()

    if not where_module(
            options.module,
            tree=options.tree):
        sys.exit(1)


if __name__ == "__main__":
    main()
