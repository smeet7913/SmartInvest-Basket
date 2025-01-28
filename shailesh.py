import requests
from bs4 import BeautifulSoup
import yfinance as yf
import csv
import warnings

# Suppress specific FutureWarnings from yfinance
warnings.simplefilter(action='ignore', category=FutureWarning)


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


# Function to convert stock data to CSV
def convert_to_csv(stock_symbols, filename="stock_data.csv"):
    fieldnames = [
        'Stock Symbol', 'Current Price', 'P/E Ratio', 'Beta', 'RSI', 'EPS (ttm)', '52-Week Low', '52-Week High',
        'Revenue Growth (YoY)', 'EPS Growth', 'Profit Margin', 'EBITDA Margin', 'Quick Ratio', 'Current Ratio', 
        'Return on Equity (ROE)', 'Return on Assets (ROA)', 'Market Cap Growth', 'PB Ratio', 'Debt / Equity',
        'Expert Recommendation', 'Analyst Target Price'
    ]
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for stock_symbol in stock_symbols:
            stock_data = fetch_all_stock_data(stock_symbol)
            
            # Flatten the dictionary to match CSV structure
            flattened_data = {'Stock Symbol': stock_symbol}
            
            # Flatten each category's data into the CSV format
            for category, data in stock_data.items():
                if isinstance(data, dict):
                    for key, value in data.items():
                        # Flatten the key-value pairs from categories
                        flattened_data[key] = value
                else:
                    flattened_data[category] = data

            writer.writerow(flattened_data)


# Example usage with a list of stock symbols
stock_symbols = ['RELIANCE', 'TCS', 'INFY']  # Replace with desired stock symbols

# Convert data to CSV
convert_to_csv(stock_symbols, filename="stock_data.csv")

#to read csv
import pandas as pd

df = pd.read_csv('stock_data.csv')

df