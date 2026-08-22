import ast
import pathlib
import sys

def test_no_duplicate_keys_in_translation_mappings():
    """Ensure translation_mappings.py has ZERO duplicate keys in all dictionaries."""
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    mappings_file = repo_root / "translation_mappings.py"
    
    source = mappings_file.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(mappings_file))

    target_dicts = {"PHRASE_MAPPINGS", "CONJUNCT_RULES", "GLOBAL_CORRECTIONS", "EDITORIAL_CORRECTIONS"}

    def ast_to_repr(node):
        if isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Tuple):
            return f"({', '.join(ast_to_repr(elt) for elt in node.elts)})"
        elif isinstance(node, ast.Call):
            return f"call({node.func.id if isinstance(node.func, ast.Name) else 'func'})"
        return ast.dump(node)

    all_duplicates = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name) and target.id in target_dicts:
                    dict_name = target.id
                    if isinstance(node.value, ast.Dict):
                        seen = {}
                        for k_node, _ in zip(node.value.keys, node.value.values):
                            k_repr = ast_to_repr(k_node)
                            if k_repr in seen:
                                all_duplicates.append(
                                    f"[{dict_name}] Duplicate key '{k_repr}' at line {k_node.lineno} (first seen at line {seen[k_repr]})"
                                )
                            else:
                                seen[k_repr] = k_node.lineno

    assert not all_duplicates, "Found duplicate keys in translation_mappings.py:\n" + "\n".join(all_duplicates)
