import requests
from bs4 import BeautifulSoup

# Function to fetch stock data
def get_stock_data(stock_symbol):
    url = f"https://stockanalysis.com/quote/nse/{stock_symbol}/"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data for {stock_symbol}")
        return { 'Current Price': 'N/A', 'P/E Ratio': 'N/A', 'Beta': 'N/A', 
                 'RSI': 'N/A', 'EPS (ttm)': 'N/A', '52-Week Low': 'N/A', '52-Week High': 'N/A' }
    
    soup = BeautifulSoup(response.text, 'html.parser')
    metrics = { 'Current Price': 'N/A', 'P/E Ratio': 'N/A', 'Beta': 'N/A', 
                'RSI': 'N/A', 'EPS (ttm)': 'N/A', '52-Week Low': 'N/A', '52-Week High': 'N/A' }

    # Extract stock price
    price = soup.find('div', class_='text-4xl font-bold inline-block')
    if price: metrics['Current Price'] = price.text.strip()

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

# Fetch data for multiple stocks
def get_multiple_stocks_data(stock_symbols):
    return {symbol: get_stock_data(symbol) for symbol in stock_symbols}

# List of stock symbols
stock_symbols = ['RELIANCE', 'TCS', 'INFY']
data = get_multiple_stocks_data(stock_symbols)

# Display results
for symbol, details in data.items():
    print(f"\n{symbol}:")
    for metric, value in details.items():
        print(f"{metric}: {value}")
