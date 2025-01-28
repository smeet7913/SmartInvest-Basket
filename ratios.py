import requests
from bs4 import BeautifulSoup

def fetch_ratio(soup, ratio_name):
    """Fetch a specific ratio value using the defined logic."""
    row = soup.find(string=ratio_name)
    if row:
        columns = row.find_parent('tr').find_all('td')
        if len(columns) > 1:
            return columns[2].text.strip() if columns[1].text.strip() == '-' and len(columns) > 2 else columns[1].text.strip()
    return None

def fetch_stock_ratios(stock_symbol, ratios):
    """Fetch ratios for a specific stock."""
    url = f'https://stockanalysis.com/quote/nse/{stock_symbol}/financials/ratios/'
    try:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        print(f"\nFinancial Ratios for {stock_symbol.upper()}:")
        for ratio in ratios:
            print(f"{ratio}: {fetch_ratio(soup, ratio) or 'Data not found'}")
    except Exception as e:
        print(f"Error fetching data for {stock_symbol.upper()}: {e}")

# List of stocks and ratios
stock_symbols = ["reliance", "tcs", "tatamotors"]
ratios_to_fetch = [
    "Quick Ratio",
    "Current Ratio",
    "Return on Equity (ROE)",
    "Return on Assets (ROA)",
    "Market Cap Growth"
]

# Fetch and display ratios for all stocks
for stock in stock_symbols:
    fetch_stock_ratios(stock, ratios_to_fetch)
