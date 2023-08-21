import telebot
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dvmn_flowers_project.settings')

import django
django.setup()

from dotenv import load_dotenv
from flowerapp.models import Order, Courier


load_dotenv()
bot = telebot.TeleBot(os.environ["COURIER_TG_TOKEN"])


@bot.message_handler(commands=['start'])
def start_handler(message):
    courier, _ = Courier.objects.get_or_create(tg_id=message.from_user.id,
                                           username=message.from_user.username)

    bot.send_message(message.from_user.id, "В этот чат будут приходить новые заказы")


def send_order(order: Order):
    print(0)
    couriers = Courier.objects.all()
    for courier in couriers:
        bot.send_message(courier.tg_id, "ПШПШПШ")
        bouquet = order.bouquet
        bot.send_message(courier.tg_id, f'Новый заказ. Номер заказа: {order.pk}\n\n'
                                      f'Букет: {bouquet}. \n'
                                      f'Цена: {bouquet.price}\n'
                                      f'Описание: {bouquet.desсription}\n\n'
                                      f'Адрес: {order.address}')


def run_courier():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    run_courier()