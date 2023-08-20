import telebot
import os
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dvmn_flowers_project.settings')

import django
django.setup()

from telebot import types
from dotenv import load_dotenv
from flowerapp.models import Client, Bouquet, Order
from datetime import time
from django.db.models import Q
import itertools


load_dotenv()
bot = telebot.TeleBot(os.environ["TG_TOKEN"])
order ={}

bouquets = []
current_index = 0

@bot.message_handler(commands=['start'])
def main_menu(message):
    client, _ = Client.objects.get_or_create(tg_id=message.from_user.id,
                                            username=message.from_user.username)
    markup = types.InlineKeyboardMarkup()
    first = [types.InlineKeyboardButton(callback_data='событие на день рождения', text='на день рождения'), 
     types.InlineKeyboardButton(callback_data='событие на свадьбу', text='на свадьбу'),
     types.InlineKeyboardButton(callback_data='событие в школу', text='в школу'),
     types.InlineKeyboardButton(callback_data='событие без повода', text='без повода')
    ]
    second = [types.InlineKeyboardButton(callback_data='событие на день рождения', text='на день рождения'), 
     types.InlineKeyboardButton(callback_data='событие на свадьбу', text='на свадьбу'),
     types.InlineKeyboardButton(callback_data='событие в школу', text='в школу'),
     types.InlineKeyboardButton(callback_data='без повода', text='без повода'),
     types.InlineKeyboardButton(callback_data='Смотреть заказы',text='Смотреть заказы')]
    if Order.objects.filter(client=client):
        for button in second:
            markup.add(button)
    else:
        for button in first:
            markup.add(button)
    bot.send_message(message.from_user.id,
                     '👋 Привет! К какому событию готовимся? Выберите один из вариантов, либо укажите свой.',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('Вернуться в главное'))
def main_menu_2(message):
    client, _ = Client.objects.get_or_create(tg_id=message.from_user.id,
                                            username=message.from_user.username)
    markup = types.InlineKeyboardMarkup()
    first = [types.InlineKeyboardButton(callback_data='событие на день рождения', text='на день рождения'), 
     types.InlineKeyboardButton(callback_data='событие на свадьбу', text='на свадьбу'),
     types.InlineKeyboardButton(callback_data='событие в школу', text='в школу'),
     types.InlineKeyboardButton(callback_data='событие без повода', text='без повода')
    ]
    second = [types.InlineKeyboardButton(callback_data='событие на день рождения', text='на день рождения'), 
     types.InlineKeyboardButton(callback_data='событие на свадьбу', text='на свадьбу'),
     types.InlineKeyboardButton(callback_data='событие в школу', text='в школу'),
     types.InlineKeyboardButton(callback_data='без повода', text='без повода'),
     types.InlineKeyboardButton(callback_data='Смотреть заказы',text='Смотреть заказы')]
    if Order.objects.filter(client=client):
        for button in second:
            markup.add(button)
    else:
        for button in first:
            markup.add(button)
    bot.send_message(message.from_user.id,
                     '👋 Привет! К какому событию готовимся? Выберите один из вариантов, либо укажите свой.',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('событие'))
def choose_price(call):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data='цена 500', text='~500')
    btn2 = types.InlineKeyboardButton(callback_data='цена 1000', text='~1000')
    btn3 = types.InlineKeyboardButton(callback_data='цена 2000', text='~2000')
    btn4 = types.InlineKeyboardButton(callback_data='цена большая', text='~больше')
    btn5 = types.InlineKeyboardButton(callback_data='цена любая', text='посмотреть все')
    btn5 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(call.from_user.id, 'На какую сумму рассчитываете?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('цена'))
def choose_bouquet_or_consult(call):
    selected_price = int(call.data[4:])

    global bouquets, current_index
    current_index = 0
    bouquets = Bouquet.objects.filter(
        Q(price__lte=selected_price) |
        Q(price__isnull=True)
    )

    current_bouquet = bouquets[current_index]
    bot.send_message(call.from_user.id, f'{current_bouquet.name}\nЦена: {current_bouquet.price}р.')
    bot.send_message(call.from_user.id, current_bouquet.get_info())

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data='Заказать букет', text='Заказать букет')
    btn2 = types.InlineKeyboardButton(callback_data='Следующий букет', text='Следующий букет')
    btn3 = types.InlineKeyboardButton(callback_data='консультация', text='Заказать консультацию')
    btn4 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(call.from_user.id, 'Хотите что-то еще более уникальное? Подберите другой букет из нашей коллекции или закажите консультацию флориста)', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'Следующий букет')
def show_next_bouquet(call):
    global bouquets, current_index

    current_index += 1

    if current_index >= len(bouquets):
        current_index = 0

    next_bouquet = bouquets[current_index]
    bot.send_message(call.from_user.id, f'{next_bouquet.name}\nЦена: {next_bouquet.price}р.')
    bot.send_message(call.from_user.id, next_bouquet.get_info())

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data='Заказать букет', text='Заказать букет')
    btn2 = types.InlineKeyboardButton(callback_data='Следующий букет', text='Следующий букет')
    btn3 = types.InlineKeyboardButton(callback_data='консультация', text='Заказать консультацию')
    btn4 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(call.from_user.id, 'Хотите что-то еще более уникальное? Подберите другой букет из нашей коллекции или закажите консультацию флориста)', reply_markup=markup)

'''консультация'''
@bot.callback_query_handler(func=lambda call: call.data.startswith('консультация'))
def get_phonenumber(call):
    markup = types.InlineKeyboardMarkup()
    msg = bot.send_message(call.from_user.id, 'Укажите номер телефона, и наш флорист перезвонит вам в течение 20 минут)', reply_markup=markup)
    bot.register_next_step_handler(msg, call_consult)


def call_consult(call):
    phonenumber = call.text
    bot.send_message(call.from_user.id, "Флорист скоро свяжется с вами. А пока можете присмотреть что-нибудь из готовой коллекции:")
    choose_bouquet_or_consult(call)


@bot.callback_query_handler(func=lambda call: call.data.startswith('Заказать букет'))
def get_user_name_surname(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn)
    msg  = bot.send_message(message.from_user.id, "Введите ваши ФИО:", reply_markup=markup)
    bot.register_next_step_handler(msg, get_address)

def get_address(message):
    order['name'] = message.text
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn)
    msg  = bot.send_message(message.from_user.id, "Введите ваш адрес:", reply_markup=markup)
    bot.register_next_step_handler(msg, get_phone)


def get_phone(message):
    order['address'] = message.text
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn)
    msg  = bot.send_message(message.from_user.id, "Введите ваш телефон:", reply_markup=markup)
    bot.register_next_step_handler(msg, get_delivery_date)


def get_delivery_date(message):
    order['phone'] = message.text
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn)
    msg  = bot.send_message(message.from_user.id, "Введите дату доставки в формате год-месяц-день (например 2023-08-16):", reply_markup=markup)
    bot.register_next_step_handler(msg, get_delivery_time)


def get_delivery_time(message):
    order['delivery_date'] = message.text
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn)
    msg = bot.send_message(message.from_user.id, "Введите время доставки в формате час:минуты:секунды (например 15:00:00):", reply_markup=markup)
    bot.register_next_step_handler(msg, makeorder)


def makeorder(message):
    order['delivery_time'] = message.text
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn)
    bot.send_message(message.from_user.id, "Отлично! Заказ создан.", reply_markup=markup)

def run_bot():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    run_bot()