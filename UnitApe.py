import os
import ast
import sys

# Author: Hanselaffe
class Unitape:
    def __init__(self):
        self.source_path = ""
        self.output_path = ""

    def main_menu(self):
        while True:
            print("\n*** Unitape - Automated UnitTest Generator ***")
            print("1. Set Source Path")
            print("2. Set Output Path")
            print("3. Generate Unittests")
            print("4. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                self.set_source_path()
            elif choice == "2":
                self.set_output_path()
            elif choice == "3":
                self.generate_unittests()
            elif choice == "4":
                print("Exiting Unitape. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")

    def set_source_path(self):
        path = input("Enter the source path containing Python files (file or directory): ")
        if os.path.isdir(path) or os.path.isfile(path):
            self.source_path = path
            print(f"Source path set to: {path}")
        else:
            print("Invalid path. Please enter a valid directory or file.")

    def set_output_path(self):
        path = input("Enter the output path to save unittest files: ")
        if os.path.isdir(path):
            self.output_path = path
            print(f"Output path set to: {path}")
        else:
            print("Invalid path. Please enter a valid directory.")

    def generate_unittests(self):
        if not self.source_path or not self.output_path:
            print("Source and Output paths must be set before generating unittests.")
            return

        if os.path.isfile(self.source_path):
            # Process a single file
            self.create_unittest_for_file(self.source_path)
        else:
            # Process all files in the directory
            for root, _, files in os.walk(self.source_path):
                for file in files:
                    if file.endswith(".py"):
                        full_path = os.path.join(root, file)
                        self.create_unittest_for_file(full_path)

    def create_unittest_for_file(self, file_path):
        with open(file_path, "r") as file:
            source_code = file.read()

        try:
            parsed_code = ast.parse(source_code)
            classes = [node for node in parsed_code.body if isinstance(node, ast.ClassDef)]

            if not classes:
                print(f"No classes found in file {file_path}. Skipping.")
                return

            for class_node in classes:
                self.create_unittest_file(file_path, class_node)

        except SyntaxError as e:
            print(f"Syntax error in file {file_path}: {e}")

    def create_unittest_file(self, file_path, class_node):
        class_name = class_node.name
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        if module_name == "test":  # Schutz gegen Konflikte mit 'test'
            module_name = "module_test"

        test_filename = f"test_{class_name.lower()}.py"
        output_file_path = os.path.join(self.output_path, test_filename)

        with open(output_file_path, "w") as test_file:
            test_file.write("import unittest\\n")
            test_file.write(f"from {module_name} import {class_name}\\n\\n")
            test_file.write(f"class Test{class_name}(unittest.TestCase):\\n")

            methods = [node for node in class_node.body if isinstance(node, ast.FunctionDef)]
            for method in methods:
                test_file.write(f"\\n    def test_{method.name}(self):\\n")
                test_file.write(f"        # TODO: Implement test for {method.name}\\n")
                test_file.write(f"        self.assertTrue(True)\\n")

        print(f"Generated unittest for class '{class_name}' in file '{output_file_path}'")

if __name__ == "__main__":
    unitape = Unitape()
    unitape.main_menu()
