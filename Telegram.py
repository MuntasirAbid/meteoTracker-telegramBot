import telebot
# import Nasa
import constants
import search
import logging
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import generateMap
import IOTD
import iotdbydate

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Create a new bot instance
bot = telebot.TeleBot(constants.TELEGRAM_KEY)

# Add a log message when the bot successfully connects to the Telegram servers
logging.info("Bot started and connected to Telegram servers")
# Define the menu button
# menu_button = KeyboardButton('/menu')

# Create a custom keyboard with buttons
keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keyboard.add(
    KeyboardButton('/start'), KeyboardButton('/help'),
    KeyboardButton('/search'), KeyboardButton('/map'),
    KeyboardButton('/interactivemap'), KeyboardButton('/Image_of_The_Day'),
    KeyboardButton('/Iotd_by_date')
)


# keyboard.add(menu_button)


# Define a handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello, welcome to my bot!", reply_markup=keyboard)


# Define a handler for the /send command
@bot.message_handler(commands=['send'])
def send_message(message):
    bot.send_message(message.chat.id, "Hello, this is a message from my bot!")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, constants.help_text)


# Define a handler for the /stop command
@bot.message_handler(commands=['stop'])
def stop_bot(message):
    bot.reply_to(message, "Stopping bot...")
    bot.stop_polling()


# Define a handler for the /search command
@bot.message_handler(commands=['search'])
def search_meteorites(message):
    # Ask the user to enter a country name
    bot.send_message(message.chat.id, "Please enter a country name:")

    # Define an inner function to handle the user's input
    def handle_country_name(message):

        # Call the search_meteorites_by_country function to get the matching meteorites
        country_name = message.text
        matching_meteorites_chunks = search.search_meteorites_by_country(country_name)

        table = "Name\tID\tYear\tMass (g)\n"
        for chunk in matching_meteorites_chunks:
            for meteorite in chunk:
                year = meteorite['year'].split('-')[0]

                meteorite_data = f"Name: {meteorite['name']}\nID: {meteorite['id']}\nYear: {year}\nMass: {meteorite['mass']}"

                bot.send_message(message.chat.id, meteorite_data)

            # Set the handler for the user's input

    # Set the handler for the user's input
    bot.register_next_step_handler(message, handle_country_name)


@bot.message_handler(commands=['map'])
def send_map(message):
    bot.send_message(message.chat.id, "Please enter a country name:")

    def handle_country_name(message):
        country_name = message.text
        # Call the `draw_map` function and pass the `chat_id`, `bot` object, and `country_name`
        generateMap.draw_map(message.chat.id, bot, country_name)

    # Set the `handle_country_name` function as the callback for the next message that the user sends
    bot.register_next_step_handler(message, handle_country_name)


@bot.message_handler(commands=['interactivemap'])
def send_interactivemap(message):
    bot.send_message(message.chat.id, "https://brook-ayanaw.github.io/Telegram-Bot/")


@bot.message_handler(commands=['Image_of_The_Day'])
def send_iotd(message):
    IOTD.iotd(bot, message.chat.id)


@bot.message_handler(commands=['Iotd_by_date'])
def send_iotdbydate(message):
    bot.send_message(message.chat.id, "Please enter a Date: (YYYY-MM-DD)")

    def handle_date(message):
        date = message.text

        iotdbydate.iotd_by_date(bot, message.chat.id, date)

        # Set the `handle_country_name` function as the callback for the next message that the user sends

    bot.register_next_step_handler(message, handle_date)


# Start the bot
bot.polling()
