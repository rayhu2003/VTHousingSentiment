import os
from google import genai
from pymongo import MongoClient
import pymongo
from pymongo.server_api import ServerApi
import json
import re
from dotenv import load_dotenv

load_dotenv()

# MongoDB setup
mongo_client = pymongo.MongoClient(os.environ["MONGODB_URI"], server_api=ServerApi('1'))
db = mongo_client["VTHousing"]
collection = db["RedditReviews"]

# Google GenAI setup
gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# getsentiment from text using Gemini, return JSON

def analyze_sentiment_gemini_json(text):
    prompt = f"""
    Analyze the sentiment in the following Reddit text regarding an apartment complex.
    Return a JSON object with sentiment scores from 1 to 10 (below 5 negative, 5 neutral, above 5 positive) for:

    - maintenance
    - distance
    - environment

    Text:
    \"\"\"{text}\"\"\"

    Respond only with JSON, for example:
    {{
      "maintenance_sentiment": 7,
      "distance_sentiment": 5,
      "environment_sentiment": 3
    }}
    """
    required_keys = ("maintenance_sentiment", "distance_sentiment", "environment_sentiment")
    try:
        response = gemini_client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        # The response text should be JSON, so parse it
        response_text = response.candidates[0].content.parts[0].text.strip()
        clean_text = re.sub(r'^```json\s*|```$', '', response_text.strip(), flags=re.MULTILINE)
        sentiment_json = json.loads(clean_text)
        if not all(isinstance(sentiment_json.get(k), (int, float)) for k in required_keys):
            print(f"Incomplete sentiment JSON: {sentiment_json}")
            return None
        return sentiment_json
    except Exception as e:
        print(f"Error or invalid JSON response: {e}")
        return None

# get sentiment for a keyword, or None if there's no text or analysis fails
def get_sentiment_for_keyword(keyword):
    query = {"keyword": keyword}
    posts = list(collection.find(query))

    combined_text = "\n".join(post.get("text", "") for post in posts).strip()
    if not combined_text:
        print(f"No scraped text for '{keyword}', skipping.")
        return None

    sentiment = analyze_sentiment_gemini_json(combined_text)
    if sentiment is None:
        return None

    sentiment["source_count"] = len(posts)
    return sentiment

# list of apartment complexes to analyze
apartment_complexes = ["Terrace View", "Smiths Landing", "The Edge", "Collegiate Suites", "Fox Ridge", "The Mill", "Sundance Ridge", "Maple Ridge", "Hunters Ridge", "Pheasant Run", "The Hub"]

# analyze and save results
def run_sentiments_and_save():
    results = {}
    skipped = []

    for complex_name in apartment_complexes:
        print(f"Analyzing sentiment for: {complex_name}")
        sentiment = get_sentiment_for_keyword(complex_name)
        if sentiment is None:
            skipped.append(complex_name)
            continue
        results[complex_name] = sentiment

    # Save to JSON file
    with open("apartment_sentiments.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Sentiment analysis completed and saved to apartment_sentiments.json")
    if skipped:
        print(f"Skipped (no data or analysis failure): {', '.join(skipped)}")


if __name__ == "__main__":
    run_sentiments_and_save()