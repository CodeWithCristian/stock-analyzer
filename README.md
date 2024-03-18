
## Stock Data Outlier Analyzer

This Python script analyzes stock data in CSV format to identify outliers in price data. It utilizes methods from the statitiscs module in Python to generate  reports for further investigation.

**Features:**

- **Command-line Interface:** Accepts a folder path containing CSV files and an optional number of files to process.
- **Random Sampling:** Analyzes randomly chosen windows of data points (default 30) from each file.
- **Outlier Detection:** Flags data points that significantly deviate from the average price (2 standard deviations by default).
- **Report Generation:** Creates separate CSV files for each analyzed file, detailing outliers with timestamps, prices, and deviation statistics.
- **Error Handling:** Catches potential file-related errors and provides informative messages.

**Usage:**

1. Save the script as a Python file (e.g., `stock_analyzer.py`).
2. Open a terminal or command prompt and navigate to the directory containing the script and your CSV files.
3. Run the script with the following command, replacing `<folder_path>` with the actual path to your folder:

```
python stock_analyzer.py <folder_path> [--num_files <number>]
```

- `<number>` (optional): The recommended number of files to sample from each exchange (default: 1).

**Example:**

```
python stock_analyzer.py data/NYSE --num_files 2
```

This command analyzes data in the `data/NYSE` folder, processing a random sample of two CSV files and generating outlier reports if it finds any outliers.

**Dependencies:**

- Python 3 (with standard libraries: `csv`, `random`, `statistics`, `os`, `argparse`)

**Note:**

- The script assumes CSV files with three columns: stock ID, timestamp, and price.
- The outlier threshold can be adjusted within the script by modifying the value used for standard deviations in the `detect_outliers` function.
