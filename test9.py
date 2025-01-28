import requests
from bs4 import BeautifulSoup
import yfinance as yf
import csv
import pandas as pd  # For loading and analyzing CSV data


# Function to load stock symbols from the CSV file
def load_stock_symbols_from_csv(csv_filename):
    try:
        data = pd.read_csv(csv_filename)
        # Assuming the CSV file has a column named 'Stock Symbol' containing stock symbols
        stock_symbols = data['Stock Symbol'].tolist()
        return stock_symbols
    except Exception as e:
        print(f"Error loading stock symbols from {csv_filename}: {e}")
        return []


# Function to fetch stock price and key metrics
def fetch_stock_data(stock_symbol):
    url = f"https://stockanalysis.com/quote/nse/{stock_symbol}/"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data for {stock_symbol}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    metrics = { 'Current Price': 'N/A', 'P/E Ratio': 'N/A', 'Beta': 'N/A', 
                'RSI': 'N/A', 'EPS (ttm)': 'N/A', '52-Week Low': 'N/A', '52-Week High': 'N/A' }

    # Extract stock price
    price = soup.find('div', class_='text-4xl font-bold inline-block')
    if price:
        metrics['Current Price'] = price.text.strip()

    # Extract key metrics
    rows = soup.find_all('tr', class_='flex flex-col border-b border-default py-1 sm:table-row sm:py-0')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 1:
            key, value = cols[0].text.strip(), cols[1].text.strip()
            if 'PE Ratio' in key: metrics['P/E Ratio'] = value
            elif 'Beta' in key: metrics['Beta'] = value
            elif 'RSI' in key: metrics['RSI'] = value
            elif 'EPS (ttm)' in key: metrics['EPS (ttm)'] = value
            elif '52-Week Range' in key:
                try:
                    low, high = value.split('-')
                    metrics['52-Week Low'] = low.strip()
                    metrics['52-Week High'] = high.strip()
                except ValueError:
                    metrics['52-Week Low'] = metrics['52-Week High'] = 'N/A'

    return metrics


# Function to fetch financial data (Revenue Growth, EPS Growth, Profit Margin, EBITDA Margin)
def fetch_financial_data(stock_symbol):
    url = f'https://stockanalysis.com/quote/nse/{stock_symbol}/financials/'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data for {stock_symbol}. HTTP Status Code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')

    def fetch_growth_value(label):
        growth_section = soup.find(string=label)
        if growth_section:
            value_cell = growth_section.find_parent('tr').find_all('td')[1]  # Get the second <td> in the row
            return value_cell.text.strip()
        return "Data not found"

    metrics = {
        "Revenue Growth (YoY)": fetch_growth_value("Revenue Growth (YoY)"),
        "EPS Growth": fetch_growth_value("EPS Growth"),
        "Profit Margin": fetch_growth_value("Profit Margin"),
        "EBITDA Margin": fetch_growth_value("EBITDA Margin")
    }

    return metrics


# Function to fetch stock ratios (Quick Ratio, Current Ratio, ROE, ROA, Market Cap Growth)
def fetch_stock_ratios(stock_symbol):
    url = f'https://stockanalysis.com/quote/nse/{stock_symbol}/financials/ratios/'
    response = requests.get(url)
    ratios = {
        "Quick Ratio": None,
        "Current Ratio": None,
        "Return on Equity (ROE)": None,
        "Return on Assets (ROA)": None,
        "Market Cap Growth": None
    }
    
    if response.status_code != 200:
        print(f"Failed to fetch ratios for {stock_symbol}")
        return ratios
    
    soup = BeautifulSoup(response.text, 'html.parser')

    def fetch_ratio(ratio_name):
        row = soup.find(string=ratio_name)
        if row:
            columns = row.find_parent('tr').find_all('td')
            if len(columns) > 1:
                return columns[2].text.strip() if columns[1].text.strip() == '-' and len(columns) > 2 else columns[1].text.strip()
        return None

    for ratio in ratios.keys():
        ratios[ratio] = fetch_ratio(ratio) or "Data not found"
    
    return ratios


# Function to fetch PB Ratio and Debt/Equity
def fetch_stock_statistics(stock_symbol):
    url = f'https://stockanalysis.com/quote/nse/{stock_symbol}/statistics/'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for {stock_symbol}. HTTP Status Code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    def fetch_stat_value(label):
        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 1 and label in row.get_text():
                return cols[1].text.strip()
        return None

    pb_ratio = fetch_stat_value('PB Ratio')
    debt_equity = fetch_stat_value('Debt / Equity')

    return {
        "PB Ratio": pb_ratio if pb_ratio else "N/A",
        "Debt / Equity": debt_equity if debt_equity else "N/A"
    }


# Function to fetch analyst data (Recommendation, Target Price)
def fetch_analyst_data(stock_symbol):
    ticker = stock_symbol + '.NS'  # Append .NS for NSE-listed stocks
    
    try:
        stock = yf.Ticker(ticker)
        expert_recommendation = stock.info.get('recommendationKey', 'N/A')
        target_price = stock.info.get('targetMeanPrice', 'N/A')
        
        return {
            "Expert Recommendation": expert_recommendation,
            "Analyst Target Price": target_price
        }
    
    except Exception as e:
        print(f"An error occurred for {stock_symbol}: {e}")
        return {
            "Expert Recommendation": "N/A",
            "Analyst Target Price": "N/A"
        }


# Master function to fetch all data for a stock
def fetch_all_stock_data(stock_symbol):
    stock_data = {}

    # Fetch stock data
    stock_data['Price and Metrics'] = fetch_stock_data(stock_symbol)
    
    # Fetch financial data
    stock_data['Financial Data'] = fetch_financial_data(stock_symbol)
    
    # Fetch stock ratios
    stock_data['Stock Ratios'] = fetch_stock_ratios(stock_symbol)
    
    # Fetch stock statistics
    stock_data['Stock Statistics'] = fetch_stock_statistics(stock_symbol)
    
    # Fetch analyst data
    stock_data['Analyst Data'] = fetch_analyst_data(stock_symbol)

    return stock_data


# Function to display data in a readable format
def display_stock_data(stock_symbol, stock_data):
    print(f"\n{stock_symbol.upper()}:")
    
    for category, data in stock_data.items():
        print(f"\n{category}:")
        if isinstance(data, dict):
            for key, value in data.items():
                print(f"  {key}: {value}")
        else:
            print(f"  {data}")


# Function to save data to CSV
def save_data_to_csv(stock_data, filename):
    # Flatten the nested dictionary structure for CSV storage
    flat_data = []
    for stock_symbol, data in stock_data.items():
        flattened_row = {'Stock Symbol': stock_symbol}
        for category, metrics in data.items():
            if isinstance(metrics, dict):
                for key, value in metrics.items():
                    flattened_row[f"{category} - {key}"] = value
            else:
                flattened_row[category] = metrics
        flat_data.append(flattened_row)

    # Save to CSV
    keys = flat_data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(flat_data)
    print(f"Data saved to {filename}")


# Function to load and analyze data from CSV
def load_data_from_csv(filename):
    try:
        data = pd.read_csv(filename)
        print(f"\nData loaded from {filename}:")
        print(data.head())  # Display the first few rows for verification
        return data
    except Exception as e:
        print(f"Error loading data from {filename}: {e}")
        return None


# Main execution
if __name__ == "__main__":
    companies_csv_filename = 'companies.csv'  # Replace with the path to your CSV file
    stock_symbols = load_stock_symbols_from_csv(companies_csv_filename)  # Fetch stock symbols from CSV

    if not stock_symbols:
        print("No stock symbols found.")
    else:
        all_stock_data = {}

        # Fetch data for each stock symbol
        for stock_symbol in stock_symbols:
            stock_data = fetch_all_stock_data(stock_symbol)
            all_stock_data[stock_symbol] = stock_data

        # Save all stock data to CSV
        csv_output_filename = 'stock_data.csv'
        save_data_to_csv(all_stock_data, csv_output_filename)

        # Load data from CSV for analysis
        stock_data_df = load_data_from_csv(csv_output_filename)

        # Example analysis: Display basic statistics for numeric columns
        if stock_data_df is not None:
            print("\nBasic statistics for numeric columns:")
            print(stock_data_df.describe())
