# UIC Grade Data Analyzer

## Description

This program is designed to analyze and visualize grade distribution data of various courses offered at the University of Illinois Chicago (UIC). The purpose is to assist students in making informed decisions regarding course and professor selections by providing insights based on historical grading data. By evaluating the grading trends, pass rates, and withdrawal rates, students can choose courses and instructors that align best with their academic goals.

## Features

- **Course Search:** Users can search for courses by course code and number, professor's name, or department.
- **Grade Distribution Visualization:** The program generates bar graphs visualizing the grade distribution (A, B, C, D, F) for each searched course.
- **Performance Metrics:** For each course, the program calculates and displays metrics such as:
  - Average letter grade
  - Pass rate
  - Fail rate
  - Withdrawal rate

## Usage Instructions

1. **Setup:**
    - Ensure that you have the necessary modules installed: `pandas` and `matplotlib`.
    - Place the CSV files containing the UIC grade data in a specific directory.
    - Ensure that the CSV files are named in the following format: `SEMESTER YEAR.csv` (e.g. `Fall 2023.csv`).
    - Update CSV_PATH in `main.py` to the path of the directory containing the CSV files.

2. **Execution:**
    - Run the program.
    - You'll be prompted to enter the Course Subject Code and Course Number.
    - The program will then display the results in the console and save grade distribution bar graphs as PNG files in the specified directory.

3. **Example:**
   ```bash
   Enter Course Subject Code: CS
   Enter Course Number: 100
   ```

## Code Structure

- `CSV`: A class that represents a CSV file. It includes methods to retrieve the year and semester and to convert the file into a dataframe.
- `Parser`: Handles the parsing of all CSV files and mounts the data into appropriate data structures.
- `Search`: Facilitates various search operations, such as searching by course code, professor, or department.
- `Course`: Represents a course with various attributes like course title, professor, and grade distributions. Includes methods to calculate various performance metrics and to generate grade distribution visualizations.

## Customization

- The output paths for images and the source directory for CSV files are configurable.
- Users can add more search functionalities or metrics as per their needs.

## Disclaimer

The data utilized by this program is based on public records from UIC. The tool aims to assist in making academic decisions and does not guarantee any specific outcomes in the courses analyzed. Users are encouraged to consider multiple factors, including personal interests and strengths, when selecting courses and instructors.

---

Enjoy exploring and choosing the best courses to enrich your academic journey at UIC! 📚📊