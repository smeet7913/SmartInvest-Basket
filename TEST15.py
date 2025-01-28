import requests
import csv
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

# 1. Fetching news articles related to a stock
def fetch_news(stock_name, api_key):
    url = f'https://newsapi.org/v2/everything?q={stock_name}&apiKey={api_key}'
    response = requests.get(url)
    news_data = response.json()
    
    if 'articles' in news_data:
        articles = news_data['articles']
    else:
        print(f"No news articles found for {stock_name}.")
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
    # News API Key (replace with your actual API key)
    api_key = 'b78382314d1548f9a981d15d4fc008b6'  # Replace with your actual News API key
    
    # Read stock symbols and names from CSV file
    with open('hello.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            stock_symbol = row['Stock Symbol']
            stock_name = row['Full Name']
            
            # Append .NS to the stock symbol for Indian stocks
            stock_symbol_ns = f"{stock_symbol}.NS"
            
            print(f"\nProcessing {stock_symbol_ns} ({stock_name})...")
            
            # Fetch the latest news articles related to the stock
            articles = fetch_news(stock_name, api_key)
            if not articles:
                continue
            
            # Analyze the news articles
            news_data = analyze_news(articles)
            
            # Analyze overall sentiment for the stock's news
            overall_sentiment = analyze_sentiment_for_stock(stock_symbol_ns, news_data)
            
            # Print the overall sentiment for the stock
            print(f"Overall sentiment for {stock_symbol_ns} ({stock_name}): {overall_sentiment}")

if __name__ == "__main__":
    main()