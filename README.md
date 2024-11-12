# Unitape - Automated UnitTest Generator

Unitape is a Python-based utility that automatically generates unit tests for classes in Python source files. It analyzes the specified source files and creates `unittest` files for each detected class, saving them as separate `.py` files. The paths for both the source and output directories are configurable via a command-line interface (CLI).

## Features

- Automatically detects classes in Python files and generates corresponding unit test templates.
- Supports both directories and individual Python files as source inputs.
- Outputs separate unit test files for each class found.
- CLI-based interface for setting paths and generating tests.

## Installation

No special installation is needed for Unitape. Simply ensure you have Python installed on your system (version 3.x recommended).

## Usage

1. Clone or download this repository.
2. Open a terminal and navigate to the folder containing `unitape.py`.
3. Run the script using Python:

   ```bash
   python unitape.py
