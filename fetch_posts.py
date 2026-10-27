import feedparser
import requests
import re
from bs4 import BeautifulSoup
import datetime
from database import *

def main():
    query_list = ['Job', 'AI', 'layoff', 'claude']
    print("Select a keyword for the reddit search:")
    for keyword,i in zip( query_list, range(0,len(query_list)) ):
        print (i,keyword)
    user_query_choice = int( input() )
    user_query_choice = query_list[user_query_choice]

    subreddit_list = ['r/developersPak', 'r/csCareerQuestions']
    print("Select a subbredit:")
    for subreddit,i in zip( subreddit_list, range(0,len(subreddit_list)) ):
        print (i,subreddit)
    user_subreddit_choice = int(input())
    user_subreddit_choice = subreddit_list[user_subreddit_choice]
    
    print(f'searching for {user_query_choice} in {user_subreddit_choice}')
    # posts = fetch_posts()
    # print(posts[0])
    # save_posts(posts)

def fetch_posts():
    posts = []

    query = "job"
    subreddit = "r/developersPak"

    headers = {
        'User-Agent': 'python:jobmarketanalyzer:v1.0 (by /u/Extra_solar)'
    }

    url = f"https://www.reddit.com/{subreddit}/search.rss?q={query}&restrict_sr=on&t=month&limit=200"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        feed = feedparser.parse(response.content)
        print(f" fetched {len(feed.entries)} posts live")
        for post in feed.entries:
            # 1. Pass the messy HTML summary to BeautifulSoup
            soup = BeautifulSoup(post.summary, "html.parser")
            clean_text = soup.get_text(separator=" ", strip=True)

            # 2. Use regex to strip the Reddit metadata at the end
            # \S+ matches any username (one or more non-whitespace characters)
            clean_text = re.sub(r"submitted by /u/\S+ \[link\] \[comments\]", "", clean_text).strip()
            
            post_db = {
                "post_id": post.id,
                "keyword": query, 
                "subreddit": post.tags[0].label,
                "title": post.title,
                "body": clean_text,
                "url": post.link,
                "published_at": post.published,
                "fetched_at": datetime.datetime.now().isoformat()
            }
            print("Title:", post.title)
            print("body:", clean_text)
            print("-" * 50)
            posts.append(post_db)
        return posts

    else:
        print(f"Failed with status code: {response.status_code}")

if __name__ == '__main__':
    main()