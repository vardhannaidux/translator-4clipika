# -*- coding: utf-8 -*-
"""
audit_duplicates.py — AST-Based Duplicate Key Inspector for Translation Mapping Tables.

Parses translation_mappings.py (or a target mapping file) using Python's AST
to detect duplicate keys in dictionaries such as PHRASE_MAPPINGS, CONJUNCT_RULES,
GLOBAL_CORRECTIONS, and EDITORIAL_CORRECTIONS.
"""

import ast
import argparse
import sys
import pathlib
from typing import Dict, List, Tuple, Set, Any


def ast_to_repr(node: ast.AST) -> str:
    """Converts an AST key node into a human-readable string representation."""
    if isinstance(node, ast.Constant):
        return repr(node.value)
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Tuple):
        return f"({', '.join(ast_to_repr(elt) for elt in node.elts)})"
    elif isinstance(node, ast.Call):
        func_name = node.func.id if isinstance(node.func, ast.Name) else "func"
        return f"call({func_name})"
    return ast.dump(node)


def audit_file_dictionaries(
    file_path: pathlib.Path, target_dicts: Set[str]
) -> Dict[str, List[Tuple[str, int, int]]]:
    """
    Parses the target Python file using AST and checks for duplicate dictionary keys.

    Returns:
        A dictionary mapping table name to a list of (key_repr, first_line, duplicate_line) tuples.
    """
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))

    results = {}

    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name) and target.id in target_dicts:
                    dict_name = target.id
                    if isinstance(node.value, ast.Dict):
                        seen: Dict[str, int] = {}
                        duplicates: List[Tuple[str, int, int]] = []
                        for k_node in node.value.keys:
                            k_repr = ast_to_repr(k_node)
                            if k_repr in seen:
                                duplicates.append(
                                    (k_repr, seen[k_repr], k_node.lineno)
                                )
                            else:
                                seen[k_repr] = k_node.lineno
                        results[dict_name] = (
                            len(node.value.keys),
                            len(seen),
                            duplicates,
                        )

    return results


def main() -> int:
    """Main CLI entry point for duplicate key audit script."""
    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Audit Python dictionary mapping tables for duplicate keys using AST."
    )
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    default_mappings = repo_root / "translation_mappings.py"

    parser.add_argument(
        "-f",
        "--file",
        type=pathlib.Path,
        default=default_mappings,
        help="Path to mapping Python file (default: translation_mappings.py)",
    )

    args = parser.parse_args()

    target_dicts = {
        "PHRASE_MAPPINGS",
        "CONJUNCT_RULES",
        "GLOBAL_CORRECTIONS",
        "EDITORIAL_CORRECTIONS",
    }

    if not args.file.exists():
        print(f"Error: File '{args.file}' does not exist.", file=sys.stderr)
        return 1

    print(f"Auditing dictionary tables in '{args.file.name}'...\n")
    audit_data = audit_file_dictionaries(args.file, target_dicts)

    total_duplicates = 0

    for dict_name, (total_keys, unique_keys, duplicates) in audit_data.items():
        dup_count = len(duplicates)
        total_duplicates += dup_count

        print(f"=== {dict_name} ===")
        print(
            f"Total keys: {total_keys} | Unique keys: {unique_keys} | Duplicates: {dup_count}"
        )

        if duplicates:
            for dup_key, line1, line2 in duplicates:
                print(
                    f"  ❌ Duplicate key: {dup_key} (first seen at line {line1}, duplicate at line {line2})"
                )
        else:
            print("  ✅ Zero duplicate keys found.")
        print()

    if total_duplicates > 0:
        print(
            f"Result: AUDIT FAILED - {total_duplicates} duplicate key(s) detected."
        )
        return 1
    else:
        print("Result: AUDIT PASSED - All mapping dictionaries are 100% unique!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
