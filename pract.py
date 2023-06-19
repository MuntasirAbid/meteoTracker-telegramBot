import json

# Load the meteorite data from the JSON file
with open('C:\\Users\\dagna\\PycharmProjects\\pythonProject\\venv\\met_datacountry.json') as infile:
    meteorite_data = json.load(infile)

# Get the country name from the user
country_name = input("Enter a country name: ")

# Loop through the meteorite data and find the meteorites that fell in the specified country
matching_meteorites = []
for meteorite in meteorite_data:
    if meteorite.get("country") == country_name:
        matching_meteorites.append(meteorite)

# Display the matching meteorites
if matching_meteorites:
    print(f"Found {len(matching_meteorites)} meteorites that fell in {country_name}:")
    for meteorite in matching_meteorites:
        print(meteorite)
else:
    print(f"No meteorites found that fell in {country_name}.")
