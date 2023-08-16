from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

updater = Updater(token='6017270704:AAH9MTfQELdHSXbbCAwfPQXL-47Xnuhf0p8', use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("День рождения", callback_data='birthday'),
         InlineKeyboardButton("Свадьба", callback_data='wedding')],
        [InlineKeyboardButton("В школу", callback_data='school'),
         InlineKeyboardButton("Без повода", callback_data='no_reason')],
        [InlineKeyboardButton("Другой повод", callback_data='other')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('К какому событию готовимся?', reply_markup=reply_markup)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def event_choice(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    callback_data = query.data

    if callback_data == 'other':
        query.edit_message_text(text="Пожалуйста, укажите повод")
    elif callback_data == 'birthday':
        query.edit_message_text(text="Вы выбрали событие 'День рождения'")
        send_bouquet_list(query.message.chat_id, 'birthday', context)
    elif callback_data == 'wedding':
        query.edit_message_text(text="Вы выбрали событие 'Свадьба'")
        send_bouquet_list(query.message.chat_id, 'wedding', context)
    elif callback_data == 'school':
        query.edit_message_text(text="Вы выбрали событие 'В школу'")
        send_bouquet_list(query.message.chat_id, 'school', context)
    elif callback_data == 'no_reason':
        query.edit_message_text(text="Вы выбрали событие 'Без повода'")
        send_bouquet_list(query.message.chat_id, 'no_reason', context)


def send_bouquet_list(chat_id, event, context):
    if event == 'birthday':
        bouquets = [
            {'name': 'Розовый букет', 'price': 10},
            {'name': 'Синий букет', 'price': 15},
            {'name': 'Фиолетовый букет', 'price': 12}
        ]
    elif event == 'wedding':
        bouquets = [
            {'name': 'Белый букет', 'price': 20},
            {'name': 'Кремовый букет', 'price': 18},
            {'name': 'Розовый букет', 'price': 22}
        ]
    elif event == 'school':
        bouquets = [
            {'name': 'Школьный букет', 'price': 8},
            {'name': 'Радужный букет', 'price': 10},
            {'name': 'Цветастый букет', 'price': 9}
        ]
    elif event == 'no_reason':
        bouquets = [
            {'name': 'Красный букет', 'price': 10},
            {'name': 'Оранжевый букет', 'price': 12},
            {'name': 'Желтый букет', 'price': 11}
        ]

    keyboard = []
    for bouquet in bouquets:
        button_text = f'{bouquet["name"]} (${bouquet["price"]})'
        button = InlineKeyboardButton(button_text, callback_data=f'order_{bouquet["name"]}')
        keyboard.append([button])

    reply_markup = InlineKeyboardMarkup(keyboard)

    message_text = f'Список букетов для выбранного события:\n'
    context.bot.send_message(chat_id=chat_id, text=message_text, reply_markup=reply_markup)

dispatcher.add_handler(CallbackQueryHandler(event_choice))


updater.start_polling()