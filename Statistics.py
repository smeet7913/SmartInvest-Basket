import requests
from bs4 import BeautifulSoup

# Function to fetch the value next to a given label using a more specific approach
def fetch_stat_value(soup, label):
    # Look for the row containing the label and extract the second column (value)
    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 1 and label in row.get_text():
            return cols[1].text.strip()
    return None

# Function to fetch stock statistics
def fetch_stock_statistics(stock_name):
    # Define the URL with the stock name
    url = f'https://stockanalysis.com/quote/nse/{stock_name}/statistics/'

    # Send a request to the website and get the HTML content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for {stock_name}. HTTP Status Code: {response.status_code}")
        return None

    html_content = response.text

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Fetch PB Ratio and Debt/Equity
    pb_ratio = fetch_stat_value(soup, 'PB Ratio')
    debt_equity = fetch_stat_value(soup, 'Debt / Equity')

    return {
        "Stock": stock_name,
        "PB Ratio": pb_ratio if pb_ratio else "N/A",
        "Debt / Equity": debt_equity if debt_equity else "N/A"
    }

# List of stock names (you can add more stock names here)
stock_names = ["TCS", "RELIANCE", "INFY"]

# Process each stock and display the results
for stock in stock_names:
    print(f"\nFetching data for {stock}...")
    stock_data = fetch_stock_statistics(stock)
    if stock_data:
       
        print(f"  PB Ratio: {stock_data['PB Ratio']}")
        print(f"  Debt / Equity: {stock_data['Debt / Equity']}")
    else:
        print(f"Data for {stock} could not be retrieved.")
