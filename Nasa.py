import requests
import json
from time import sleep

import constants


# Function to get the country name from coordinates using LocationIQ API
def get_country_name(latitude, longitude, api_key):
    url = f"https://us1.locationiq.com/v1/reverse.php?key={api_key}&lat={latitude}&lon={longitude}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        address = data.get("address")
        if address:
            country = address.get("country")
            if country:
                return country


# Define LocationIQ API key
api_key = constants.LOCATION_API

# Make request to NASA meteorite API
url = "https://data.nasa.gov/resource/y77d-th95.json"
response = requests.get(url)

# Process meteorite data and add country name
if response.status_code == 200:
    data = response.json()
    sorted_data = sorted(data, key=lambda x: float(x.get("mass", "0")) if x.get("mass") and x.get("mass").replace(',',
                                                                                                                  '').replace(
        '.', '').isdigit() else 0, reverse=True)

    for meteor in sorted_data[:200]:
        latitude = meteor.get("reclat")
        longitude = meteor.get("reclong")
        if latitude and longitude:
            country = get_country_name(latitude, longitude, api_key)
            meteor["country"] = country
        sleep(1)  # Add sleep to avoid exceeding rate limit

    with open('met_datacountry.json', 'w') as outfile:
        json.dump(sorted_data[:200], outfile)

    print("Data saved to met_data.json")
else:
    print("Error retrieving data from API")
