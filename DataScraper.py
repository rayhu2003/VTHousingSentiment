import praw
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# --- MongoDB setup ---
uri = "mongodb+srv://user1:1@cluster0.mtu1bhc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
db = client["VTHousing"]
collection = db["RedditReviews"]

# --- Reddit API setup ---
reddit = praw.Reddit(
    client_id="h73r7mq7xBIRsOvaK2BSUw",
    client_secret="y5NeC8ALHecpPhnqvSSQMXwZEdt5GQ",
    user_agent="VTHousingScraper"
)

# --- Subreddits & keywords ---
subs = ["VirginiaTech", "Blacksburg"]
# housing", "apartment", "dorm", "Cochrane", "Pritchard", "Terrace View", "Smiths Landing", "On Campus", "The Edge"
keywords = ["Collegiate Suites", "Fox Ridge", "The Mill", "Sundance Ridge", "Maple Ridge", "Hunters Ridge", "Pheasant Run", "The Hub"]

for sub in subs:
    subreddit = reddit.subreddit(sub)
    for kw in keywords:
        print(f"\nSearching '{kw}' in r/{sub}...")
        for post in subreddit.search(kw, limit=10):  # limit small for testing
            if collection.find_one({"type": "post", "id": post.id}):
                print(f"Post '{post.title}' already in DB, skipping comments and post.")
                continue  # skip duplicate post and comments
            post_doc = {
                "type": "post",
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
                    "subreddit": sub,
                    "keyword": kw,
                    "parent_post": post.title,
                    "text": comment.body,
                    "url": f"https://reddit.com{comment.permalink}"
                }
                collection.insert_one(comment_doc)
