import requests
import more_itertools

url = "https://server-for-telegram-bot.vercel.app/botCollectionsData"
response = requests.get(url)
meteorite_data = response.json()


def search_meteorites_by_country(country_name):

    # Loop through the meteorite data and find the meteorites that fell in the specified country
    matching_meteorites = []
    for meteorite in meteorite_data:
        if meteorite.get("country") == country_name:
            matching_meteorites.append(meteorite)

    matching_meteorites_chunks = list(more_itertools.chunked(matching_meteorites, 1))

    return matching_meteorites_chunks
