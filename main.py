import os
from requests import get
from dotenv import load_dotenv
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup

from tg_bot.ORM_test.data import db_session
from tg_bot.ORM_test.data.users import User

db_session.global_init("ORM_test/db/Users.db")

username = ''
date = ''
func = ''

load_dotenv()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

reply_keyboard = [["/photo_of_the_Earth"], ["/photo_Mars"], ["/photo_NASA"], ["/start"]]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def stop(update, context):
    await update.message.reply_text("BB")
    return ConversationHandler.END


async def photo_NASA(update, context):
    await update.message.reply_html('Введите дату которая вас интересует (в формате гггг-мм-дд),'
                                    ' и мы отправим вам фото, сделанное NASA в этот день')
    return 1


async def first_N_response(update, context):
    global username
    global date
    global func
    user = update.effective_user
    locality = update.message.text
    db_sess = db_session.create_session()
    username = user['username']
    func = 'photo_NASA'
    date = ''.join(locality)
    print(username, func, date)
    user = User(username=username, date=date, func=func)

    db_sess.add(user)
    db_sess.commit()
    api_key = 'iuCdE8es7d2DuclaVnHviPHbWC8fRT21VfnAykJT'
    url = f'https://api.nasa.gov/planetary/apod?date={locality}&api_key={api_key}'
    file = get(url).json()

    if len(file) != 0:
        if len(file) != 1:
            for num in file:
                if num == 'url':
                    url = file['url']
    await update.message.reply_photo(url)
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('photo_NASA', photo_NASA)],
    states={
        # Функция читает ответ на первый вопрос и задаёт второй.
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_N_response)]

    },
    fallbacks=[CommandHandler('stop', stop)])


async def photo_of_the_Earth(update, context):
    await update.message.reply_html('Введите дату которая вас интересует (в формате гггг-мм-дд),'
                                    ' и мы отправим вам фото земли в этот день')
    return 3


async def first_E_response(update, context):
    global username
    global date
    global func
    db_sess = db_session.create_session()
    locality = update.message.text
    user = update.effective_user
    username = user['username']
    func = 'photo_of_the_Earth'
    date = ''.join(locality)
    print(username, func, date)
    user = User(username=username, date=date, func=func)

    db_sess.add(user)
    db_sess.commit()
    s = locality.split('-')
    print(s)
    api_key = 'iuCdE8es7d2DuclaVnHviPHbWC8fRT21VfnAykJT'
    url_1 = f'https://api.nasa.gov/EPIC/api/natural/date/{locality}?api_key={api_key}'
    file = get(url_1).json()
    url_2 = file[0]['identifier']
    print(url_2)

    url_3 = f'https://api.nasa.gov/EPIC/archive/natural/{s[0]}/{s[1]}/{s[2]}/png/epic_1b_{url_2}.png?api_key={api_key}'
    await update.message.reply_photo(url_3)
    return ConversationHandler.END


conv_handler2 = ConversationHandler(
    entry_points=[CommandHandler('photo_of_the_Earth', photo_of_the_Earth)],
    states={
        # Функция читает ответ на первый вопрос и задаёт второй.
        3: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_E_response)]

    },
    fallbacks=[CommandHandler('stop', stop)])


async def photo_Mars(update, context):
    await update.message.reply_html('Введите дату которая вас интересует (в формате гггг-м-д),'
                                    ' и мы отправим вам фото, сделанное марсоходом в этот день!')
    return 5


async def first_M_response(update, context):
    global username
    global date
    global func
    db_sess = db_session.create_session()
    locality = update.message.text
    user = update.effective_user
    username = user['username']
    func = 'photo_Mars'
    date = ''.join(locality)
    print(username, func, date)
    user = User(username=username, date=date, func=func)

    db_sess.add(user)
    db_sess.commit()
    print(locality)
    api_key = 'iuCdE8es7d2DuclaVnHviPHbWC8fRT21VfnAykJT'
    url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={locality}&api_key={api_key}'
    file = get(url).json()
    await update.message.reply_photo(file['photos'][1]['img_src'])
    return ConversationHandler.END


conv_handler3 = ConversationHandler(
    entry_points=[CommandHandler('photo_Mars', photo_Mars)],
    states={
        # Функция читает ответ на первый вопрос и задаёт второй.
        5: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_M_response)]

    },
    fallbacks=[CommandHandler('stop', stop)])
a = 1108048915


async def start(update, context):
    user = update.effective_user
    global username
    username = user['username']

    db_sess = db_session.create_session()

    user_bd = db_sess.query(User).filter(User.username == username).first()
    if not user_bd:

        await update.message.reply_html(
            rf'Привет,{user.mention_html()}! Это телеграмм бот NASA! Я умею многое, например, '
            rf'я могу узнать погоду на Марсе или показать как выглядела Земля из космоса в любой'
            rf' день. И самое интересное я могу предоставить фотографию от NASA которую она сделала'
            rf' в определённый день!!' rf'',
            reply_markup=markup)
        await update.message.reply_html('Сейчас немного расскажу про свой функционал:\n'
                                        '<b>•Астрономическая картина дня</b>\n'
                                        '<b>•Околоземные астероиды</b>\n'
                                        '<b>•Камера для съёмки Земли</b>')
        await update.message.reply_html('Выберите одну из представленных функций')
        # МНОГО ТЕКСТА?
        # await update.message.reply_html('<b>Астрономическая картина дня</b> - '
        #                                 'Откройте для себя космос! Каждый день'
        #                                 ' появляется новое изображение или фотография нашей'
        #                                 ' удивительной Вселенной. вместе с кратким объяснением,'
        #                                 ' написанным профессиональным астрономом.')
        # await update.message.reply_html('<b>Околоземные астероиды</b> - '
        #                                 'С помощью данной функции пользователь может: искать астероиды по дате'
        #                                 ' их ближайшего сближения с Землей, искать конкретный астероид'
        #                                 ' по его идентификатору малого тела NASA JPL, а также просматривать'
        #                                 ' общий набор данных.')
        # await update.message.reply_html('<b>Камера для съёмки Земли</b> '
        #                                 'предоставляет информацию о ежедневных изображениях,'
        #                                 ' собираемых с помощью инструмента DSCOVR Earth Polychromatic'
        #                                 ' Imaging Camera (EPIC). Уникально расположенный в точке'
        #                                 ' Лагранжа между Землей и Солнцем, EPIC обеспечивает получение'
        #                                 ' полных изображений диска Земли и фиксирует уникальные'
        #                                 ' перспективы определенных астрономических событий, таких как'
        #                                 ' транзиты Луны, с помощью детектора CCD (Charge Coupled Device)'
        #                                 ' с разрешением 2048x2048 пикселей, соединенного с'
        #                                 ' 30-сантиметровой апертурой телескопа Кассегрена.')
    else:
        await update.message.reply_html(
            rf'Привет,{user.mention_html()}! Рады видеть тебя снова. Выбери интересующую функцию)' rf'',
            reply_markup=markup)


async def data(update, funcc):
    date = update.message.text
    await update.message.reply_text(f'Ваша функция:{funcc}\n Ваша дата {date}')  # перевести объект тг в текст


def main():
    token = os.environ.get('TOKEN', '')
    app = Application.builder().token(token).build()
    app.add_handler(conv_handler)
    app.add_handler(conv_handler2)
    app.add_handler(conv_handler3)  ###размер кнопок  текст на руском?
    app.add_handler(CommandHandler('start', start))
    # app.add_handler(CommandHandler('photo_NASA', photo_NASA))
    # app.add_handler(CommandHandler('photo_of_the_Earth', photo_of_the_Earth))
    # app.add_handler(CommandHandler('photo_Mars', photo_Mars))
    # app.add_handler(CommandHandler('stop', stop))

    app.run_polling()


if __name__ == '__main__':
    main()
