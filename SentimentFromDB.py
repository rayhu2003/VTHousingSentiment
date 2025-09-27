from google import genai
from pymongo import MongoClient
import pymongo
from pymongo.server_api import ServerApi
import json
import re

# MongoDB setup
uri = "mongodb+srv://user1:1@cluster0.mtu1bhc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
db = client["VTHousing"]
collection = db["collection"]

# Google GenAI setup
client = genai.Client(api_key="AIzaSyDOMYtROTuFF7KoIRNRU0G3Rk6fbEipBjk")

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
    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        # The response text should be JSON, so parse it
        response_text = response.candidates[0].content.parts[0].text.strip()
        clean_text = re.sub(r'^```json\s*|```$', '', response_text.strip(), flags=re.MULTILINE)
        sentiment_json = json.loads(clean_text)
        return sentiment_json
    except Exception as e:
        print(f"Error or invalid JSON response: {e}")
        # Return neutral fallback
        return {
            "maintenance_sentiment": 5,
            "distance_sentiment": 5,
            "environment_sentiment": 5
        }
    
# get setiment from a posts about a keyword
def get_sentiment_for_keyword(keyword):
    query = {"keyword": keyword}
    posts = collection.find(query)

    # combine texts from all posts/comments about the keyword
    combined_text = ""
    for post in posts:
        combined_text += post.get("text", "") + "\n"

    # Analyze sentiment for the combined text
    return analyze_sentiment_gemini_json(combined_text)

# list of apartment complexes to analyze
apartment_complexes = ["Terrace View", "Smiths Landing", "The Edge", "Collegiate Suites", "Fox Ridge", "The Mill", "Sundance Ridge", "Maple Ridge", "Hunters Ridge", "Pheasant Run", "The Hub"]

# analyze and save results
def run_sentiments_and_save():
    results = {}

    for complex_name in apartment_complexes:
        print(f"Analyzing sentiment for: {complex_name}")
        sentiment = get_sentiment_for_keyword(complex_name)
        results[complex_name] = sentiment

    # Save to JSON file
    with open("apartment_sentiments.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Sentiment analysis completed and saved to apartment_sentiments.json")


if __name__ == "__main__":
    run_sentiments_and_save()