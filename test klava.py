import requests
import time
import json

#тут все ясно
TOKEN = '6777897206:AAH7lctWm73bO3eOSg_4o1BXJb61w3m4pY0'
URL = 'https://api.telegram.org/bot'

#ринимает сообщения и клики
def get_updates(offset=0):
    result = requests.get(f'{URL}{TOKEN}/getUpdates?offset={offset}').json()
    return result['result']

#отправка сообщения
def send_message(chat_id, text):
    requests.get(f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={text}')

#отправка фотки по url
def send_photo_url(chat_id, img_url):
    requests.get(f'{URL}{TOKEN}/sendPhoto?chat_id={chat_id}&photo={img_url}')

#отправка фотки с компа (оставила для зайца)
def send_photo_file(chat_id, img):
    files = {'photo': open(img, 'rb')}
    requests.post(f'{URL}{TOKEN}/sendPhoto?chat_id={chat_id}', files=files)

#отправка фотки с сервера тг (вряд ли понадобится)
def send_photo_file_id(chat_id, file_id):
    requests.get(f'{URL}{TOKEN}/sendPhoto?chat_id={chat_id}&photo={file_id}')

#сообщение с кнопкой контакты
def inline_keyboard_contacts(chat_id, text):
    reply_markup = {'inline_keyboard': [[{'text': 'Алиса лох', 'url': 'https://yandex.ru'},{'text': 'объелась блох', 'url': 'https://yandex.ru'}]]}
    data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
    requests.post(f'{URL}{TOKEN}/sendMessage', data=data)

#сообщение с кнопками функций
def inline_keyboard_func(chat_id, text):
    reply_markup = {'inline_keyboard': [[{'text': 'Пинать хуи', 'url': 'https://yandex.ru'},{'text': 'не спать', 'url': 'https://yandex.ru'},{'text': 'страдать', 'url': 'https://yandex.ru'}]]}
    data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
    requests.post(f'{URL}{TOKEN}/sendMessage', data=data)

#типо основные кнопки
def reply_keyboard(chat_id, text):
    reply_markup ={ "keyboard": [["Астрономическая картина дня", "Околоземные астероиды"], ["Что ты умеешь?"]], "resize_keyboard": True, "one_time_keyboard": True}
    data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
    requests.post(f'{URL}{TOKEN}/sendMessage', data=data)

#проверка введенного текста (текст кнопки также считается за текст)
def check_message(chat_id, message):
    if message.lower() in ['привет', 'hello']:
        send_message(chat_id, 'Привет :)')
    elif message.lower() in 'Контакты':
        inline_keyboard_contacts(chat_id, 'Наши контакты')
    elif message.lower().split()[-1] in 'астероиды':
        send_message(chat_id, 'Введите стартовую дату в формате: гггг-мм-дд')

    elif message.lower().split()[-1] in 'дня':
        # Отправить URL-адрес картинки (телеграм скачает его и отправит)
        send_message(chat_id, 'Введите стартовую дату в формате: гггг-мм-дд')
        send_photo_url(chat_id, 'https://apod.nasa.gov/apod/image/2404/M82Center_HubbleWebb_1080.jpg')
    elif message.lower() in 'фото с компьютера':
        # Отправить файл с компьютера
        send_photo_file(chat_id, 'photo.jpg')
    elif message.lower() in 'фото с сервера телеграм':
        # Отправить id файла (файл уже хранится где-то на серверах Telegram)
        send_photo_file_id(chat_id, 'AgACAgIAAxkBAAMqYVGBbdbivL53IzKLfUKUClBnB0cAApy0MRtfMZBKHL0tNw9aITwBAAMCAAN4AAMhBA')
    else:
        reply_keyboard(chat_id, 'Вот что я умею')
        inline_keyboard_func(chat_id, 'Весь мой функционал')

def run():
    update_id = get_updates()[-1]['update_id'] # Присваиваем ID последнего отправленного сообщения боту
    while True:
        time.sleep(2)
        messages = get_updates(update_id) # Получаем обновления
        for message in messages:
            # Если в обновлении есть ID больше чем ID последнего сообщения, значит пришло новое сообщение
            if update_id < message['update_id']:
                update_id = message['update_id'] # Присваиваем ID последнего отправленного сообщения боту
                # Отвечаем тому кто прислал сообщение боту
                check_message(message['message']['chat']['id'], message['message']['text'])

if __name__ == '__main__':
    run()