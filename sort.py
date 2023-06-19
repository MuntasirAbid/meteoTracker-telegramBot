import json
import requests
import time
import constants

# LocationIQ API endpoint
api_endpoint = "https://us1.locationiq.com/v1/reverse.php"

# LocationIQ API key
api_key = constants.LOCATION_API

# Read the input JSON file
with open("C:\\Users\\dagna\\PycharmProjects\\pythonProject\\venv\\met_data.json", "r") as f:
    data = json.load(f)

# Loop through the data and extract the coordinates
for item in data:
    lat = item["reclat"]
    lon = item["reclong"]

    # Make a request to the LocationIQ API
    params = {
        "key": api_key,
        "lat": lat,
        "lon": lon,
        "format": "json"
    }
    response = requests.get(api_endpoint, params=params)

    # Parse the response and add the location to the item
    location = json.loads(response.text)
    item["location"] = location

    # Wait for 1 second before making the next request
    time.sleep(1)

# Write the output JSON file
with open("output.json", "w") as f:
    json.dump(data, f)