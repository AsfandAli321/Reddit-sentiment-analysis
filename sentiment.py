import numpy as np
from transformers import pipeline

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"


class SentimentAnalyzer:
    def __init__(self):
        print("Loading sentiment model...")

        self.classifier = pipeline(
            "text-classification",
            model=MODEL_NAME,
            device=-1,  # Run on CPU
        )

    def analyze(self, posts):
        if posts.empty:
            return []

        posts_dict = posts.to_dict("records")  # list of dicts, one per post

        texts = [
            # f"{post.title}. {post.body or ''}"
            # for post in posts
            f"{post['title']}. {post['body'] or ''}"
            for post in posts_dict
        ]


        predictions = self.classifier(
            texts,
            batch_size=8,
            truncation=True,
            max_length=512,
        )

        results = []

        for post, prediction in zip(posts_dict, predictions):
            results.append({
                "post_id": post["post_id"],
                "keyword": post["keyword"],
                "subreddit": post["subreddit"],
                "title": post["title"],
                "sentiment": prediction["label"],
                "confidence": np.round( float(prediction["score"]), 4 ),
            })

        return results
