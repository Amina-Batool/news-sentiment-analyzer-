from flask import Flask, render_template, request, jsonify
import requests
from textblob import TextBlob
import os
from dotenv import load_dotenv
from datetime import datetime
import logging
load_dotenv()

app=Flask(__name__)
@app.after_request
def add_no_cache(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

NewsApiKey=os.getenv('NEWSAPI_KEY')
NewsDataKey=os.getenv('NEWSDATA_KEY')

Categories=['business','entertainment','general','health','science','sports','technology']

def analyze_sentiment(text):
    """
    This function takes a sentence and tells you if it's happy or sad.
    Example: "Apple released a new phone" → positive 😊
             "Earthquake destroyed city" → negative 😞
    """
    
    # 🛡️ EDGE CASE #1: What if text is empty? (User gave no news)
    if not text or len(text.strip()) == 0:
        return {'score': 0, 'label': 'neutral'}  # Can't analyze nothing
    
    try:
        # TextBlob does the magic
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # Number from -1 (sad) to +1 (happy)
        
        # Convert number to words
        if polarity > 0.1:
            label = 'positive'   # 😊
        elif polarity < -0.1:
            label = 'negative'   # 😞
        else:
            label = 'neutral'    # 😐
        
        return {
            'score': round(polarity, 2),
            'label': label
        }
    except Exception as e:
        # 🛡️ EDGE CASE #2: TextBlob crashes (very rare)
        return {'score': 0, 'label': 'neutral'}
    
def fetch_news_from_newsapi(query):
    """
    Call NewsAPI.org and ask for news about 'query'
    Example: query = "iPhone" → gets 10 news articles about iPhone
    """
    
    # 🛡️ EDGE CASE #3: No API key found
    if not NewsApiKey:
        return []  # Return empty list
    
    try:
        url = "https://newsapi.org/v2/everything"
        
        params = {
            'q': query,           # What to search for
            'language': 'en',     # English only
            'pageSize': 10,       # Get 10 articles
            'apiKey': NewsApiKey  # Your library card
        }
        
        # 🛡️ EDGE CASE #4: API is SLOW (timeout after 5 seconds)
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()  # Will crash if error (404, 500)
        
        data = response.json()  # Convert to Python dictionary
        
        # 🛡️ EDGE CASE #5: API returns an error message
        if data.get('status') == 'error':
            return []
        
        articles = []
        for article in data.get('articles', []):
            # Each article is a dictionary with keys: title, description, url, etc.
            
            # Get each field, or use default if missing
            title = article.get('title', 'No title')
            description = article.get('description', 'No description')
            url = article.get('url', '#')
            image = article.get('urlToImage', 'https://via.placeholder.com/300x200?text=No+Image')
            source = article.get('source', {}).get('name', 'Unknown')
            published_at = article.get('publishedAt', '')[:10]  # Just the date part
            
            # Ask: Is this news happy or sad?
            sentiment = analyze_sentiment(f"{title} {description}")
            
            articles.append({
                'title': title[:100],  # Don't let title be too long
                'description': description[:200],
                'url': url,
                'image': image,
                'source': source,
                'published_at': published_at,
                'sentiment': sentiment,
                'api_source': 'NewsAPI'
            })
        
        return articles
        
    except requests.exceptions.Timeout:
        # 🛡️ EDGE CASE #6: API took too long
        print("NewsAPI was too slow")
        return []
    except Exception as e:
        # 🛡️ EDGE CASE #7: Any other error (no internet, etc.)
        print(f"Error: {e}")
        return []
    
def fetch_news_from_newsdata(query):
    """Same as above, but calls NewsData.io instead"""
    
    if not NewsDataKey:
        return []
    
    try:
        url = "https://newsdata.io/api/1/news"
        params = {
            'q': query,
            'language': 'en',
            'apikey': NewsDataKey
        }
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'error':
            return []
        
        articles = []
        for article in data.get('results', [])[:10]:
            title = article.get('title', 'No title')
            description = article.get('description', 'No description')
            
            sentiment = analyze_sentiment(f"{title} {description}")
            
            articles.append({
                'title': title[:100],
                'description': description[:200] if description else 'No description',
                'url': article.get('link', '#'),
                'image': article.get('image_url', 'https://via.placeholder.com/300x200?text=No+Image'),
                'source': article.get('source_id', 'Unknown'),
                'published_at': article.get('pubDate', '')[:10],
                'sentiment': sentiment,
                'api_source': 'NewsData'
            })
        
        return articles
        
    except Exception as e:
        print(f"NewsData error: {e}")
        return []
    
@app.route('/search')
def search():
    """
    This runs when user types something and clicks Search.
    Example URL: http://localhost:5000/search?query=iPhone
    """
    
    # Get what user typed (from the URL)
    query = request.args.get('query', '').strip()
    category = request.args.get('category', '')
    
    # 🛡️ EDGE CASE #8: User typed nothing or just 1 letter
    if not query or len(query) < 2:
        return jsonify({
            'success': False,
            'message': 'Please enter at least 2 characters'
        }), 400
    
    try:
        # Get news from BOTH APIs
        news1 = fetch_news_from_newsapi(query)
        news2 = fetch_news_from_newsdata(query)
        
        # Combine them
        all_news = news1 + news2
        
        # 🛡️ EDGE CASE #9: No news found at all
        if not all_news:
            return jsonify({
                'success': False,
                'message': f'No news found for "{query}"'
            }), 404
        
        # 🛡️ EDGE CASE #10: Remove duplicate articles (same title)
        seen_titles = set()
        unique_news = []
        for article in all_news:
            if article['title'] not in seen_titles:
                seen_titles.add(article['title'])
                unique_news.append(article)
        
        # Send back to the webpage
        return jsonify({
            'success': True,
            'articles': unique_news[:20]  # Max 20 articles
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Something went wrong'
        }), 500
    
@app.route('/')
def index():
    """Show the homepage (the search box)"""
    return render_template('index.html', categories=Categories)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)