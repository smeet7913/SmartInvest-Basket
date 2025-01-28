import yfinance as yf

def fetch_stock_metrics_with_alpha(ticker, market_ticker="^NSEI"):
    stock = yf.Ticker(ticker)
    market = yf.Ticker(market_ticker)

    # Fetch latest stock info
    info = stock.info

    # Fetch historical data for the past 1 year (for Alpha calculation)
    stock_hist = stock.history(period="1y")
    market_hist = market.history(period="1y")

    # Calculate stock and market annualized returns
    stock_return = (stock_hist['Close'].pct_change().mean()) * 252  # Annualized stock return
    market_return = (market_hist['Close'].pct_change().mean()) * 252  # Annualized market return

    # Alpha = Stock Return - Market Return
    alpha = stock_return - market_return

    # Fetch metrics
    metrics = {
        "Stock Price (INR)": info.get('currentPrice'),  # Real-time market price (delayed)
        "Beta": info.get('beta'),  # Volatility compared to the market
        "P/E Ratio (TTM)": info.get('trailingPE'),  # Price-to-Earnings ratio
        "P/B Ratio (TTM)": info.get('priceToBook'),  # Price-to-Book ratio
        "EV/EBITDA (TTM)": info.get('enterpriseToEbitda'),  # Enterprise Value to EBITDA
        "ROE (%) (TTM)": info.get('returnOnEquity', 0) * 100,  # Return on Equity
        "Net Profit Margin (%) (TTM)": info.get('profitMargins', 0) * 100,  # Net profit margin
        "D/E Ratio (TTM)": info.get('debtToEquity'),  # Debt-to-Equity ratio
        "Revenue Growth (YoY, %) (TTM)": info.get('revenueGrowth', 0) * 100,  # Revenue Growth
        "Profit Growth (%) (YoY)": info.get('earningsGrowth', 0) * 100,  # Profit Growth
        "ROCE (%)": info.get('returnOnCapitalEmployed', 0) * 100,  # Return on Capital Employed
        "Promoter Holding (%)": info.get('heldPercentInsiders', 0) * 100,  # Proxy for promoter holding
        "Expert Recommendation": info.get('recommendationKey', 'N/A'),  # Buy/Sell/Hold recommendation
        "Alpha (1 Year)": alpha,  # Annualized alpha
    }

    return metrics

# Example usage
if __name__ == "__main__":
    ticker = "WIPRO.NS"  # Replace with stock ticker
    market_ticker = "^NSEI"  # Replace with the market index ticker (e.g., Nifty 50)
    data = fetch_stock_metrics_with_alpha(ticker, market_ticker)
    print("\nStock Metrics with Alpha (Delayed):")
    for key, value in data.items():
        print(f"{key}: {value}")
