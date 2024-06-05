#!/usr/bin/python3
"""
:file: main.py
:brief: CLI entry point for the input/output apps for the Karaoke project
:author: Joseph Smith
"""

import sys

if __name__ == '__main__':
    mode = sys.argv[1]

    if mode == 'input':
        import input
        app = input.App()
    elif mode in ['output', 'search']:
        import output
        app = output.App()
    else:
        print("Invalid argument")
        print("Usage: python3 main.py [input|output|search]")
        exit(0)

    app.run()