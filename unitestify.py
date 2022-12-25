import ast
import click

UNITTEST_TYPES = {
    "unittest": {
        "import": "import unittest",
        "class": "unittest.TestCase",
    }, 
    "django": {
        "import": "from django.test import TestCase",
        "class": "TestCase",
    }
}

# 4 Spaces
SPACES = 5

@click.command()
@click.option("--file", help="Path to file from which to generate test file")
@click.option("--type", default="unittest", help="Type of test to generate")
def unitestify(file: str, type: str):
    """Unitestify command line arguments."""    
    if not file:
        click.echo("Path to file is required")
        return
    
    test = type.lower()
    test_type = UNITTEST_TYPES.get(test, {})
    definitions = parse_file(file)
    create_test_file(definitions, file, test_type)

def create_base(class_name: str, test_type):
    """Create imports and class to inherit from."""
    cls_name = f"Test{class_name}"
    test_definition = f"class {cls_name}({test_type['class']}):"
    test_class_docstring = "\n".ljust(SPACES ) + f'"""{cls_name}."""\n'
    import_statements = f"{test_type['import']}\n\n"
    definitions = [import_statements, test_definition, test_class_docstring]
    return "".join(definitions)

def parse_file(file_name: str):
    """Parser file and get module definitions."""
    definitions = {}
    with open(file_name, encoding="utf-8") as file:
        tree = ast.parse(file.read())

    class_methods = []
    # Iterate over the nodes in the AST
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_args = node.args.args
            method_data = {node.name : {}}
            
            for arg in func_args:
                arg_type = arg.annotation
                method_data[node.name] = {
                    "type": arg_type.id if arg_type else None,
                    "argument": arg.arg
                }
   
            class_methods.append(method_data)   
  
        if isinstance(node, ast.ClassDef):
            definitions["class"] = node.name

    definitions["functions"] = class_methods
    return definitions


def create_test_file(definitions: dict, file_name: str, test_type: dict):
    class_name = definitions.get("class", "")
    class_methods = definitions.get("functions", {})
    filename = f"test_{file_name}"
    test_definition = create_base(class_name, test_type)

    for method in class_methods:
        for method_name, _ in method.items():
            parts = method_name.split("_")
            docstring = f'"""Test {" ".join(parts)}."""'
            test_definition += "\n".ljust(SPACES)
            test_definition += f"def test_{method_name}(self):".ljust(SPACES)
            test_definition += "\n".ljust(SPACES + 4)
            test_definition += docstring
            test_definition += "\n".ljust(SPACES + 4)
            
        with open(filename, "w", encoding="utf-8") as file:
            file.write(test_definition)
