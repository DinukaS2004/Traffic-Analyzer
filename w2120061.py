# Author: Dinuka Samarasinghe
# Date: 26.11.2024
# Student ID: 20240624

import csv
# Task A: Input Validation
def is_leap_year(year):
    """
    Checks if the given year is a leap year.
    Reference: https://www.geeksforgeeks.org/python-program-to-check-leap-year/
    Args:
        year (int): The year to check if it is a leap year or not.
    Returns:
        bool: True if the year is a leap year, False if the year is not a leap year.
    """
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False

def validate_date_input():
   """
   Prompts the user to enter a valid date in the format DD/MM/YYYY
   Returns:
        tuple: (day, month, year) which represent validated date
   """
   # Loop until the user enters a valid date
   while True:
       try:
           day = int(input("Please enter the day of the survey in the format DD : "))
           if (day < 1 or day > 31):
               print("Out of range - values must be in the range 1 and 31")
               continue
       except ValueError:
           print("Integer required")
           continue
       else:
           break
       
   # Loop until the user enters a valid month 
   while True:
       try:
           month = int(input("Please enter the month of the survey in the format MM : "))
           if (month < 1 or month > 12):
               print("Out of range - values must be in the range 1 to 12")
               continue
       except ValueError:
           print("Integer required")
           continue
       else:
           break
       
   # Loop until the user enters a valid year 
   while True:
       try:
           year = int(input("Please enter the year of the survey in the format YYYY : "))
           if (year < 2000 or year > 2024):
               print("Out of range - values must be in the range 2000 to 2024")
               continue
       except ValueError:
           print("Integer required")
           continue
       else:
           break
    
   leap_year = is_leap_year(year)
    
   # Define the number of days in each month
   # Refference: https://docs.python.org/3/tutorial/datastructures.html#dictionaries 
   days_of_months = {
       1: 31,2: 29 if leap_year else 28,3: 31,4: 30,5: 31,6: 30,7: 31,8: 31,9: 30,10: 31,11: 30,12: 31
   }

   if day > days_of_months[month]:
       print(f"The day {day} is not valid for the month {month} in the year {year}. Please enter a valid date.")
       return validate_date_input()
   return day, month, year

# Get date as an input from user 
    
def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    Returns:
        str: 'y' if the user wants to continue, 'n' if the user wants to exit.
    """
    print("")
    continue_input = input("Do you want to select another data file for a different date? Y/N : ").lower()
    while True:
        if continue_input == "y" or continue_input == "n" :
            return continue_input
        else:
            continue_input = input("Please enter “Y” or “N”")
            
# Task B: Processed Outcomes
def process_csv_data(file_name):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    Args:
        file_name (str): The name of the CSV file to process
    Returns:
        list: A list of strings containing the processed outcomes
    Raises:
        FileNotFoundError: If the file is not found
    Refference: https://docs.python.org/3/library/csv.html
    """
    outcomes = []
    total_vehicles = 0
    total_trucks = 0
    total_electric_vehicles = 0
    total_two_wheeled_vehicles = 0
    total_buses_elm_to_north = 0
    total_vehicles_no_turns = 0
    total_vehicles_over_speed_limit = 0
    total_vehicles_elm = 0
    total_vehicles_hanley = 0
    total_scooters_elm = 0
    total_bikes = 0
    rain_hours = set()
    total_rain_hours = 0
    vehicles_per_hour_hanley = {}
    vehicles_per_hour_elm = {}
    
    
    try:
        # open csv file and read data
        with open (file_name,"r") as file: 
            reader = csv.DictReader(file)
            for row in reader:
                vehicle_type = row.get("VehicleType", "").lower()
                electric_hybrid = row.get("elctricHybrid", "").lower()
                junction_name = row.get("JunctionName", "").lower()
                travel_direction_in = row.get("travel_Direction_in", "").lower()
                travel_direction_out = row.get("travel_Direction_out", "").lower()
                vehicle_speed = int(row.get("VehicleSpeed", 0))
                junction_speed_limit = int(row.get("JunctionSpeedLimit", 0))
                time_of_day = row.get("timeOfDay", "")
                weather_conditions = row.get("Weather_Conditions", "").lower()

                # Extract the hour from time_of_day
                hour = time_of_day[:2] if time_of_day else None

                # Calculate total vehicle count
                total_vehicles += 1

                # Vehicle type-based counting
                if "truck" in vehicle_type:
                    total_trucks += 1
                if vehicle_type in ["motorcycle", "bicycle", "scooter"]:
                    total_two_wheeled_vehicles += 1
                if vehicle_type == "bicycle":
                    total_bikes += 1

                # Electric/hybrid vehicle count
                if electric_hybrid == "true":
                    total_electric_vehicles += 1

                # Specific conditions
                if "buss" in vehicle_type and travel_direction_out == "n" and junction_name == "elm avenue/rabbit road":
                    total_buses_elm_to_north += 1

                # Vehicles not making turns
                if travel_direction_in == travel_direction_out:
                    total_vehicles_no_turns += 1

                # Vehicles exceeding speed limit
                if vehicle_speed > junction_speed_limit:
                    total_vehicles_over_speed_limit += 1

                # Junction-specific vehicle counts
                if junction_name == "elm avenue/rabbit road":
                    total_vehicles_elm += 1
                if vehicle_type == "scooter" and junction_name == "elm avenue/rabbit road":
                    total_scooters_elm += 1
                if junction_name == "hanley highway/westway":
                    total_vehicles_hanley += 1
                    
                # Track frequency per hour from Elm & Hanley juctions
                if junction_name == "hanley highway/westway" and hour:
                    if hour not in vehicles_per_hour_hanley:
                        vehicles_per_hour_hanley[hour] = 0
                    vehicles_per_hour_hanley[hour] += 1
                    
                if junction_name == "elm avenue/rabbit road" and hour:
                    if hour not in vehicles_per_hour_elm:
                        vehicles_per_hour_elm[hour] = 0
                    vehicles_per_hour_elm[hour] += 1

                # Rainy weather condition tracking
                if weather_conditions in ["heavy rain", "light rain"] and hour:
                    rain_hours.add(hour)
            
            # Average number of bikes per hour
            avg_bikes_per_hour = round(total_bikes /24)

            # Percentage of total vehicles that are trucks
            trucks_percentage = round((total_trucks / total_vehicles) * 100)

            # Percentage of vehicles through Elm Avenue/Rabbit Road that are scooters
            scooters_percentage = round((total_scooters_elm / total_vehicles_elm) * 100)

            # Total rain hours calculation
            total_rain_hours = len(rain_hours) 
                    
            # Calculate the highest number of vehicles per hour on Hanley Highway/Westway
            highest_hour = max(vehicles_per_hour_hanley, key=vehicles_per_hour_hanley.get)
            highest_count = vehicles_per_hour_hanley[highest_hour]
            
            # Calculate the time range with the highest number of vehicles
            start_time = f"{highest_hour}:00"
            # Define the hour and format as two digits
            # Refference: https://docs.python.org/3/library/stdtypes.html#str.zfill
            end_hour = str(int(highest_hour) + 1).zfill(2)

            end_time = f"{end_hour}:00"
            highest_time_range = f"{start_time} and {end_time}"
            highest_time = f"{start_time}-{end_time}"
            
            outcomes = [
                (f"Data file selected is {file_name}"),
                (f"The total number of vehicles recorded for this date is {total_vehicles}"),
                (f"The total number of trucks recorded for this date is {total_trucks}"),
                (f"The total number of electric vehicles recorded for this date is {total_electric_vehicles}"),
                (f"The total number of two wheeled vehicles recorded for this date is {total_two_wheeled_vehicles}"),
                (f"The total number of busses leaving Elm Avenue/Rabbit Road heading North is {total_buses_elm_to_north}"),
                (f"The total number of vehicles through both junctions not turning left or right is {total_vehicles_no_turns}"),
                (f"The percentage of total vehicles recorded that are trucks for this date is {trucks_percentage}%"),
                (f"The average number of bikes per hour for this date is {avg_bikes_per_hour}"),
                (f"The total number of vehicles recorded as the speed limit for this date is {total_vehicles_over_speed_limit}"),
                (f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {total_vehicles_elm}"),
                (f"The total number of vehicles recorded through Hanley Highway/Westway junction is {total_vehicles_hanley}"),
                (f"{scooters_percentage}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters"),
                (f"The highest number of vehicles in an hour on Hanley Highway/Westway is {highest_count}"),
                (f"The most vehicles through Hanley Highway/Westway were recorded between {highest_time}"),
                (f"The number of hours of rain for this date is {total_rain_hours}")
                ]
            display_outcomes(outcomes)
            save_results_to_file(outcomes)
            
            # Ensure all hours (00 to 23) are included in the lists, even if the count is 0
            vehicles_per_hour_elm_list = [vehicles_per_hour_elm.get(f"{hour:02d}", 0) for hour in range(24)]
            vehicles_per_hour_hanley_list = [vehicles_per_hour_hanley.get(f"{hour:02d}", 0) for hour in range(24)]
            
            return vehicles_per_hour_elm_list, vehicles_per_hour_hanley_list
        
    except FileNotFoundError:
        print(f"The file {file_name} was not found...")


def display_outcomes(outcomes):
    """
    Displays the calculated outcomes in a clear and formatted way.
    Args:
        outcomes (list): A list of strings containing the processed outcomes   
    """
    for value in outcomes:
        print(value)
    

# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    Args:
        outcomes (list): A list of strings containing the processed outcomes
        file_name (str): The name of the file to save the outcomes.
    """
    try:
        with open(file_name, 'a') as file:
            for outcome in outcomes:
                file.write(outcome + "\n")
            file.write("\n")
            file.write("============================================================================")
            file.write("\n\n")
    except PermissionError:
        print("")
        print("Permission required to write data to file")
    except Exception as e:
        print(e)
        
# if you have been contracted to do this assignment please do not remove this line

# Task D: Histogram Display
import tkinter as tk
class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        Args:
            traffic_data (tuple) : A tuple containing two lists of vehicle frequencies per hour for two locations
            date (str) : The date for traffic data
        """
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.canvas = None  # Will hold the canvas for drawing

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        Configure title,size, properties of the window
        """
        self.root.title("Histogram for Vehicle Frequency per Hour")
        canvas_width = 1200
        canvas_height = 510

        # Set the window size and make it non-resizable
        self.root.geometry(f"{canvas_width}x{canvas_height}")
        self.root.resizable(False, False)

        # Ensure the window pops up on top
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))

        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg="#EDF1ED")
        self.canvas.pack()

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        elmlst, hanlst = self.traffic_data
        max_frequency = max(max(elmlst), max(hanlst))

        # Chart dimensions
        chart_start_y = 125
        chart_start_x = 50
        chart_end_y = 450
        chart_end_x = 1123
        max_height = chart_end_y - chart_start_y

        # Bar dimensions and gap
        bar_width = 18
        bar_gap = 27

        # Check if max_frequency is zero to avoid division by zero
        if max_frequency == 0:
            self.canvas.create_text(683.5, 250, text="No data available to display", font=("Arial", 15, "bold"), fill="#50524F", anchor="center")
            return

        # Drawing bars for Elm Avenue/Rabbit Road
        bar_x_start = chart_start_x
        for i in elmlst:
            bar_height = (i / max_frequency) * max_height
            self.canvas.create_rectangle(bar_x_start, chart_end_y - bar_height, bar_x_start + bar_width, chart_end_y, fill="#9FF697", outline="#53AD4B", width=1)
            self.canvas.create_text(bar_x_start + bar_width / 2, chart_end_y - bar_height - 10, text=f"{i}", font=("Arial", 10, "bold"), fill="#50AE56", anchor="center")
            bar_x_start += bar_width + bar_gap

        # Drawing bars for Hanley Highway/Westway
        bar_x_start = chart_start_x + bar_width + 1
        for i in hanlst:
            bar_height = (i / max_frequency) * max_height
            self.canvas.create_rectangle(bar_x_start, chart_end_y - bar_height, bar_x_start + bar_width, chart_end_y, fill="#F99794", outline="#C7635F", width=1)
            self.canvas.create_text(bar_x_start + bar_width / 2, chart_end_y - bar_height - 10, text=f"{i}", font=("Arial", 10, "bold"), fill="#DD7663", anchor="center")
            bar_x_start += bar_width + bar_gap

        # Drawing the chart baseline
        self.canvas.create_line(chart_start_x, chart_end_y, chart_end_x, chart_end_y, fill="#5E5E5C", width=1)

        # Adding hours labels
        text_x_point = chart_start_x + bar_width / 2 + bar_gap / 2.5
        for i in range(24):
            self.canvas.create_text(text_x_point, 460, text=f"{int(i):02d}", font=("Arial", 10, "bold"), fill="#60625F", anchor="center")
            text_x_point += bar_width + bar_gap

        # Adding base text
        self.canvas.create_text(600, 490, text="Hours 0:00 to 24:00", font=("Arial", 10, "bold"), fill="#60625F", anchor="center")

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        This creates specific colored rectangles and texts to represent vehicle frequency data
        """
        bar_width = 18
        self.canvas.create_text(50, 25, text=f"Histogram of Vehicle Frequency per Hour ({self.date})", font=("Arial", 15, "bold"), fill="#50524F", anchor="w")
        self.canvas.create_rectangle(50, 45, 50 + bar_width, 70, fill="#9FF697", outline="#53AD4B", width=1)
        self.canvas.create_text(55 + bar_width, 57.5, text="Elm Avenue/Rabbit Road", font=("Arial", 10, "bold"), fill="#60625F", anchor="w")
        self.canvas.create_rectangle(50, 75, 50 + bar_width, 100, fill="#F99794", outline="#C7635F", width=1)
        self.canvas.create_text(55 + bar_width, 87.5, text="Hanley Highway/Westway", font=("Arial", 10, "bold"), fill="#60625F", anchor="w")

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        This set up the window, add the legend, draws the histogram, and starts the main event loop of the tkinter application
        """
        self.setup_window()
        self.add_legend()
        self.draw_histogram()
        self.root.mainloop()
        
# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the MultiCSVProcessor to handle loading and processing of multiple CSV files.
        Attributes:
        current_data (list): Holds the currently loaded traffic data.
        """
        self.current_data = None

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        Parameters:
            file_path (str): The path to the CSV file to be loaded.
        Returns:
            list: The processed data from the CSV file, or None if the file was not found.
        """
        try:
            self.current_data = process_csv_data(file_path)
            return self.current_data
        except FileNotFoundError:
            print(f"The file {file_path} was not found. Please check the file name and try again.")
            self.current_data = None

    def clear_previous_data(self):
        """
        Clears the previously loaded data.
        This method resets the current_data attribute to None and prints a confirmation message.
        """
        self.current_data = None
        print("Previous data cleared.")

    def handle_user_interaction(self):
        """
        Handles user interaction for loading CSV files and displaying histograms.
        This method prompts the user for date input, constructs the file name,
        loads the data, and displays the histogram if data is available.
        """
        while True:
            day, month, year = validate_date_input()
            print("")
            date = f"{day:02d}{month:02d}{year}"
            file_name = f"traffic_data{date}.csv"
            print("")
            
            self.load_csv_file(file_name)
            if self.current_data:
                histogram_app = HistogramApp(self.current_data, date)
                histogram_app.run()
            
            continue_input = validate_continue_input()
            print("")
            if continue_input == 'n':
                print("End of Run")
                break
            else:
                self.clear_previous_data()
            print("")

    def process_files(self):
        """
        Initiates the process of handling multiple CSV files.
        This method starts the user interaction loop for loading and processing traffic data files.
        """
        self.handle_user_interaction()

def main():
    """
    Main function to execute the MultiCSVProcessor.
    This function creates an instance of MultiCSVProcessor and starts the file processing.
    """
    processor = MultiCSVProcessor()
    processor.process_files()

if __name__ == "__main__":
    main()
    