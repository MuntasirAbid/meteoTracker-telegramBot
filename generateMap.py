import requests
import folium
import search
import io
from PIL import Image
import constants


def generate_map(country_name):
    api_key = constants.FINDCENTER_API
    url = f"https://api.opencagedata.com/geocode/v1/json?q={country_name}&key={api_key}"
    response = requests.get(url).json()

    if len(response['results']) > 0:
        geometry = response['results'][0]['geometry']
        lat, lng = geometry['lat'], geometry['lng']

    if country_name == "Russia":
        zoom = 3
    elif country_name in["United States","China"]:
        zoom = 4
    else:
        zoom = 6

    # Create a map object using the Folium library
    map = folium.Map(location=[lat, lng], zoom_start= zoom)
    matching_meteorites = search.search_meteorites_by_country(country_name)

    # Add markers to the map for each meteorite
    for meteorite_chunk in matching_meteorites:
        for meteorite in meteorite_chunk:
            # Extract the latitude, longitude, and name of the meteorite
            latitude = meteorite.get('reclat')
            longitude = meteorite.get('reclong')
            name = meteorite.get('name')

            # Add a marker for the meteorite
            folium.Marker(location=[latitude, longitude], popup=name).add_to(map)

    # Save the map as an image
    img = map._to_png()
    image_bytes = io.BytesIO(img)

    return image_bytes


def draw_map(chat_id, bot, country_name):
    # Send a message indicating that the map is being generated
    message = bot.send_message(chat_id, "Generating map...")

    # Generate the map image
    image_bytes = generate_map(country_name)

    # Open the image using Pillow
    image = Image.open(image_bytes)

    # Convert Pillow image to bytes
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        image_data = output.getvalue()

    # Send the map image as a photo
    bot.send_photo(chat_id, photo=io.BytesIO(image_data))

    # Delete the message indicating that the map is being generated
    bot.delete_message(chat_id, message.message_id)

    # Close the bytes buffer
    image_bytes.close()
