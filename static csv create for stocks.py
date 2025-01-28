import csv
import os
import yfinance as yf  # Ensure you have installed yfinance using `pip install yfinance`

# Define the file name
csv_file = "hello.csv"

# Function to initialize the CSV file with headers if it doesn't exist
def initialize_csv(file_name):
    if not os.path.exists(file_name):
        with open(file_name, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Stock Symbol", "Full Name", "Theme"])  # Add headers

# Function to fetch the full name of a stock using yfinance
def fetch_stock_full_name(stock_symbol):
    try:
        # Temporarily append '.NS' for the lookup
        stock = yf.Ticker(stock_symbol + ".NS")
        return stock.info.get('longName', "Unknown")  # Default to "Unknown" if full name is unavailable
    except Exception as e:
        print(f"Error fetching name for {stock_symbol}: {e}")
        return "Unknown"

# Function to add a stock symbol, full name, and theme to the CSV file
def add_stock(file_name, stock_symbol, theme):
    existing_entries = set()  # Stores (stock_symbol, theme) pairs

    # Check if the file exists and load existing entries
    if os.path.exists(file_name):
        with open(file_name, mode="r") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            for row in reader:
                existing_entries.add((row[0].strip().lower(), row[2].strip().lower()))  # Store as lowercase tuple

    # Check if the exact stock symbol and theme combination already exists
    if (stock_symbol.strip().lower(), theme.strip().lower()) in existing_entries:
        print(f"{stock_symbol} with theme '{theme}' already exists in the CSV file. Skipping.")
    else:
        # Fetch the full name of the stock
        full_name = fetch_stock_full_name(stock_symbol)

        # Add the new stock symbol with its full name and theme
        with open(file_name, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([stock_symbol, full_name, theme])
            print(f"{stock_symbol} ({full_name}) with theme '{theme}' added to the CSV file.")

# Initialize the CSV file
initialize_csv(csv_file)

# List of stock symbols
stocks = [
    "YESBANK", "SRF", "SBICARD", "FEDERALBNK", "MARICO", 
    "COLPAL", "CONCOR", "MPHASIS", "POLICYBZR", "DIXON", 
    "MRF", "ACC", "HINDPETRO", "MUTHOOTFIN", "GMRAIRPORT", 
    "PHOENIXLTD", "CUMMINSIND", "KPITTECH", "TATACOMM", "INDHOTEL", 
    "ALKEM", "NMDC", "ASTRAL", "BHARATFORG", "POLYCAB", 
    "LUPIN", "VOLTAS", "UPL", "GODREJPROP", "SUNDARMFIN", 
    "AUROPHARMA", "ABCAPITAL", "APLAPOLLO", "SAIL", "ASHOKLEY", 
    "MAXHEALTH", "LTF", "PETRONET", "OFSS", "PERSISTENT", 
    "PIIND", "OBEROIRLTY", "INDUSTOWER", "HDFCAMC", "CGPOWER", 
    "SUZLON", "IDEA", "SUPREMEIND", "IDFCFIRSTB", "AUBANK"
]

# Theme for all stocks
theme = "Midcap"

# Add each stock symbol with the theme to the CSV
for stock in stocks:
    add_stock(csv_file, stock, theme)
