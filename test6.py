import requests
from bs4 import BeautifulSoup

# Function to fetch Debt / Equity ratio from the statistics page
def get_debt_equity_ratio(stock_symbol):
    url = f"https://stockanalysis.com/quote/nse/{stock_symbol}/statistics/"
    
    # Send the request
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        debt_equity = 'N/A'
        
        try:
            # Look for the table row containing "Debt / Equity"
            rows = soup.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) > 1 and 'Debt / Equity' in cols[0].text:
                    debt_equity = cols[1].text.strip()
                    break  # Stop after finding the Debt / Equity row
        except AttributeError:
            pass  # In case of any error, keep debt_equity as 'N/A'
        
        return debt_equity
    else:
        print(f"Failed to fetch data for {stock_symbol}")
        return 'N/A'

# Example usage
stock_symbol = 'RELIANCE'  # Replace with the stock symbol you want
debt_equity = get_debt_equity_ratio(stock_symbol)

# Output the result
print(f"Debt-to-Equity for {stock_symbol}: {debt_equity}")
