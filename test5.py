import yfinance as yf

def fetch_stock_metrics_with_ttm_alpha(stock_ticker, market_ticker="^NSEI"):
    """
    Fetches stock metrics including Alpha (TTM) using historical data.

    Parameters:
    - stock_ticker: Ticker symbol of the stock (e.g., "RELIANCE.NS")
    - market_ticker: Ticker symbol of the market index (default: "^NSEI" for Nifty 50)

    Returns:
    - Dictionary of stock metrics
    """
    stock = yf.Ticker(stock_ticker)
    market = yf.Ticker(market_ticker)

    # Fetch stock and market historical data for the past year (TTM)
    stock_hist = stock.history(period="1y")
    market_hist = market.history(period="1y")

    if stock_hist.empty or market_hist.empty:
        return {"Error": "Historical data is unavailable for the given ticker(s)."}

    # Calculate daily returns
    stock_daily_returns = stock_hist['Close'].pct_change()
    market_daily_returns = market_hist['Close'].pct_change()

    # Calculate annualized return for the stock and market
    stock_annualized_return = stock_daily_returns.mean() * 252  # Annualized for ~252 trading days
    market_annualized_return = market_daily_returns.mean() * 252

    # Calculate Alpha (TTM)
    alpha_ttm = stock_annualized_return - market_annualized_return

    # Fetch key metrics
    info = stock.info
    metrics = {
        "Stock Price (INR)": info.get('currentPrice'),  # Delayed real-time stock price
        "Beta": info.get('beta'),  # Volatility compared to the market
        "P/E Ratio (TTM)": info.get('trailingPE'),  # Price-to-Earnings ratio
        "P/B Ratio (TTM)": info.get('priceToBook'),  # Price-to-Book ratio
        "EV/EBITDA (TTM)": info.get('enterpriseToEbitda'),  # Enterprise Value to EBITDA
        "ROE (%) (TTM)": info.get('returnOnEquity', 0) * 100,  # Return on Equity
        "Revenue Growth (YoY, %) (TTM)": info.get('revenueGrowth', 0) * 100,  # Revenue growth
        "Profit Growth (%) (YoY)": info.get('earningsGrowth', 0) * 100,  # Profit growth
        "Promoter Holding (%)": info.get('heldPercentInsiders', 0) * 100,  # Proxy for promoter holding
        "Expert Recommendation": info.get('recommendationKey', 'N/A'),  # Buy/Sell/Hold recommendation
        "Alpha (TTM)": alpha_ttm,  # Alpha based on TTM
    }

    return metrics

# Example usage
if __name__ == "__main__":
    stock_ticker = "ITC.NS"  # Replace with your stock ticker
    market_ticker = "^NSEI"  # Replace with market index ticker (default: Nifty 50)
    data = fetch_stock_metrics_with_ttm_alpha(stock_ticker, market_ticker)

    print("\nStock Metrics with Alpha (TTM):")
    for key, value in data.items():
        print(f"{key}: {value}")
