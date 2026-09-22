#!/usr/bin/env python3
"""
AI Agent Context Utility: Python File Summarizer

This script parses a Python file (or an entire project) and prints a high-level 
tree view of its structural components (classes, methods, and top-level functions). 

Purpose: To easily share the architectural outline of a module with AI agents 
(like LLMs) while significantly reducing context size and saving tokens.
"""

import ast
import sys
import os

# Ignore these directories to save context window tokens
IGNORE_DIRS = {'.git', '__pycache__', 'venv', 'env', '.venv', 'node_modules', '.pytest_cache'}

def print_tree(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            # Skip completely empty files
            if not content.strip():
                return
            tree = ast.parse(content)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    # Check if the file actually has classes or functions to save space
    has_structure = any(isinstance(node, (ast.ClassDef, ast.FunctionDef)) for node in tree.body)
    
    print(f"📄 {filepath}")
    
    if not has_structure:
        # If it's just imports or variables (like an __init__.py), note it compactly
        print("└── (No classes or top-level functions)\n")
        return

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            print(f"├── class {node.name}:")
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    print(f"│   ├── def {child.name}(...)")
        elif isinstance(node, ast.FunctionDef):
            print(f"├── def {node.name}(...)")
            
    print() # Add spacing between files for the AI's readability

def scan_project(root_dir="."):
    """Recursively scan for important .py files."""
    for root, dirs, files in os.walk(root_dir):
        # Mutate the dirs list in-place to prevent os.walk from entering ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        # Sort to ensure deterministic, alphabetical output for the AI
        dirs.sort()
        files.sort()
        
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                
                # Exclude the script itself and auto-generated env files
                if file == "tree_view.py" or file.startswith("."):
                    continue
                    
                # Normalize path for cleaner printing (e.g., remove './')
                clean_path = os.path.normpath(filepath)
                print_tree(clean_path)

if __name__ == "__main__":
    if "--full" in sys.argv:
        scan_project()
    elif len(sys.argv) > 1 and sys.argv[1] != "--full":
        target = sys.argv[1]
        if os.path.isdir(target):
            scan_project(target)
        else:
            print_tree(target)
    else:
        print("Usage:")
        print("  python tree_view.py <file.py>       # Scan a single file")
        print("  python tree_view.py <directory>     # Scan a specific directory")
        print("  python tree_view.py --full          # Scan the entire project recursively")