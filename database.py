import sqlite3
from contextlib import closing
from pathlib import Path
import pandas as pd

DB_PATH = Path("jobmarketanalyzer.db")


def get_connection():
    # DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with closing(get_connection()) as conn, conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                post_id TEXT NOT NULL,
                keyword TEXT NOT NULL,
                subreddit TEXT NOT NULL,
                title TEXT NOT NULL,
                body TEXT,
                url TEXT NOT NULL,
                published_at TEXT,
                fetched_at TEXT NOT NULL,
                PRIMARY KEY (post_id, keyword)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS sentiment_results (
                post_id TEXT PRIMARY KEY,
                keyword TEXT NOT NULL,
                subreddit TEXT NOT NULL,
                sentiment_label TEXT NOT NULL,
                confidence REAL NOT NULL,
                model_name TEXT NOT NULL,
                analyzed_at TEXT NOT NULL
            )
        """)


def save_posts(posts):
    if not posts:
        return
    with closing(get_connection()) as conn, conn:
        conn.executemany("""
            INSERT INTO posts (
                post_id, keyword, subreddit, title, body,
                url, published_at, fetched_at
            )
            VALUES (
                :post_id, :keyword, :subreddit, :title, :body,
                :url, :published_at, :fetched_at
            )
            ON CONFLICT(post_id, keyword) DO UPDATE SET
                fetched_at = excluded.fetched_at
        """, posts)


def save_sentiment_results(posts):
    if not posts:
        return
    with closing(get_connection()) as conn, conn:
        conn.executemany("""
            INSERT INTO sentiment_results (
                post_id, keyword, subreddit, sentiment_label,
                confidence, model_name, analyzed_at
            )
            VALUES (
                :post_id, :keyword, :subreddit, :sentiment_label,
                :confidence, :model_name, :analyzed_at
            )
        """, posts)

def load_posts(subreddits):
    if not subreddits:
        with closing(get_connection()) as conn:
            return pd.read_sql_query("SELECT * FROM posts WHERE 0", conn)

    placeholders = ", ".join("?" for _ in subreddits)

    query = f"""
        SELECT *
        FROM posts
        WHERE subreddit IN ({placeholders})
        ORDER BY published_at DESC
    """

    with closing(get_connection()) as conn:
        return pd.read_sql_query(
            query,
            conn,
            params=list(subreddits)
        )