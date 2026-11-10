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
    "Terrace View": "https://images.squarespace-cdn.com/content/v1/647f3f67a8d30515dd10eb3b/179fd6fc-4b8a-4f46-af36-84a5e1b7b477/2025.10.07_TerraceView_Exterior_001.jpg?format=500w",
    "Smiths Landing": "https://lh3.googleusercontent.com/p/AF1QipOjU9zYUJkxXeh_K94yWbwRSst4u9-cwxMDT811=s680-w680-h510-rw",
    "The Edge": "https://lh3.googleusercontent.com/p/AF1QipMtIK9ItbbQS30lYzW1oe5r_lig_yIOmMJ9R7YZ=s680-w680-h510-rw",
    "Collegiate Suites": "https://images.squarespace-cdn.com/content/v1/64b57d78e189f7418cd1ce6a/171a293f-2086-4eb7-9294-0b85c306f63c/CollegiateSuitesStudentLiving_1310HenryLn_II-4835028_PHO-28.jpg?format=1000w",
    "Fox Ridge": "https://lh3.googleusercontent.com/p/AF1QipOZS_7Mz7wMr-4AlgBM-AMs47_hnqxLEbC5SpSH=s680-w680-h510-rw",
    "The Mill": "https://s3-media0.fl.yelpcdn.com/bphoto/RMQFWGWtyKtHOui5t_JX9A/o.jpg",
    "Sundance Ridge": "https://photos.zillowstatic.com/fp/23c8004595e518b2c5c282c45f6bbeba-cc_ft_1536.jpg",
    "Maple Ridge": "https://images.squarespace-cdn.com/content/v1/64b5ab92ede2a068c43b1b4b/f96c1108-ed35-44d1-9756-ff93a04df02c/2025.10.08_MapleRidge_Pool_002.jpg?format=750w",
    "Hunters Ridge": "https://images.squarespace-cdn.com/content/v1/64b57d78e189f7418cd1ce6a/05291c6e-2662-49be-8416-3795e49cd31f/2025.10.09_CSHR_OutdoorSpace_002.jpg?format=750w",
    "Pheasant Run": "https://ssl.cdn-redfin.com/photo/154/mbphotov3/136/genMid.4487136_5.jpg",
    "The Hub": "https://huboncampus.com/blacksburg/wp-content/uploads/2024/06/gallerypage_gallery-15.jpg",
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
