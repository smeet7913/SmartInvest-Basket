import pandas as pd
import requests
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

# Load the CSV file
csv_file = "hello.csv"  # Update with the correct path
stocks_df = pd.read_csv(csv_file)

# Initialize sentiment analysis model
sentiment_analysis = pipeline('sentiment-analysis')
news_classifier_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
classifier = AutoModelForSequenceClassification.from_pretrained(news_classifier_model_name)
tokenizer = AutoTokenizer.from_pretrained(news_classifier_model_name)

# Function to fetch news articles
def fetch_news(stock_name, api_key):
    url = f'https://newsapi.org/v2/everything?q={stock_name}&apiKey={api_key}'
    response = requests.get(url)
    news_data = response.json()
    return news_data.get('articles', [])

# Function to analyze sentiment
def analyze_sentiment(articles):
    positive_count, negative_count, neutral_count = 0, 0, 0
    
    for article in articles:
        title = article.get('title', '')
        description = article.get('description', '')
        combined_text = f"{title} {description}".strip()
        
        if combined_text:
            sentiment_result = sentiment_analysis(combined_text)
            sentiment = sentiment_result[0]['label']
            
            if sentiment == 'POSITIVE':
                positive_count += 1
            elif sentiment == 'NEGATIVE':
                negative_count += 1
            else:
                neutral_count += 1
    
    if positive_count > negative_count:
        return "Positive"
    elif negative_count > positive_count:
        return "Negative"
    else:
        return "Neutral"

# API Key for NewsAPI (Replace with your actual key)
api_key = 'b78382314d1548f9a981d15d4fc008b6'

# Update News Sentiment in CSV
for index, row in stocks_df.iterrows():
    stock_name = row['Full Name']
    articles = fetch_news(stock_name, api_key)
    sentiment = analyze_sentiment(articles)
    stocks_df.at[index, 'News Sentiment'] = sentiment

# Save the updated CSV
stocks_df.to_csv("hello.csv", index=False)
print("Updated CSV with News Sentiment saved as 'updated_stocks.csv'")
