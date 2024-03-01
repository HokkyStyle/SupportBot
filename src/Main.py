import telebot
import random
from telebot import types

bot = telebot.TeleBot('6796670990:AAE3i0hhWTvA4hW3_iUUDpeNz-rSJUYkbck')

urls = ['https://t.me/xoxilixxx']
url_index = 0  # Индекс текущего URL


@bot.message_handler(commands=['start'])
def start(message):
    global url_index
    current_url = urls[url_index]
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Перейти к оператору", url=current_url)
    markup.add(button1)
    bot.send_message(message.chat.id,
                     "Welcome! Нажмите на кнопку, чтобы перейти к одному из операторов".format(message.from_user),
                     reply_markup=markup)
    url_index = (url_index + 1) % len(urls)


bot.polling(none_stop=True)
