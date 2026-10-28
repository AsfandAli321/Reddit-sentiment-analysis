import feedparser
import requests
import re
from bs4 import BeautifulSoup
from pprint import pprint
from database import *
import datetime
from sentiment import SentimentAnalyzer

def main():
    initialize_database()
    #enable after incoperating streamlit dashboard
    # posts = fetch_posts()

    # Load posts already collected and saved in SQLite.
    subreddits = ['r/cscareerquestions', 'r/developersPak/']
    posts = load_posts(subreddits)
    if posts.empty:
        print("No posts found. Run fetch_posts.py first.")
        return
    print(f"Fetched {len(posts)} posts.")

    print(f"Analyzing {len(posts)} posts...")

    # if not posts.empty:
    #     analyzer = SentimentAnalyzer()
    #     results = analyzer.analyze(posts)

    #     # Display the first 10 predictions.
    #     for result in results[:50]:
    #         print(
    #             f"{result['sentiment']} "
    #             f"({result['confidence']}) | "
    #             f"{result['title']}"
    #         )

    # 3. Save the collected posts to SQLite.
    save_posts(posts)

    # print("Posts saved to the database.")

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



if __name__ == '__main__':
    main()