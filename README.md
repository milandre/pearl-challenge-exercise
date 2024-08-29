# Homeowners and Neighborhoods

This is a coding exercise that involves assigning home buyers to neighborhoods. You can find the problem specifications in the PDF file located in the `assets` folder.

## Requirements

- Python 3.11+ (https://www.python.org/downloads/)
- Pytest (https://docs.pytest.org/en/stable/getting-started.html)
- Pipenv (https://pipenv.pypa.io/en/latest/#install-pipenv-today) (Optional: Use a virtual environment)

## Setup

To test the solution, you will need to execute the following command:

```console
python3 app/main.py <input_file> <output_file>
```

Replace `input_file` and `output_file` with the appropriate file paths for input and output. There is a sample input file to start with in `assets/inputs/case0.txt`.

If you are going to use `pipenv`, remember to install the requirements and activate it.

## Test

Run the tests with the following command in the root folder of the project:

```
pytest
```

## Test Cases

In the `scripts` folder, there is a file called `generate_test_cases.sh` that can be used to create input file cases and run tests. The input and output files will be placed in the `assets/inputs/` and `assets/outputs/` folders, respectively.

To use the script, simply run the following command:

```bash
./scripts/generate_test_cases.sh
```
