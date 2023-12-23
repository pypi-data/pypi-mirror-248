import argparse
import ast
import textwrap
import os

class TestGenerator:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tree = ast.parse(source_code)

    def generate_tests(self):
        tests = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                test = self.generate_test(node)
                tests.append(test)
        return tests

    def generate_test(self, function_node):
        # Generate a test that calls the function with different arguments
        # and checks the return value
        test_code = textwrap.dedent(f"""
            def test_{function_node.name}():
                # Call the function with different arguments
                try:
                    result = {function_node.name}(1, 2)
                    assert result == 3, f"Expected 3, but got {{result}}"
                    result = {function_node.name}(0, 0)
                    assert result == 0, f"Expected 0, but got {{result}}"
                    result = {function_node.name}(-1, -2)
                    assert result == -3, f"Expected -3, but got {{result}}"
                except Exception as e:
                    assert False, f"Function {function_node.name} raised an exception: {{e}}"
        """)
        return test_code

def main():
    parser = argparse.ArgumentParser(description='Generate tests for a Python file.')
    parser.add_argument('filename', help='The Python file to generate tests for')
    args = parser.parse_args()

    try:
        with open(args.filename, 'r') as file:
            source_code = file.read()
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error opening file: {e}")
        return

    try:
        test_generator = TestGenerator(source_code)
        tests = test_generator.generate_tests()
    except SyntaxError as e:
        print(f"Error parsing Python code: {e}")
        return

    # Write the tests to a file
    try:
        with open('test_generated.py', 'w') as file:
            # Add import statements
            file.write(f"import pytest\nimport {os.path.splitext(args.filename)[0]}\n\n")
            file.write('\n'.join(tests))
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error writing to file: {e}")
        return

if __name__ == "__main__":
    main()