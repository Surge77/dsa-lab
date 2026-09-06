# Python Environment and Project Setup Guide

## Project Setup (setup.py)

The `setup.py` file in this project serves several important purposes:

### What the Setup File Does

1. **Package Management**
   - Uses `setuptools` to make our code installable as a Python package
   - Automatically discovers all packages using `find_packages()`
   - Makes the code importable from anywhere in your system once installed

2. **Project Metadata**
   ```python
   name="dsa_lab"      # Package name used for installation
   version="0.1"                # Project version for tracking updates
   packages=find_packages()     # Automatically finds all Python packages
   install_requires=[]          # List project dependencies here
   ```

3. **Author Information**
   - Includes author name and contact information
   - Provides project description and keywords
   - Helps with package distribution and documentation

### Why We Need It

1. **Proper Import Structure**
   - Enables Python to find and import modules correctly
   - Maintains clean import statements in code
   - Prevents import-related issues when running tests

2. **Development Benefits**
   - Makes the project installable in "editable" mode (`pip install -e .`)
   - Ensures consistent behavior across different environments
   - Simplifies dependency management

## Environment PATH Setup

### Why Configure PATH?

1. **Module Accessibility**
   - Allows Python to find your project modules
   - Enables imports from any directory
   - Prevents "ModuleNotFoundError" issues

2. **Test Execution**
   - Ensures tests can import project modules
   - Maintains consistent import paths
   - Simplifies test organization

### How to Configure PATH

1. **Temporary Method (Command Line)**
   ```powershell
   # Windows PowerShell
   $env:PYTHONPATH = "C:\Users\tdmne\Desktop\experiments\dsa-lab"
   ```

2. **Permanent Method (System Environment)**
   - Open System Properties → Advanced → Environment Variables
   - Add/Edit PYTHONPATH variable
   - Add project root path: `C:\Users\tdmne\Desktop\experiments\dsa-lab`

3. **Using .env File (Development)**
   ```env
   PYTHONPATH=C:\Users\tdmne\Desktop\experiments\dsa-lab
   ```

### Best Practices

1. **Virtual Environment**
   - Create a virtual environment for isolation:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate
     ```
   - Install project in editable mode:
     ```powershell
     pip install -e .
     ```

2. **Import Structure**
   - Use absolute imports in your code
   - Example:
     ```python
     from dsa_lab.data_structures import BinaryTree
     ```
   - Avoid relative imports when possible

3. **Testing**
   - Run tests from project root
   - Use pytest's module import mechanism
   - Keep test files in dedicated test directory

## Common Issues and Solutions

1. **ModuleNotFoundError**
   - Verify PYTHONPATH includes project root
   - Check virtual environment activation
   - Ensure proper import statements

2. **Import Issues**
   - Use absolute imports
   - Verify package installation (`pip list`)
   - Check file/directory structure

3. **Test Discovery Problems**
   - Run tests from project root
   - Use correct pytest command format
   - Verify test file naming convention
