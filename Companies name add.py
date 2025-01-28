import csv
import os

# Define the file name
csv_file = "companies.csv"

# Function to initialize the CSV file with headers if it doesn't exist
def initialize_csv(file_name):
    if not os.path.exists(file_name):
        with open(file_name, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Stock Name", "Theme"])  # Add headers

# Function to add a company to the CSV file
def add_company(file_name, company_name, theme):
    # Read the existing companies to check for duplicates
    existing_companies = set()
    if os.path.exists(file_name):
        with open(file_name, mode="r") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            for row in reader:
                existing_companies.add(row[0].strip().lower())  # Store company names in lowercase

    # Check if the company already exists
    if company_name.strip().lower() in existing_companies:
        print(f"{company_name} already exists in the CSV file. Skipping.")
    else:
        # Add the new company
        with open(file_name, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([company_name, theme])
            print(f"{company_name} added to the CSV file.")

# Initialize the CSV file
initialize_csv(csv_file)

# List of stock names and theme
stocks = [
    "ICICIBANK", "HDFCBANK", "KOTAKBANK", "BANKBARODA", "AXISBANK",
    "INDUSINDBK", "AUBANK", "SBIN", "FEDERALBNK", "IDFCFIRSTB", "CANBK", "PNB"
]

# Theme to be set for all stocks
theme = "Midcap"

# Add each stock to the CSV with the 'Midcap' theme
for stock in stocks:
    add_company(csv_file, stock, theme)
