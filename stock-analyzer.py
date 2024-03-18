import csv
import random
import statistics
import os
import argparse


# Parse the script arguments
parser = argparse.ArgumentParser(description="Analyze stocks in csv format.")

parser.add_argument("folder_path", type=str, help="Path to the folder containing files.")
parser.add_argument("-n", "--num_files", type=int, default=1, help="Number of files to process (default: 1).")

args = parser.parse_args()

folder_path = args.folder_path
num_files = args.num_files

def get_random_data(file_path, window_size=30):

  try:
    with open(file_path, 'r') as file:
      reader = csv.reader(file)
      data = list(reader)  # Read all CSV rows into a list

      if not data:
        raise ValueError("File is empty.")

      total_lines = len(data)

      # Make sure enough data points for the window size
      if total_lines < window_size:
        raise ValueError(f"File has fewer than {window_size} data points.")

      # Start with a random index within the valid range
      random_index = random.randint(0, total_lines - window_size - 1)

      # Extract the data points
      extracted_data = data[random_index:random_index+window_size]

      # Convert each row (list) to a list with stock_id, timestamp, and price
      parsed_data = [[row[0], row[1], float(row[2])] for row in extracted_data]

      return parsed_data

  except FileNotFoundError:
    raise FileNotFoundError(f"File not found: {file_path}")


def detect_outliers(data):

  # Extract price values from the data
  prices = [point[2] for point in data]

  # Calculate mean and standard deviation
  mean = statistics.mean(prices)
  std_dev = statistics.stdev(prices)

  # Define outlier threshold (2 standard deviations).
  threshold = 2 * std_dev

  outliers = []
  for point in data:
    # Extract data and calculate deviation
    stock_id, timestamp, price = point
    deviation = abs(price - mean)

    # Check for outliers and calculate statistics
    if deviation > threshold:
      outlier_data = {
          "stock_id": stock_id,
          "timestamp": timestamp,
          "actual_price": price,
          "mean": mean,
          "difference": deviation,
          "percent_deviation": (deviation / mean) * 100
      }
      outliers.append(outlier_data)

  return outliers


def write_outlier_report(outliers, file_path):
  
  if not outliers:
    print("No outliers found, skip writing a report.")
  else:
    print(f"Found {len(outliers)} outliers. Writing report.")

# debug 1 - check the output of the outliers
    # print(f"{outliers}")

     
  headers = ["Stock-ID", "Timestamp", "Actual Price", "Mean", "Difference", "% Deviation"]

  try:
      # Extract filename without extension
      filename = os.path.splitext(os.path.basename(file_path))[0]
      output_file_path = os.path.join(os.path.dirname(file_path), f"{filename}_outliers.csv")

      with open(output_file_path, 'w', newline='') as file:
          writer = csv.writer(file)
          writer.writerow(headers)

          for outlier in outliers:
              stock_id, timestamp, price, mean, difference, percent_deviation = outlier

              # Write line by line 
              writer.writerow([outlier[stock_id], outlier[timestamp], outlier[price], outlier[mean], outlier[difference], outlier[percent_deviation]])

  except OSError as e:
      print(f"Error writing outlier report for {file_path}: {e}")


def main(folder_path, num_files=1):

  exchange_name = folder_path.split("/")[-1]  # Extract exchange name from folder path
  results = []

  # Get a list of all CSV files in the folder with the exception of the output files
  csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv") and not f.__contains__("_outliers") ]

  # Loop through the recommended number of files
  for csvfile in range(1, int(num_files)):
    try:
      # Select a random CSV file
      random_file = random.choice(csv_files)
      file_path = os.path.join(folder_path, random_file)

      # Get random data and detect outliers
      data = get_random_data(file_path)
      outliers = detect_outliers(data)


      # Write outlier report to a separate CSV file
      write_outlier_report(outliers, file_path)

      results.append({"exchange": exchange_name, "outliers": outliers})

    except (FileNotFoundError, ValueError) as e:
      print(f"Error processing sample {csvfile} for {exchange_name}: {e}")

  return results


# Run script
if __name__ == "__main__":
# deprecated method of getting input. Using script parameters instead.
#   folder_path = input("Enter the directory containing exchange data: ")
#   num_files = input("Enter the recommended number of files to be sampled for each Stock Exchange: ")
  main(folder_path, num_files)