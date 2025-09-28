from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load your JSON data
with open('sentiments.json') as f:
    raw_data = json.load(f)

# include images for apartments
image_urls = {
    "Terrace View": "https://lh3.googleusercontent.com/p/AF1QipODLbecf7KofzJQAt-Rjnw8sNut33t7YZ8rOKqN=s680-w680-h510-rw",
    "Smiths Landing": "https://lh3.googleusercontent.com/p/AF1QipOjU9zYUJkxXeh_K94yWbwRSst4u9-cwxMDT811=s680-w680-h510-rw",
    "The Edge": "https://lh3.googleusercontent.com/p/AF1QipMtIK9ItbbQS30lYzW1oe5r_lig_yIOmMJ9R7YZ=s680-w680-h510-rw",
    "Collegiate Suites": "https://images.squarespace-cdn.com/content/v1/64b57d78e189f7418cd1ce6a/171a293f-2086-4eb7-9294-0b85c306f63c/CollegiateSuitesStudentLiving_1310HenryLn_II-4835028_PHO-28.jpg?format=1000w",
    "Fox Ridge": "https://lh3.googleusercontent.com/p/AF1QipOZS_7Mz7wMr-4AlgBM-AMs47_hnqxLEbC5SpSH=s680-w680-h510-rw",
    "The Mill": "https://lh3.googleusercontent.com/p/AF1QipPVGFTwlEux_N0-NLpOKnScBumM1tENVl4T5CM8=s680-w680-h510-rw",
    "Sundance Ridge": "https://images1.apartments.com/i2/kSpHpXjlWrAtbZlObW3Mw7GkR42xb6ippC1PvQu2VpE/111/sundance-ridge-blacksburg-va-primary-photo.jpg",
    "Maple Ridge": "https://mapleridgeessex.com/wp-content/uploads/2021/11/MapleRidgeAssistedLiving-15-e1636149499526.jpg",
    "Hunters Ridge": "https://images1.forrent.com/i2/MuXn2UdutanfqfF7xnMWdwYkv4YFO-Kh44_AeT7qFYQ/112/image.jpg?p=1",
    "Pheasant Run": "https://ssl.cdn-redfin.com/photo/154/mbphotov3/136/genMid.4487136_5.jpg",
    "The Hub": "https://huboncampus.com/blacksburg/wp-content/uploads/2024/06/homepage_Hero-Image-3.jpg",
}

website_urls = {
    "Terrace View": "https://terraceviewblacksburg.com",
    "Smiths Landing": "https://www.smithslandingapartments.com",
    "The Edge": "https://www.cmgleasing.com/office/the-edge",
    "Collegiate Suites": "https://collegiatesuitesblacksburg.com",
    "Fox Ridge": "https://www.foxridgeliving.com",
    "The Mill": "https://www.blacksburgmill.com",
    "Sundance Ridge": "https://www.nestrealty.com/new_river_valley/neighborhood-guides/sundance_ridge",
    "Maple Ridge": "https://mapleridgeblacksburg.com",
    "Hunters Ridge": "https://collegiatesuitesblacksburg.com",
    "Pheasant Run": "https://pheasantrunblacksburg.com",
    "The Hub": "https://huboncampus.com/blacksburg",
}

# Transform dict into list with overall sentiment added
data = []
for location, sentiments in raw_data.items():
    overall = round(
        (sentiments.get('maintenance_sentiment', 0) +
         sentiments.get('distance_sentiment', 0) +
         sentiments.get('environment_sentiment', 0)) / 3, 2)
    
    entry = {
        "image_url": image_urls.get(location, ""),
        "location": location,
        **sentiments,
        "overall_sentiment": overall,
        "website_url": website_urls.get(location, "")
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
    
    sorted_data = sorted(data, key=lambda x: x.get(sort_field, 0), reverse=True) 
    
    return jsonify(sorted_data)


if __name__ == '__main__':
    app.run(debug=True)
