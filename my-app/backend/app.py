from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load your JSON data
with open('sentiments.json') as f:
    raw_data = json.load(f)

# Transform dict into list with overall sentiment added
data = []
for location, sentiments in raw_data.items():
    overall = round(
        (sentiments.get('maintenance_sentiment', 0) +
         sentiments.get('distance_sentiment', 0) +
         sentiments.get('environment_sentiment', 0)) / 3, 2)
    
    entry = {
        "location": location,
        **sentiments,
        "overall_sentiment": overall
    }
    data.append(entry)

valid_sort_keys = {
    'maintenance': 'maintenance_sentiment',
    'distance': 'distance_sentiment',
    'environment': 'environment_sentiment',
    'overall': 'overall_sentiment'
}

@app.route('/sort', methods=['GET'])
def sort_locations():
    sort_key = request.args.get('by', 'overall').lower()
    sort_field = valid_sort_keys.get(sort_key)
    
    if not sort_field:
        return jsonify({
            "error": f"Invalid sort key. Use one of {list(valid_sort_keys.keys())}"
        }), 400
    
    sorted_data = sorted(data, key=lambda x: x.get(sort_field, 0), reverse=True)  # Descending order
    
    return jsonify(sorted_data)


if __name__ == '__main__':
    app.run(debug=True)
