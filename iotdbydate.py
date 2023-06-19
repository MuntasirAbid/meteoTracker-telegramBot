import requests
from PIL import Image
from io import BytesIO
import constants


def iotd_by_date(bot, chat_id, date):
    # NASA API endpoint for the image of the day
    url = "https://api.nasa.gov/planetary/apod"

    # Parameters for the API request
    params = {
        "api_key": constants.NASA_API_KEY,
        "date": date,
        "hd": "True"  # Get the high-definition version of the image
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Parse the response JSON
    data = response.json()

    # Get the URL of the image
    image_url = data["hdurl"]

    # Download the image
    response = requests.get(image_url)

    # Load the image into a PIL Image object
    image = Image.open(BytesIO(response.content))

    # Resize the image to meet Telegram's requirements
    max_size = (1280, 1280)
    image.thumbnail(max_size)

    # Send the image to the bot
    with BytesIO() as bio:
        bio.name = 'image.jpeg'
        image.save(bio, 'JPEG')
        bio.seek(0)
        bot.send_photo(chat_id, photo=bio, caption=data["title"])
