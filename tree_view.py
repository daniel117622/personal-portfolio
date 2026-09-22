#!/usr/bin/env python3
"""
AI Agent Context Utility: Python File Summarizer

This script parses a Python file and prints a high-level tree view of its 
structural components (classes, methods, and top-level functions). 

Purpose: To easily share the architectural outline of a module with AI agents 
(like LLMs) while significantly reducing context size and saving tokens.
"""

import ast
import sys

def print_tree(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    print(f"📄 {filepath}")
    
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            print(f"├── class {node.name}:")
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    print(f"│   ├── def {child.name}(...)")
        elif isinstance(node, ast.FunctionDef):
            print(f"├── def {node.name}(...)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_tree.py <file.py>")
    else:
        print_tree(sys.argv[1])