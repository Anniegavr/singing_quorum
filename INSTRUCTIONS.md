# Setup and Run Instructions

## Prerequisites
- Python 3.13 (older version 3.x should also work, but the packages may vary in versions)
- pip (Python package manager)

## Step 1: Clone or Download the Project
Download or clone the project files to your computer.

## Step 2: Install Dependencies
Open a terminal (PowerShell) in the project directory and run:

```
pip install -r requirements.txt
```
If you want to check the version of the installed packages, you can run (for example):

```
pip show pandas | findstr Version
```

This will install the required packages (pip, pandas).

## Step 3: Prepare Data Files
Ensure the following CSV files are present in the `data/` folder:
- bills.csv
- legislators.csv
- vote_results.csv
- votes.csv

## Step 4: Run the Main Script
In the terminal, run:

```
python main.py
```

## Step 5: View Output
Output files will be generated in the `output/` folder:
- bills.csv
- legislators-support-oppose-count.csv

## Step 6: Run Automated Tests
To verify the code works correctly, run the automated tests:

```
pytest -s tests/test_main.py
```

The `-s` flag ensures you see detailed output in the terminal. The tests will:
- Show the input data used for each test case
- Show the expected output for that input
- Show the actual output produced by the code
- Compare the actual output to the expected output

If all tests pass, you will see output like:
```
Input: ...
Expected output: ...
Actual output: ...
.
```
This means the code produces the correct results for the sample inputs. If a test fails, you will see an error message explaining the mismatch.

## Troubleshooting
- If you see errors about missing packages, re-run the pip install command.
- Make sure your terminal is in the project directory before running commands.
- If you encounter permission errors, try running the terminal as administrator.



