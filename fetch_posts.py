import feedparser
import requests
import re
from bs4 import BeautifulSoup
import datetime
from database import *

posts = fetch_posts()


def fetch_posts():
    posts = []

    headers = {
        'User-Agent': 'python:jobmarketanalyzer:v1.0 (by /u/Extra_solar)'
    }

    url = "https://www.reddit.com/r/developersPak/search.rss?q=job&restrict_sr=on&t=month&limit=200"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        feed = feedparser.parse(response.content)
        # pprint(response)
        print(f" fetched {len(feed.entries)} posts live")
        for post in feed.entries:
            print("Title:", post.title)
            
            # 1. Pass the messy HTML summary to BeautifulSoup
            soup = BeautifulSoup(post.summary, "html.parser")
            clean_text = soup.get_text(separator=" ", strip=True)

            # 2. Use regex to strip the Reddit metadata at the end
            # \S+ matches any username (one or more non-whitespace characters)
            clean_text = re.sub(r"submitted by /u/\S+ \[link\] \[comments\]", "", clean_text).strip()
            
            post_db = {
                "post_id": post.id,
                "keyword": "job", 
                "subreddit": post.tags[0].label,
                "title": post.title,
                "body": clean_text,
                "url": post.link,
                "published_at": post.published,
                "fetched_at": datetime.datetime.now().isoformat()
            }

            posts.append(post_db)
        return posts

    else:
        print(f"Failed with status code: {response.status_code}")

