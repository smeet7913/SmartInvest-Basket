import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER lexicon for sentiment analysis
nltk.download('vader_lexicon')

def get_yahoo_finance_news_from_url(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news_data = []
    
    for item in soup.find_all('h3'):
        headline = item.text.strip()
        link_tag = item.find('a')
        if link_tag and 'href' in link_tag.attrs:
            link = link_tag['href']
            if not link.startswith("http"):
                link = "https://finance.yahoo.com" + link
            news_data.append((headline, link))

    return news_data

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)['compound']  # VADER returns score from -1 (negative) to +1 (positive)

def get_stock_sentiment_from_url(url):
    news_list = get_yahoo_finance_news_from_url(url)

    if not news_list:
        return "No recent news found."

    sentiment_scores = [analyze_sentiment(news[0]) for news in news_list]
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)

    return f"Sentiment Score for the given stock URL: {avg_sentiment:.2f}"

# Example Usage with the provided URL
url = "https://finance.yahoo.com/quote/TCS.NS/news/"
print(get_stock_sentiment_from_url(url))
