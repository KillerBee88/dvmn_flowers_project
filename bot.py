import phonenumbers
import telebot
import os
import datetime
from datetime import datetime
import sqlite3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dvmn_flowers_project.settings')

import django
django.setup()

from telebot import types
from dotenv import load_dotenv
from flowerapp.models import Client, Bouquet, Order
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
    order = {}
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
     types.InlineKeyboardButton(callback_data='событие без повода', text='без повода'),
     types.InlineKeyboardButton(callback_data='Мои заказы', text='Мои заказы')]
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
    order['type'] = call.data[8:]
    print(order['type'])
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data='цена 500', text='~500')
    btn2 = types.InlineKeyboardButton(callback_data='цена 1000', text='~1000')
    btn3 = types.InlineKeyboardButton(callback_data='цена 2000', text='~2000')
    btn4 = types.InlineKeyboardButton(callback_data='цена большая', text='~больше')
    btn5 = types.InlineKeyboardButton(callback_data='цена любая', text='посмотреть все')
    btn6 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(call.from_user.id, 'На какую сумму рассчитываете?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('цена'))
def choose_bouquet_or_consult(call):
    print(order['type'])
    global bouquets, current_index
    current_index = 0
    if call.data == 'цена любая' or call.data == 'цена':
        selected_price = 0
    if call.data == 'цена большая':
        selected_price = 2500
    else:
        try:
            selected_price = int(call.data[4:])
        except :
            selected_price = 0
    if order['type'] != '':
        bouquets = Bouquet.objects.filter(
        Q(price__gte=selected_price, type=order['type']) |
        Q(price__isnull=True)
    )
    else:
        bouquets = Bouquet.objects.filter(
        Q(price__gte=selected_price) |
        Q(price__isnull=True)
    )


    current_bouquet = bouquets[current_index]
    bot.send_photo(call.from_user.id, photo=current_bouquet.image)
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
    bot.send_photo(call.from_user.id, photo=next_bouquet.image)
    bot.send_message(call.from_user.id, f'{next_bouquet.name}\nЦена: {next_bouquet.price}р.')
    bot.send_message(call.from_user.id, next_bouquet.get_info())

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data='Заказать букет', text='Заказать букет')
    btn2 = types.InlineKeyboardButton(callback_data='Следующий букет', text='Следующий букет')
    btn3 = types.InlineKeyboardButton(callback_data='консультация', text='Заказать консультацию')
    btn4 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    btn5 = types.InlineKeyboardButton(callback_data='Мои заказы', text='Мои заказы')
    markup.add(btn1, btn2, btn3, btn4, btn5)

    bot.send_message(call.from_user.id, 'Хотите что-то еще более уникальное? Подберите другой букет из нашей коллекции или закажите консультацию флориста)', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'Мои заказы')
def my_orders_callback(call):
    client_id = call.from_user.id
    client = Client.objects.get(tg_id=client_id)
    orders = Order.objects.filter(client=client).order_by('delivery_date')
    
    if orders:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️',
                                          text='Вернуться в главное меню ⬅️')
        markup.add(btn1)
        bot.send_message(client_id, 'Ваши заказы.', reply_markup=markup)

        for order in orders:
            order_str = f'Заказ №{order.id}\n' \
                        f'Букет: {order.bouquet}\n' \
                        f'Адрес: {order.address}\n' \
                        f'Дата доставки: {order.delivery_date}\n' \
                        f'Телефон: {order.phone}\n' \
                        f'Время доставки: {order.delivery_time}\n'
            bot.send_message(client_id, order_str, reply_markup=markup)
    else:
        bot.send_message(client_id, "У вас пока нет заказов.") 
'''консультация'''
@bot.callback_query_handler(func=lambda call: call.data.startswith('консультация'))
def get_phonenumber(call):
    order['type'] = ''
    markup = types.InlineKeyboardMarkup()
    msg = bot.send_message(call.from_user.id, 'Укажите номер телефона, и наш флорист перезвонит вам в течение 20 минут)', reply_markup=markup)
    bot.register_next_step_handler(msg, call_consult)


def call_consult(call):
    try:
        pasrephone = phonenumbers.parse(call.text, "RU")
        if not(phonenumbers.is_valid_number(pasrephone)):
            raise ZeroDivisionError
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(callback_data='цена',
                                          text='Выбрать букеты')
        markup.add(btn1)
        bot.send_message(call.from_user.id, "Флорист скоро свяжется с вами. А пока можете присмотреть что-нибудь из готовой коллекции:", reply_markup=markup)
        bot.register_next_step_handler(call, choose_bouquet_or_consult)
    except:
        markup = types.InlineKeyboardMarkup()
        bot.send_message(call.from_user.id, "Неправильно ввели телефон, попробуйте ещё раз:", reply_markup=markup)
        get_phonenumber(call)
   
    


@bot.callback_query_handler(func=lambda call: call.data.startswith('Заказать букет'))
def get_user_name_surname(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn)
    msg  = bot.send_message(message.from_user.id, "Введите ваши ФИО:", reply_markup=markup)
    bot.register_next_step_handler(msg, get_address)
    order['bouquet'] = bouquets[current_index]


def get_address(message):
    order['name'] = message.text
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn)
    msg  = bot.send_message(message.from_user.id, "Введите ваш адрес:", reply_markup=markup)
    bot.register_next_step_handler(msg, get_phone)


def get_phone(message):
    if 'address' not in order:
        order['address'] = message.text
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn)
    msg  = bot.send_message(message.from_user.id, "Введите ваш телефон:", reply_markup=markup)
    bot.register_next_step_handler(msg, get_delivery_date)


def get_delivery_date(message):
    try:
        pasrephone = phonenumbers.parse(message.text, "RU")
        if not(phonenumbers.is_valid_number(pasrephone)):
            raise ZeroDivisionError
        if 'phone' not in order:
            order['phone'] = message.text
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
        markup.add(btn)
        msg  = bot.send_message(message.from_user.id, "Введите дату доставки в формате год-месяц-день (например 2023-12-02):", reply_markup=markup)
        bot.register_next_step_handler(msg, get_delivery_time)
    except:
        markup = types.InlineKeyboardMarkup()
        bot.send_message(message.from_user.id, "Неправильно ввели телефон, попробуйте ещё раз:", reply_markup=markup)
        get_phone(message)


def get_delivery_date_second(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn)
    msg  = bot.send_message(message.from_user.id, "Введите дату доставки в формате год-месяц-день (например 2023-12-02):", reply_markup=markup)
    bot.register_next_step_handler(msg, get_delivery_time)

def get_delivery_time(message):
    try:
        datetime.strptime(message.text, '%Y-%m-%d') 
        order['delivery_date'] = message.text
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
        markup.add(btn)
        msg = bot.send_message(message.from_user.id, "Введите время доставки в формате час:минуты (например 15:00):", reply_markup=markup)
        bot.register_next_step_handler(msg, makeorder)
    except ValueError:
        bot.send_message(message.from_user.id, "Неправильно ввели дату, попробуйте ещё раз!")
        get_delivery_date_second(message)

def get_delivery_time_second(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn)
    msg = bot.send_message(message.from_user.id, "Введите время доставки в формате час:минуты (например 15:00):", reply_markup=markup)
    bot.register_next_step_handler(msg, makeorder)
        

def makeorder(message):
    try:
        datetime.strptime(message.text, '%H:%M') 
        order['delivery_time'] = message.text
        client_id = message.from_user.id
        delivery_time = message.text

        client, created = Client.objects.get_or_create(tg_id=client_id, defaults={'username': 'Unknown'})
        selected_bouquet = Bouquet.objects.get(id=order['bouquet'].id) 
        
        new_order = Order(
            client=client,
            bouquet=selected_bouquet,
            address=order['address'],
            delivery_date=order['delivery_date'],
            phone=order['phone'],
            delivery_time=delivery_time
        )
        new_order.save()

        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
        markup.add(btn)
        bot.send_message(message.from_user.id, "Отлично! Заказ создан.", reply_markup=markup)
    except ValueError:
        bot.send_message(message.from_user.id, "Неправильно ввели время, попробуйте ещё раз!")
        get_delivery_time_second(message)



    

def run_bot():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    run_bot()