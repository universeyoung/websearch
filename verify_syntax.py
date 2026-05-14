#!/usr/bin/env python3
"""Verification script to check code syntax"""

import ast
import sys
from pathlib import Path


def verify_python_syntax(file_path: Path) -> tuple[bool, str]:
    """Verify Python file syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source)
        return True, "OK"
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    """Main verification function"""
    project_root = Path(__file__).parent
    python_files = list(project_root.rglob("*.py"))

    print("Verifying Python syntax...")
    print(f"Found {len(python_files)} Python files\n")

    all_ok = True
    for file_path in python_files:
        if '__pycache__' in str(file_path):
            continue

        rel_path = file_path.relative_to(project_root)
        ok, message = verify_python_syntax(file_path)

        status = "✓" if ok else "✗"
        print(f"{status} {rel_path}: {message}")

        if not ok:
            all_ok = False

    print("\n" + "=" * 50)
    if all_ok:
        print("✓ All Python files have valid syntax")
        return 0
    else:
        print("✗ Some files have syntax errors")
        return 1


if __name__ == "__main__":
    sys.exit(main())
