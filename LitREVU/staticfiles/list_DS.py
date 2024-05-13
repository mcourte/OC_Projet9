import os
import re


project_directory = "LitREVU"


def extract_functions_with_docstrings(directory):
    function_pattern = re.compile(r'def\s+([^\(]+)\(([^)]*)\)\s*:\s*("""(.*?)""")?', re.DOTALL)

    functions = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = function_pattern.findall(content)
                    for match in matches:
                        function_name = match[0]
                        docstring = match[3] if match[3] else "No docstring"
                        functions.append((file, function_name, docstring))

    return functions


def write_functions_to_file(functions, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for file, function_name, docstring in functions:
            f.write(f"File: {file}\n")
            f.write(f"Function: {function_name}\n")
            f.write(f"Docstring: {docstring}\n\n")


output_file = os.path.join(project_directory, "docstrings.txt")
functions = extract_functions_with_docstrings(project_directory)
test = write_functions_to_file(functions, output_file)
