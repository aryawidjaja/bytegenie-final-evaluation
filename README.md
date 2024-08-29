# ByteGenie Second Test Solutions⚡️- Mutaqin Aryawijaya

## Overview

This repository contains the solutions for Problems 1, 2, and 3 as described in the provided test. The solutions are structured into separate directories (`problem1`, `problem2`, and `problem3`) for easy navigation and execution. Each problem addresses a specific task involving data filtering, querying from a PostgreSQL database, and improving LLM-generated SQL queries.

## What's Inside

- **`problem1/`**: Solution for Problem 1, focusing on filtering interconnected dataframes.
- **`problem2/`**: Solution for Problem 2, which involves querying a PostgreSQL database based on dynamic filters.
- **`problem3/`**: Explanation for Problem 3 on how to improve LLM-generated SQL queries.

## How to Run the Solutions

### Create and Activate a Virtual Environment
Before running the solutions, it's recommended to use a virtual environment:

1. **Create a virtual environment**:
    ```sh
    python -m venv venv
    ```

2. **Activate the virtual environment**:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```
3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

### Problem 1

To run the solution for Problem 1:

1. **Set Up the Environment**:
   - Navigate to the `problem1` directory:
     ```sh
     cd problem1
     ```

2. **Run the Filtering Function**:
   - Run the `data_filter.py` script to test the filtering functionality with the provided dummy data:
     ```sh
     python data_filter.py
     ```

   The script will execute and display the filtered data based on the conditions specified in the code.

### Problem 2

To run the solution for Problem 2:

1. **Set Up the PostgreSQL Database**:
   - Ensure you have PostgreSQL installed and running on your local machine.
   - Create a database named `bytegenie_db` and populate it with the necessary tables and data as specified in the code and example CSV files.

2. **Navigate to the `problem2` Directory**:
   - Navigate to the `problem2` directory:
     ```sh
     cd problem2
     ```

3. **Run the Querying Function**:
   - Run the `query_data.py` script to execute the dynamic SQL queries and see the results based on the input filters:
     ```sh
     python query_data.py
     ```

   The script will connect to the PostgreSQL database, apply the filters, and return the results in a DataFrame format.

### Problem 3

Problem 3 is a conceptual explanation and does not require code execution. The answer for this problem is written in `problem3/solution.md`

