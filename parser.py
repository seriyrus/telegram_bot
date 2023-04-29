import config
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup as bs

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    barnaul = types.InlineKeyboardButton('Барнаул', callback_data='barnaul')
    ekaterinburg = types.InlineKeyboardButton('Екатеринбург', callback_data='ekaterinburg')
    krasnouarsk = types.InlineKeyboardButton('красноярск', callback_data='krasnouarsk')
    elektrostal = types.InlineKeyboardButton('электросталь', callback_data='elektrostal')
    omsk = types.InlineKeyboardButton('омск', callback_data='omsk')
    rostov = types.InlineKeyboardButton('ростов', callback_data='rostov')
    moskow = types.InlineKeyboardButton('москва', callback_data='moskow')
    piter = types.InlineKeyboardButton('питер', callback_data='piter')
    markup.row(barnaul, ekaterinburg, krasnouarsk, elektrostal)
    markup.row(omsk, rostov, moskow, piter)
    bot.send_message(message.chat.id, 'Пример парсера сайта (парсим gismeteo)\nВыберите город:',reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def cities_get_weather(callback):
    if callback.data == 'barnaul':
        url = 'https://www.gismeteo.ru/weather-barnaul-4720/now/'
        msg = 'В Барнауле сейчас:' + generate_parser(url)
        bot.send_message(callback.message.chat.id, msg)

    if callback.data == 'elektrostal':
        url = 'https://www.gismeteo.ru/weather-elektrostal-11312/now/'
        msg = 'В Электростали сейчас:' + generate_parser(url)
        bot.send_message(callback.message.chat.id, msg)

    if callback.data == 'ekaterinburg':
        url = 'https://www.gismeteo.ru/weather-yekaterinburg-4517/now/'
        msg = 'В Екатеринбурге сейчас:' + generate_parser(url)
        bot.send_message(callback.message.chat.id, msg)

    if callback.data == 'krasnouarsk':
        url = 'https://www.gismeteo.ru/weather-krasnoyarsk-4674/now/'
        msg = 'В Красноярске сейчас:' + generate_parser(url)
        bot.send_message(callback.message.chat.id, msg)

    if callback.data == 'omsk':
        url = 'https://www.gismeteo.ru/weather-omsk-4578/now/'
        msg = 'В Омске сейчас:' + generate_parser(url)
        bot.send_message(callback.message.chat.id, msg)

    if callback.data == 'rostov':
        url = 'https://www.gismeteo.ru/weather-rostov-na-donu-5110/now/'
        msg = 'В Ростове сейчас:' + generate_parser(url)
        bot.send_message(callback.message.chat.id, msg)

    if callback.data == 'moskow':
        url = 'https://www.gismeteo.ru/weather-moscow-4368/now/'
        msg = 'В Москве сейчас:' + generate_parser(url)
        bot.send_message(callback.message.chat.id, msg)

    if callback.data == 'piter':
        url = 'https://www.gismeteo.ru/weather-sankt-peterburg-4079/now/'
        msg = 'В Санкт-Петербурге сейчас:' + generate_parser(url)
        bot.send_message(callback.message.chat.id, msg)

def generate_parser(url):
    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
        }
    )
    page = requests.get(url, headers=headers)
    html = bs(page.content, 'html.parser')

    temp = html.select('.weather-value')[0].text[0:3]
    msg = '\n' + '🌡' + temp + '\n'
    desk = html.select('.now-desc')[0].text
    if desk.split(',')[0] == 'Ясно':
        msg += '☀' + desk
    if desk.split(',')[0] == 'Пасмурно':
        msg += '🌧' + desk
    if desk.split(',')[0] == 'Облачно':
        msg += '⛅' + desk
    return msg


bot.polling(none_stop=True)
