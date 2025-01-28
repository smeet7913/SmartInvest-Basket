import requests
from bs4 import BeautifulSoup

# Function to fetch financial data for a specific stock
def fetch_financial_data(stock_symbol):
    url = f'https://stockanalysis.com/quote/nse/{stock_symbol}/financials/'  # Dynamic URL for each stock
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data for {stock_symbol}. HTTP Status Code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Function to fetch the value next to a given label
    def fetch_growth_value(label):
        growth_section = soup.find(string=label)
        if growth_section:
            value_cell = growth_section.find_parent('tr').find_all('td')[1]  # Get the second <td> in the row
            return value_cell.text.strip()
        return "Data not found"

    # Metrics to fetch
    metrics = {
        "Revenue Growth (YoY)": None,
        "EPS Growth": None,
        "Profit Margin": None,
        "EBITDA Margin": None
    }

    for metric in metrics.keys():
        metrics[metric] = fetch_growth_value(metric)
    
    return metrics

# List of stock symbols to fetch data for
stock_symbols = ['RELIANCE', 'INFY', 'TATAMOTORS']  # Replace with the stock symbols of interest

# Fetch and display data for each stock
for stock_symbol in stock_symbols:
    print(f"\nFetching data for {stock_symbol}...")
    stock_data = fetch_financial_data(stock_symbol)
    if stock_data:
        print(f"Financial Data for {stock_symbol}:")
        for key, value in stock_data.items():
            print(f"{key}: {value}")
