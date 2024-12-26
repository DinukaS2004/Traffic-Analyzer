# 🚗 Traffic Data Analysis Project

Welcome to the Traffic Data Analysis Project! This project involves analyzing traffic data to provide insightful metrics about vehicle frequencies, types, and behaviors at different junctions.

## 📋 Project Overview

This project processes CSV files containing traffic data to:
- Validate date inputs
- Process and analyze vehicle data
- Display histograms of vehicle frequencies per hour

## 📂 File Structure

- `w2120061.py`: Main script for processing traffic data and generating histograms.
- `results.txt`: File where processed outcomes are saved.

## 🛠️ Usage

1. **Run the Script:**
   ```sh
   python w2120061.py
- Follow the Prompts:
Enter the date of the survey when prompted.\
Select a CSV file with the traffic data for the entered date.
## 📊 Features
- Input Validation: Ensures that the date input is valid.
- CSV Data Processing: Extracts and processes data from the CSV files.
- Histogram Display: Visual representation of vehicle frequencies per hour using Tkinter.
## 🧩 Code Details
#### validate_date_input()
Validates user input for the date in DD/MM/YYYY format, ensuring the date is within the allowed range and checks if the year is a leap year.

#### process_csv_data(file_name)
Processes the CSV data to extract various metrics such as total vehicles, total trucks, electric vehicles, and more. Displays outcomes and saves results to a text file.

#### HistogramApp
A Tkinter-based class that creates and displays histograms for vehicle frequencies per hour at different junctions.

#### MultiCSVProcessor
Handles multiple CSV file inputs and processes them iteratively based on user interaction.

## 📚 Documentation
For detailed information on how the code works, please refer to the docstrings within the w2120061.py file.

## 🌟 Acknowledgements
#### References:
GeeksforGeeks: Check Leap Year\
Python CSV Documentation
## 🧑‍💻 Author
Dinuka Samarasinghe
