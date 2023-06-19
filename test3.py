import folium
import io
import requests
import telebot
import constants

def send_map_html(chat_id, bot):
    url = "https://server-for-telegram-bot.vercel.app/botCollectionsData"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

    # Create a map centered on the Poland
    m = folium.Map(location=[0, 0], zoom_start=3)

    # Loop through each meteorite and add a marker for it on the map
    for meteorite in data:
        if 'reclat' in meteorite and 'reclong' in meteorite:
            lat = float(meteorite['reclat'])
            lon = float(meteorite['reclong'])
            name = meteorite['name']
            mass = meteorite['mass']
            marker_text = f"{name}<br>Mass: {mass}"
            folium.Marker(location=[lat, lon], popup=marker_text).add_to(m)

    # Save the map as an HTML file and convert it to a byte stream
    map_html = m._repr_html_()
    map_bytes = map_html.encode()

    # Send the HTML file as a document to the chat
    bot = telebot.TeleBot(constants.TELEGRAM_KEY)
    file_like = io.BytesIO(map_bytes)
    file_like.name = 'map.html'
    bot.send_document(chat_id, file_like)
