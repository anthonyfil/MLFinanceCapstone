## Predicting the Motion of Securities using Machine Learning
# Software Packages:
NumPy
Pandas
Sklearn
Pyplot
Glob
Python3
Kivy
Csv

# Algorithm Sequential Steps:
1. Running the algorithm:
2. Find an IDE/editor that allows you to run capstone_decision_tree.py
3. Modify the file path to include the latest version of our data (Line 13)

# Visualization Sequential Steps:
1. Find an IDE/editor that allows you to run GUI.py
2. Input numbers
3. Get resulting estimate for delta ROA

# Git Repository:
https://github.com/anthonyfil/MLFinanceCapstone

# Unrealized Features:
Looking at the relationships between indicators using combinatorial decision trees.

# Data Cleaning Software Packages:
pandas
random
datetime
os

# Data Cleaning Sequential Steps:
1. Extract Input Data into the SECData folder.

  a. Each quarter can be found at: https://www.sec.gov/dera/data/financial-statement-data-sets.html. These are arranged as SECData/20XXqX folders
  
2. Run FinalDataCleaner.py

4. Type E, C, or B to Extract data from SEC filing folders, Clean extracted data, or Both extract and clean respectively.

  a. Extracting will sort data out of quarterly SEC filings into company specific csv files
  
  b. Cleaning will take extracted data and clean irrelevant data out and present sorted information with calculated indicators.
  
4. Adjusting Settings

  a. TickerCIK.csv stores the companies we are interested in looking at. These are both stock ticker (for readability), and CIK number (for reference)
  
  b. RequiredStats.csv stores the indicators and data points we are most interested in. During data cleaning, the process will remove quarters where these indicators have insufficient data.
  
  c. SeenStats.csv stores the indicators and data points we wish to view. During data cleaning, these indicators will be sorted, but still included even if data coverage is spotty.

