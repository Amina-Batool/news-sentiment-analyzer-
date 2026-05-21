from flask import Flask, render_template, request, jsonify
import requests
from textblob import TextBlob
import os
from dotenv import load_dotenv
from datetime import datetime
import logging
load_dotenv()

app=Flask(__name__)

NewsApiKey=os.getenv('NEWSAPI_KEY')
NewsDataKey=os.getenv('NEWSDATA_KEY')

Categories=['business','entertainment','general','health','science','sports','technology']

def analyze_sentiment(text):
    if not text or text.strip() == '':
        return 'neutral'
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            return 'positive'
        elif polarity < 0:
            return 'negative'
        else:
            return 'neutral'
    except Exception as e:
        logging.error(f"Error analyzing sentiment: {e}")
        return 'neutral'
    
def fetch_newsapi(category):
    if not NewsApiKey:
        logging.error("NewsAPI key is missing.")
        return []
    
    try:
        url = f'https://newsapi.org/v2/everything'
        parms={
            'q':query,
            'language':'en',
            'pageSize':10,
            'apiKey': NewsApiKey
        }
        response = requests.get(url, params=parms, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get('status') == 'error':
            logging.error(f"NewsAPI error: {data.get('message')}")
            return []
        articles = []
        for article in data.get('articles', []):
            sentiment = analyze_sentiment(article.get('description', ''))
            articles.append({
                'title': article.get('title'),
                'description': article.get('description'),
                'url': article.get('url'),
                'sentiment': sentiment
            })
        return articles
    except requests.exceptions.Timeout:
        # 🛡️ EDGE CASE #6: API took too long
        logging.error("NewsAPI was too slow")
        return []
    except Exception as e:
        logging.error(f"Error fetching news from NewsAPI: {e}")
        return []
    
def fetch_newsdataapi(category):
    if not NewsDataKey:
        logging.error("NewsData key is missing.")
        return []
    
    try:
        url = f'https://newsapi.org/v2/everything'
        parms={
            'q':query,
            'language':'en',
            'pageSize':10,
            'apiKey': NewsDataKey
        }
        response = requests.get(url, params=parms, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get('status') == 'error':
            logging.error(f"NewsDataAPI error: {data.get('message')}")
            return []
        articles = []
        for article in data.get('articles', []):
            sentiment = analyze_sentiment(article.get('description', ''))
            articles.append({
                'title': article.get('title'),
                'description': article.get('description'),
                'url': article.get('url'),
                'sentiment': sentiment
            })
        return articles
    except requests.exceptions.Timeout:
        # 🛡️ EDGE CASE #6: API took too long
        logging.error("NewsDataAPI was too slow")
        return []
    except Exception as e:
        logging.error(f"Error fetching news from NewsDataAPI: {e}")
        return []
    
@app.route('/search')
def search_news():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    try:
        news1=fetch_newsapi(query)
        news2=fetch_newsdataapi(query)
        all_news = news1 + news2
        if not all_news:
            return jsonify({'error': 'No news found for the given query'}), 404
        seen_titles = set()
        unique_news = []    
        for article in all_news:
            if article['title'] not in seen_titles:
                seen_titles.add(article['title'])
                unique_news.append(article)
        
        return jsonify({'news': unique_news})
    except Exception as e:
        logging.error(f"Error in search_news: {e}")
        return jsonify({'error': 'An error occurred while fetching news'}), 500
    
@app.route('/')
def index():
    return render_template('index.html', categories=Categories)

if(__name__ == '__main__'):
    app.run(debug=True)