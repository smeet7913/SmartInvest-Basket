import yfinance as yf

def get_analyst_data(stock_names):
    for stock_name in stock_names:
        ticker = stock_name + '.NS'  # Append .NS for NSE-listed stocks
        
        try:
            # Fetch the stock data using yfinance
            stock = yf.Ticker(ticker)
            
            # Get the expert recommendation from the stock info
            expert_recommendation = stock.info.get('recommendationKey', 'N/A')  # Buy/Sell/Hold recommendation
            target_price = stock.info.get('targetMeanPrice', 'N/A')  # Analyst Target Price
            
            # Print stock name first
            print(f"{stock_name}:")
            
            # Display expert recommendation and target price if available
            if expert_recommendation != 'N/A':
                print(f"  Expert Recommendation: {expert_recommendation}")
            else:
                print("  Expert Recommendation: N/A")
            
            if target_price != 'N/A':
                print(f"  Analyst Target Price: {target_price}")
            else:
                print("  Analyst Target Price: N/A")
            
            print("-" * 50)  # Separator for readability
            
        except Exception as e:
            print(f"An error occurred for {stock_name}: {e}")
            print("-" * 50)  # Separator for readability

# Example usage with a list of stock names
stock_list = ['Reliance', 'TCS', 'TataMotors']  # List of stock names
get_analyst_data(stock_list)
