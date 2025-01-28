import yfinance as yf
import time

# A hypothetical list of stock symbols (for example, Indian stocks on NSE)
# You would need to fetch or provide this list
all_stocks = [
    "TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS", "RELIANCE.NS", 
    "ADANIGREEN.NS", "SBIN.NS", "BHARTIARTL.NS", "ICICIBANK.NS", "LT.NS"
]

def fetch_all_stocks_data(stocks_list):
    all_stocks_data = {}
    
    for stock_symbol in stocks_list:
        stock = yf.Ticker(stock_symbol)
        
        # Get fundamental data
        fundamental_data = stock.info
        
        # Extract required data points
        stock_data = {
            "Share Price": fundamental_data.get('currentPrice', 'N/A'),
            "P/E Ratio": fundamental_data.get('trailingPE', 'N/A'),
            "EPS (TTM)": fundamental_data.get('trailingEps', 'N/A'),
        }
        
        all_stocks_data[stock_symbol] = stock_data
        time.sleep(1)  # To avoid hitting rate limits of Yahoo Finance
        
    return all_stocks_data

# Example usage
stocks_data = fetch_all_stocks_data(all_stocks)

# Displaying the results
for symbol, data in stocks_data.items(): 
    print(f"Stock: {symbol}")
    print(f"Share Price: {data['Share Price']}")
    print(f"P/E Ratio: {data['P/E Ratio']}")
    print(f"EPS (TTM): {data['EPS (TTM)']}")
    print("-" * 50)
