from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from functools import lru_cache

app = Flask(__name__)

@lru_cache(maxsize=32)
def fetch_rss_feed(*urls):
    all_news_items = []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        items = soup.findAll('item')
        feed_name = url.split('/')[3]  # Extract feed name from the URL

        for item in items:
            news_item = {
                'feed': feed_name,
                'title': item.title.text if item.title else 'No Title',
                'link': item.link.text if item.link else 'No Link',
                'description': item.description.text if item.description else 'No Description',
                'pubDate': item.pubDate.text if item.pubDate else 'No Publication Date'
            }
            all_news_items.append(news_item)
    
    return all_news_items

@app.route('/')
def index():
    # List of feed URLs to fetch
    feed_urls = [
        "https://hnrss.org/frontpage",
        "https://hnrss.org/bestcomments",
        "https://hnrss.org/newest?points=10",
        "https://hnrss.org/best"
    ]
    # Fetch and combine items from multiple feeds
    all_items = fetch_rss_feed(*feed_urls)
    # Sort items by publication date if available
    all_items.sort(key=lambda x: x['pubDate'] if x['pubDate'] else '', reverse=True)
    return render_template('index.html', news_items=all_items)

if __name__ == '__main__':
    app.run(debug=True)
