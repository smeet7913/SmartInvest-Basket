import requests
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from textblob import TextBlob

# Stock symbols to full stock names
# stock_symbol_to_name = {
#     "AAPL": "Apple Inc.",
#     "LMT": "Lockheed Martin",
#     "GOOG": "Alphabet Inc. (Google)",
#     "MSFT": "Microsoft Corporation",
#     # Add more stock symbols and names as needed
# }

stock_symbol_to_name = {
    
    
    #Indian stocks
    "INFY.NS": "Infosys Limited",
    "TCS.NS": "Tata Consultancy Services",
    "RELIANCE.NS": "Reliance Industries",
    "HDFCBANK.NS": "HDFC Bank",
    "ICICIBANK.NS": "ICICI Bank",
    "HINDUNILVR.NS": "Hindustan Unilever Limited",
    "BHARTIARTL.NS": "Bharti Airtel",
    "KOTAKBANK.NS": "Kotak Mahindra Bank",
    "LT.NS": "Larsen & Toubro",
    "ITC.NS": "ITC Limited",
    "SBIN.NS": "State Bank of India",
    "AXISBANK.NS": "Axis Bank",
    "M&M.NS": "Mahindra & Mahindra",
    "TATAMOTORS.NS": "Tata Motors",
    "MARUTI.NS": "Maruti Suzuki India",
    "TITAN.NS": "Titan Company",
    "WIPRO.NS": "Wipro Limited",
    "ADANIGREEN.NS": "Adani Green Energy",
    "ADANIPORTS.NS": "Adani Ports and Special Economic Zone",
    "ZOMATO.NS": "Zomato Limited",
    "NESTLEIND.NS": "Nestle India",
    "ASIANPAINT.NS": "Asian Paints",
    "SUNPHARMA.NS": "Sun Pharmaceutical Industries",
    "JIOFIN.NS":"Jio Financial Services Ltd",
    "NATCOPHARM.NS":"Natco Pharma Ltd",
    "AJANTPHARM.NS":"Ajanta Pharma Limited"
}


# 1. Fetching news articles related to a stock
def fetch_news(stock_name, api_key):
    url = f'https://newsapi.org/v2/everything?q={stock_name}&apiKey={api_key}'
    response = requests.get(url)
    news_data = response.json()
    
    if 'articles' in news_data:
        articles = news_data['articles']
    else:
        print("No news articles found for this stock.")
        articles = []
    
    return articles

# 2. Load the pre-trained LLM (for news classification and sentiment analysis)
sentiment_analysis = pipeline('sentiment-analysis')
news_classifier_model_name = "distilbert-base-uncased-finetuned-sst-2-english"  # Example sentiment model
classifier = AutoModelForSequenceClassification.from_pretrained(news_classifier_model_name)
tokenizer = AutoTokenizer.from_pretrained(news_classifier_model_name)

# 3. Classify news articles and perform sentiment analysis
def analyze_news(articles):
    categorized_news = []
    for article in articles:
        # Safely get title and description, falling back to empty string if None
        title = article.get('title', '')
        description = article.get('description', '')
        
        # Make sure both title and description are treated as strings (fallback to empty string if None)
        combined_text = str(title) + " " + str(description)

        # 3.1: Sentiment Analysis
        sentiment_result = sentiment_analysis(combined_text)
        sentiment = sentiment_result[0]['label']
        
        # 3.2: Classifying the news into categories (you can later modify this part to return more specific categories)
        inputs = tokenizer(combined_text, return_tensors="pt", truncation=True, padding=True)
        outputs = classifier(**inputs)
        prediction = outputs.logits.argmax(dim=1).item()
        
        # Basic sentiment interpretation
        category = "Positive" if sentiment == 'POSITIVE' else "Negative"
        
        categorized_news.append({
            'title': title,
            'category': category,
            'sentiment': sentiment,
            'prediction': prediction,  # You can map this prediction number to actual sectors or categories
            'content': article.get('content', '')
        })
    return categorized_news

# 4. Sentiment Summary for Stock News
def analyze_sentiment_for_stock(stock_symbol, news_data):
    positive_count = 0
    negative_count = 0
    neutral_count = 0

    # Analyze sentiment for each article
    for news in news_data:
        sentiment = news['sentiment']
        if sentiment == 'POSITIVE':
            positive_count += 1
        elif sentiment == 'NEGATIVE':
            negative_count += 1
        else:
            neutral_count += 1

    print(f"Sentiment Summary for {stock_symbol}:")
    print(f"Positive news: {positive_count}")
    print(f"Negative news: {negative_count}")
    print(f"Neutral news: {neutral_count}")

    if positive_count > negative_count and positive_count > neutral_count:
        overall_sentiment = "Positive"
    elif negative_count > positive_count and negative_count > neutral_count:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"
    
    return overall_sentiment

# Main function
def main():
    # Get user input for stock symbol
    stock_symbol = input("Enter the stock symbol (e.g., AAPL, MSFT): ").upper().strip()
    
    # News API Key (replace with your actual API key)
    api_key = 'b78382314d1548f9a981d15d4fc008b6'  # Replace with your actual News API key
    
    if stock_symbol not in stock_symbol_to_name:
        print(f"Invalid stock symbol: {stock_symbol}. Please enter a valid stock symbol.")
        return
    
    stock_name = stock_symbol_to_name[stock_symbol]
    
    # Fetch the latest news articles related to the stock
    articles = fetch_news(stock_name, api_key)
    if not articles:
        return
    
    # Analyze the news articles
    news_data = analyze_news(articles)
    
    # Analyze overall sentiment for the stock's news
    overall_sentiment = analyze_sentiment_for_stock(stock_symbol, news_data)
    
    # Print the overall sentiment for the stock
    print(f"\nOverall sentiment for {stock_symbol} ({stock_name}): {overall_sentiment}")

if __name__ == "__main__":
    main()