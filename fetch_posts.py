import feedparser
import requests
import re
from bs4 import BeautifulSoup
import datetime
from database import *

def main():
    query_list = ['Job', 'AI', 'layoffs', 'claude', 'salary', 'hiring']
    print("Select a keyword for the reddit search:")
    for i,keyword in enumerate(query_list):
        print (i,keyword)
    while True:
        user_query_choice = input('>')
        if user_query_choice.isdigit() and int(user_query_choice) < len(query_list):
            user_query_choice = query_list[int(user_query_choice)]
            print("keyword selected")
            break
        print('enter a valid num.')

    subreddit_list = ['r/developersPak', 'r/PakistaniDevs/', 'r/csCareerQuestions']
    print("Select a subbredit:")
    for i,subreddit in enumerate(subreddit_list):
        print (i,subreddit)
    while True:
        user_subreddit_choice = input('>')
        if user_subreddit_choice.isdigit() and int(user_subreddit_choice) < len(subreddit_list):
            user_subreddit_choice = subreddit_list[int(user_subreddit_choice)]
            print("subreddit selected")
            break
        print("enter a valid num")
    print(f'search set for {user_query_choice} in {user_subreddit_choice}')


    country_list = ['pakistan', 'europe/', 'india']
    print("Select a country:")
    for i,country in enumerate(country_list):
        print (i,country)
    while True:
        user_subreddit_choice = input('>')
        if user_subreddit_choice.isdigit() and int(user_subreddit_choice) < len(subreddit_list):
            user_subreddit_choice = subreddit_list[int(user_subreddit_choice)]
            print("subreddit selected")
            break
        print("enter a valid num")
    print(f'search set for {user_query_choice} in {user_subreddit_choice}')



    posts = fetch_posts(user_query_choice, user_subreddit_choice)
    # print(posts[0])
    save_posts(posts)

def fetch_posts(query, subreddit):
    posts = []

    # query = "job"
    # subreddit = "r/developersPak"

    headers = {
        'User-Agent': 'python:jobmarketanalyzer:v1.0 (by /u/Extra_solar)'
    }

    url = f"https://www.reddit.com/{subreddit}/search.rss?q={query}&restrict_sr=on&t=month&limit=200"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        feed = feedparser.parse(response.content)
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
        print(f" fetched {len(feed.entries)} posts live")
        return posts

    else:
        print(f"Failed with status code: {response.status_code}")

if __name__ == '__main__':
    main()