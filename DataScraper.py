import os
import praw
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv(override=True)

# --- MongoDB setup ---
mongo_client = pymongo.MongoClient(os.environ["MONGODB_URI"], server_api=ServerApi('1'))
db = mongo_client["VTHousing"]
collection = db["collection"]

# --- Reddit API setup ---
reddit = praw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    user_agent="VTHousingScraper"
)

# --- Subreddits & keywords ---
subs = ["VirginiaTech", "Blacksburg"]
keywords = ["Terrace View", "Smiths Landing", "The Edge", "Collegiate Suites", "Fox Ridge", "The Mill", "Sundance Ridge", "Maple Ridge", "Hunters Ridge", "Pheasant Run", "The Hub"]

for sub in subs:
    subreddit = reddit.subreddit(sub)
    for kw in keywords:
        print(f"\nSearching '{kw}' in r/{sub}...")
        for post in subreddit.search(kw, limit=10):  # limit small for testing
            if collection.find_one({"type": "post", "id": post.id, "keyword": kw}):
                print(f"Post '{post.title}' already in DB, skipping comments and post.")
                continue  # skip duplicate post and comments
            post_doc = {
                "type": "post",
                "id": post.id,
                "subreddit": sub,
                "keyword": kw,
                "title": post.title,
                "text": post.selftext,
                "url": post.url
            }
            collection.insert_one(post_doc)  # save post

            # --- Scrape comments ---
            post.comments.replace_more(limit=0)
            for comment in post.comments[:5]:  # grab top 5 comments
                comment_doc = {
                    "type": "comment",
                    "id": comment.id,
                    "parent_post_id": post.id,
                    "subreddit": sub,
                    "keyword": kw,
                    "parent_post": post.title,
                    "text": comment.body,
                    "url": f"https://reddit.com{comment.permalink}"
                }
                collection.insert_one(comment_doc)
