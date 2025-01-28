import requests
import yfinance as yf
import time

# Step 1: Fetch stock symbols from the NSE API
def fetch_stock_symbols():
    # URL of the NSE page that lists stock names
    url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20MIDCAP%2050"

    # Headers to include in the request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "Cookie": "_ga=GA1.1.960283774.1716295466; _ga_QJZ4447QD3=GS1.1.1716295488.1.1.1716295533.0.0.0; _abck=F54BF07DD29CEEC70D63CB33D0A5CFEF~0~YAAQDvY3F0BoZ16UAQAASiNXbw0QwB6+rJjPadECzgbucstPxcGefChqdqvIeJQBYySqBWRbQo84jAai1Me20CtwuQEfp7rZ4Xcp6dhvJAFi2MAR01afq4ASgA6w67YHyptRmeJoSH8SrEiRdqmJv4+rGLlWYln+WrMr1hXAR8yV3GX+muqVZguNi48/EP0uq/XiGJuMc6y9lQPrKw9W/ruMmzdcTZAMmpaZytxLK4833nP+xXKQUPMIoEjJiGbn+0gaba59i+UdCUbe23ay2qKeyCZzkJhqaWTEdJnBXQxMMoTkkxUJ8ZxKHOyCPwZ8iIGAtdSm7OnyXeP1JqqUsSJ9FUrHzq7yWM2cC9m3rHk9vLwZOzcD0wcw1ErMUZRlCF4o+6Ea9RgagWGqHCSIOj+JOYXETNF412yjvq8rAd5X/C2AAQeBRfscyQ4oXYeTp2b17WL7hs7PfFspP0MVFA9ySb3/5OItfB8Ef1RU9RirY2ClmTUm3NHyECFzhw==~-1~-1~-1",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5"
    }

    # Send GET request to fetch the content
    response = requests.get(url, headers=headers)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()  # Assuming the response is JSON
        stock_symbols = [stock.get('symbol') for stock in data.get('data', [])]
        return stock_symbols
    else:
        print(f"Failed to fetch stock symbols. Status code: {response.status_code}")
        return []

# Step 2: Fetch stock data from Yahoo Finance
def fetch_all_stocks_data(stocks_list):
    all_stocks_data = {}
    
    for stock_symbol in stocks_list:
        stock = yf.Ticker(stock_symbol + ".NS")  # Add ".NS" for NSE stocks
        
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

# Main execution
if __name__ == "__main__":
    # Step 1: Fetch stock symbols
    stock_symbols = fetch_stock_symbols()
    
    if stock_symbols:
        print(f"Fetched {len(stock_symbols)} stock symbols.")
        
        # Step 2: Fetch stock data
        stocks_data = fetch_all_stocks_data(stock_symbols)
        
        # Display the results
        for symbol, data in stocks_data.items():
            print(f"Stock: {symbol}")
            print(f"Share Price: {data['Share Price']}")
            print(f"P/E Ratio: {data['P/E Ratio']}")
            print(f"EPS (TTM): {data['EPS (TTM)']}")
            print("-" * 50)
    else:
        print("No stock symbols fetched.")
