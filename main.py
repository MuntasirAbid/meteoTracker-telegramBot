import folium
import webbrowser
import requests

url = "https://server-for-telegram-bot.vercel.app/botCollectionsData"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

# Create a map centered on the Poland
m = folium.Map(location=[51.9194, 19.1451], zoom_start=6)

# Loop through each meteorite and add a marker for it on the map
for meteorite in data:
    if 'reclat' in meteorite and 'reclong' in meteorite:
        lat = float(meteorite['reclat'])
        lon = float(meteorite['reclong'])
        name = meteorite['name']
        mass = meteorite['mass']
        marker_text = f"{name}<br>Mass: {mass}"
        folium.Marker(location=[lat, lon], popup=marker_text).add_to(m)

# Save the map as an HTML file and open it in a web browser
m.save('map.html')
webbrowser.open('map.html')
