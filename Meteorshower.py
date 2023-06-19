import requests
import json
import datetime

import constants

# Enter your API key here
API_KEY = 'siHcxeFTUwq6b8LgyqjbmXgND13bvqnqbLlgRjRz'

# Define the API endpoint
API_ENDPOINT = "https://api.nasa.gov/planetary/meteor/showers"

# Define the current year
now = datetime.datetime.now()
year = now.year

# Fetch the meteor shower data for the current year
response = requests.get(API_ENDPOINT, params={"api_key": API_KEY, "year": year})
data = json.loads(response.text)

# Display the meteor shower dates and times
for shower in data:
    print(shower["name"])
    for peak in shower["peak"]:
        date = datetime.datetime.strptime(peak, "%Y-%m-%d %H:%M:%S")
        print(date.strftime("%b %d %Y %I:%M %p"))
    print("--------------------")
