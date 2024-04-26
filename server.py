import os
import datetime as dt
from requests import get
from dotenv import load_dotenv
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup

from tg_bot.ORM_test.data import db_session
from tg_bot.ORM_test.data.users import User

print(44+60+341)

db_session.global_init("ORM_test/db/Users.db")

username = ''
date = ''
func = ''

load_dotenv()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

reply_keyboard = [["/photo_of_the_Earth"], ["/photo_Mars"], ["/photo_NASA"],  ['/Sun_sistem'],
                  ["/Info_func"], ["/zayac"],["/start"], ["/stop"]]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

async def Info_func(update, context):
    await update.message.reply_html('<b>/photo_of_the_Earth</b> - '
                                    'Фотография Земли по вашей дате')
    await update.message.reply_html('<b>/photo_Mars</b> - '
                                    'фотография Марса по вашей дате')
    await update.message.reply_html('<b>/photo_NASA</b> '
                                    "Фотография из архивов Nasa по вашей дате")
    await update.message.reply_html('<b>/Sun_sistem</b> '
                                    "Информация о Солнечной системе")
    await update.message.reply_html('<b>/zayac</b> '
                                    "Вам пришлют зайца!")
    await update.message.reply_html('<b>/start</b> '
                                    "При нажатии этой кнопке Вы просто начнете сначало")
    await update.message.reply_html('<b>/stop</b> '
                                    "При нажатии этой кнопки бот остановится")
    await update.message.reply_html('Выберите одну из представленных функций')

async def stop(update, context):
    await update.message.reply_text("Пока!")
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
    d = dt.datetime.now().date()
    db_sess = db_session.create_session()
    username = user['username']
    func = 'photo_NASA'
    date = ''.join(locality)
    user = User(username=username, date=date, func=func)

    db_sess.add(user)
    db_sess.commit()
    api_key = 'iuCdE8es7d2DuclaVnHviPHbWC8fRT21VfnAykJT'
    url = f'https://api.nasa.gov/planetary/apod?date={locality}&api_key={api_key}'
    file = get(url).json()
    if len(locality.split('-')) != 3:
        await update.message.reply_text('Неверный формат даты, повторите попытку')
        return
    else:
        s = locality.split('-')
    if s[0].isdigit() and s[1].isdigit() and s[2].isdigit():
        if (2013 < int(s[0]) < d.year) and (1 <= int(s[1]) <= 12) and (1 <= int(s[2]) <= 31):
            if len(file) != 0:
                if len(file) != 1:
                    for num in file:
                        if num == 'url':
                            url = file['url']
                            await update.message.reply_photo(url)
        elif (s[0] == d.year) and (s[1] <= d.month) and (s[1] < d.day):
            await update.message.reply_photo(url)


        else:
            await update.message.reply_text('Извините, у NASA пока нет фотографии сделанной в этот день)')
            return
    else:
        await update.message.reply_text('Проверьте верность формата введённой даты')
        return
    await update.message.reply_text('Вау, какое красивое фото!\n'
                                    'Попробуйте наши другие функции или запустите снова эту))')
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
    user = User(username=username, date=date, func=func)

    db_sess.add(user)
    db_sess.commit()
    d = dt.datetime.now().date()
    api_key = 'iuCdE8es7d2DuclaVnHviPHbWC8fRT21VfnAykJT'
    url_1 = f'https://api.nasa.gov/EPIC/api/natural/date/{locality}?api_key={api_key}'
    if len(locality.split('-')) != 3:
        await update.message.reply_text('Неверный формат даты, повторите попытку')
        return
    else:
        s = date.split('-')
    if s[0].isdigit() and s[1].isdigit() and s[2].isdigit():
        if (2010 < int(s[0]) < d.year) and (1 <= int(s[1]) <= 12) and (1 <= int(s[2]) <= 31):
            file = get(url_1).json()
            url_2 = file[0]['identifier']
            url_3 = f'https://api.nasa.gov/EPIC/archive/natural/{s[0]}/{s[1]}/{s[2]}/png/epic_1b_{url_2}.png?api_key={api_key}'
            await update.message.reply_photo(url_3)

        elif (s[0] == d.year) and (s[1] <= d.month) and (s[1] < d.day):
            file = get(url_1).json()
            url_2 = file[0]['identifier']
            url_3 = f'https://api.nasa.gov/EPIC/archive/natural/{s[0]}/{s[1]}/{s[2]}/png/epic_1b_{url_2}.png?api_key={api_key}'
            await update.message.reply_photo(url_3)

        else:
            await update.message.reply_text('Извините, у NASA пока нет фотографии сделанной в этот день)')
            return
    else:
        await update.message.reply_text('Проверьте верность формата введённой даты')
        return
    await update.message.reply_text('Наша планета прекрасна!!\n'
                                    'Попробуйте наши другие функции или запустите снова эту))')
    return ConversationHandler.END


conv_handler2 = ConversationHandler(
    entry_points=[CommandHandler('photo_of_the_Earth', photo_of_the_Earth)],
    states={
        # Функция читает ответ на первый вопрос и задаёт второй.
        3: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_E_response)]

    },
    fallbacks=[CommandHandler('stop', stop)])


async def photo_Mars(update, context):
    await update.message.reply_html('Введите дату которая вас интересует (в формате гггг-мм-дд),'
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

    api_key = 'iuCdE8es7d2DuclaVnHviPHbWC8fRT21VfnAykJT'
    url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={locality}&api_key={api_key}'

    d = dt.datetime.now().date()
    if len(locality.split('-')) != 3:
        await update.message.reply_text('Неверный формат даты, повторите попытку')
        return
    else:
        s = locality.split('-')
    if s[0].isdigit() and s[1].isdigit() and s[2].isdigit():
        if (2010 < int(s[0]) < d.year) and (1 <= int(s[1]) <= 12) and (1 <= int(s[2]) <= 31):
            file = get(url).json()
            await update.message.reply_photo(file['photos'][1]['img_src'])

        elif (s[0] == d.year) and (s[1] <= d.month) and (s[1] <= d.day):
            file = get(url).json()
            await update.message.reply_photo(file['photos'][1]['img_src'])

        else:
            await update.message.reply_text('Извините, у NASA пока нет фотографии сделанной в этот день)')
            return
    else:
        await update.message.reply_text('Проверьте верность формата введённой даты')
        return
    await update.message.reply_text('Марс иснтересная планета, не правда ли?\n'
                                    'Попробуйте наши другие функции или запустите снова эту))')
    return ConversationHandler.END


conv_handler3 = ConversationHandler(
    entry_points=[CommandHandler('photo_Mars', photo_Mars)],
    states={
        # Функция читает ответ на первый вопрос и задаёт второй.
        5: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_M_response)]

    },
    fallbacks=[CommandHandler('stop', stop)])


async def sun_sistem(update, context):
    await update.message.reply_html(
        '<b>Что такое Солнечная система?</b>\n'
        'Солнечная система – это совокупность планет, вращающихся вокруг центральной звезды.\n\n'
        'Ученым удалось установить, что ей примерно 4,57 млрд лет, а появилась она за счет гравитационного сжатия '
        'газопылевого облака. В основе системы лежит яркая звезда – Солнце, которое удерживает планеты и другие объекты,'
        ' заставляя их вращаться по орбите на определенном расстоянии.\n\n'
        'Оно во много раз превосходит по диаметру другие объекты, находящиеся в области его притяжения. Интересный факт:'
        ' Солнце обладает такой большой массой, что все остальные планеты системы составляют лишь 0,0014% от его веса.'
        ' В составе Солнечной системы, помимо звезды, находится восемь основных планет, а также пять карликовых.'
        ' Располагается она в галактике Млечный Путь, в рукаве Ориона. \n\n'
        'Сейчас процесс возникновения Солнечной системы описывается следующими шагами:\n\n'
        'Изначально в этой области вселенной находилось облако, состоящее из гелия, водорода и других'
        ' веществ, полученных при взрывах старых'
        ' звезд. В небольшой его части началось уплотнение, ставшее центром гравитационного коллапса. '
        'Он постепенно начал притягивать к себе окружающие вещества.\n\n'
        'Из-за притяжения веществ размеры облака начали уменьшаться, при этом росла скорость вращения. '
        'Постепенно его форма превратилась в диск.\n\n'
        'По мере сжатия увеличивалась плотность частиц на единицу объема, что приводило к постепенному '
        'нагреву вещества за счет частых столкновений молекул.\n\n'
        'Когда центр гравитационного коллапса разогрелся до нескольких тысяч кельвинов, он начал светиться'
        ', что означало образование протозвезды. '
        'Параллельно с этим, в разных областях диска начали появляться другие уплотнения, которые в будущем'
        ' послужат гравитационными центрами'
        ' для образования планет.\n \n'
        'Финальный этап формирования солнечной системы начался в период, когда температура центра протозвезды'
        ' превысила несколько миллионов кельвинов. '
        'Тогда гелий и водород вступили в реакцию термоядерного синтеза, что привело к появлению полноценной '
        'звезды. Остальные уплотнения диска постепенно сформировались в планеты, которые начали вращаться'
        ' в одном направлении вокруг Солнца, находясь на одной плоскости.')


async def start(update, context):
    user = update.effective_user
    global username
    username = user['username']

    db_sess = db_session.create_session()

    user_bd = db_sess.query(User).filter(User.username == username).first()
    print(user_bd)
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
        # МНОГО ТЕКСА?
        await update.message.reply_html('<b>Астрономическая картина дня</b> - '
                                        'Откройте для себя космос! Каждый день'
                                        ' появляется новое изображение или фотография нашей'
                                        ' удивительной Вселенной. вместе с кратким объяснением,'
                                        ' написанным профессиональным астрономом.')
        await update.message.reply_html('<b>Околоземные астероиды</b> - '
                                        'С помощью данной функции пользователь может: искать астероиды по дате'
                                        ' их ближайшего сближения с Землей, искать конкретный астероид'
                                        ' по его идентификатору малого тела NASA JPL, а также просматривать'
                                        ' общий набор данных.')
        await update.message.reply_html('<b>Камера для съёмки Земли</b> '
                                        'предоставляет информацию о ежедневных изображениях,'
                                        ' собираемых с помощью инструмента DSCOVR Earth Polychromatic'
                                        ' Imaging Camera (EPIC). Уникально расположенный в точке'
                                        ' Лагранжа между Землей и Солнцем, EPIC обеспечивает получение'
                                        ' полных изображений диска Земли и фиксирует уникальные'
                                        ' перспективы определенных астрономических событий, таких как'
                                        ' транзиты Луны, с помощью детектора CCD (Charge Coupled Device)'
                                        ' с разрешением 2048x2048 пикселей, соединенного с'
                                        ' 30-сантиметровой апертурой телескопа Кассегрена.')
    else:
        await update.message.reply_html(
            rf'Привет,{user.mention_html()}! Рады видеть тебя снова. Выбери интересующую функцию)' rf'',
            reply_markup=markup)


async def zayac(update, cotext):
    await update.message.reply_photo('zayac.jpg')


def main():
    token = os.environ.get('TOKEN', '')
    app = Application.builder().token(token).build()
    app.add_handler(conv_handler)
    app.add_handler(conv_handler2)
    app.add_handler(conv_handler3)

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('photo_NASA', photo_NASA))
    app.add_handler(CommandHandler('photo_of_the_Earth', photo_of_the_Earth))
    app.add_handler(CommandHandler('photo_Mars', photo_Mars))
    app.add_handler(CommandHandler('stop', stop))
    app.add_handler(CommandHandler('Info_func', Info_func))
    app.add_handler(CommandHandler('sun_sistem', sun_sistem))
    app.add_handler(CommandHandler('zayac', zayac))

    app.run_polling()


if __name__ == '__main__':
    main()
