import os
from requests import get
from dotenv import load_dotenv
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup

load_dotenv()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

reply_keyboard = [["/photo_of_the_Earth"], ["/near_Earth_asteroids"], ["/photo_NASA"], ["/start"]]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

async def stop(update, context):
    await update.message.reply_text("BB")
    return ConversationHandler.END
async def photo_of_the_Earth(update, context):
    await update.message.reply_html('Введите дату которая вас интересует,'
                                    ' и мы отправим вам фото земли в этот день')
    return 1

async def stop(update, context):
    await update.message.reply_text("BB")
    return ConversationHandler.END

async def first_response(update, context):
    locality = update.message.text
    print(locality)
    api_key = 'iuCdE8es7d2DuclaVnHviPHbWC8fRT21VfnAykJT'
    url = f'https://api.nasa.gov/planetary/apod?date={locality}&api_key={api_key}'
    file = get(url).json()

    if len(file) != 0:
        if len(file) != 1:
            for num in file:
                if num == 'url':
                    url = file['url']
    await update.message.reply_photo(url)


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('photo_of_the_Earth', photo_of_the_Earth)],
    states={
        # Функция читает ответ на первый вопрос и задаёт второй.
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)]

    },
    fallbacks=[CommandHandler('stop', stop)])

async def photo_of_the_Earth(update, context):
    await update.message.reply_html('Введите дату которая вас интересует,'
                                    ' и мы отправим вам фото земли в этот день')
    return 1


async def first_response(update, context):
    locality = update.message.text
    api_key = 'iuCdE8es7d2DuclaVnHviPHbWC8fRT21VfnAykJT'
    url = f'https://api.nasa.gov/planetary/apod?date={locality}&api_key={api_key}'
    file = get(url).json()

    if len(file) != 0:
        if len(file) != 1:
            for num in file:
                if num == 'url':
                    url = file['url']
    await update.message.reply_photo(url)


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('photo_of_the_Earth', photo_of_the_Earth)],
    states={
        # Функция читает ответ на первый вопрос и задаёт второй.
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)]

    },
    fallbacks=[CommandHandler('stop', stop)])


async def start(update, context):
    user = update.effective_user
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


async def func(update, context):
    funcc = update.message.text
    await update.message.reply_text(f"Укажите дату")
    return 2, funcc


async def data(update, funcc):
    date = update.message.text
    await update.message.reply_text(f'Ваша функция:{funcc}\n Ваша дата {date}')  # pеревести объект тг в текст





async def near_Earth_asteroids(update, context):
    await update.message.reply_html('*Алиса умница ваще')


async def photo_NASA(update, context):
    await update.message.reply_html(
        'Введите интересующую вас дату, и мы вышлем вам фото которое NASA сделала в это день')



async def near_Earth_asteroids(update, context):
    await update.message.reply_html('*Алиса умница ваще')


async def photo_NASA(update, context):
    await update.message.reply_html(
        'Введите интересующую вас дату, и мы вышлем вам фото которое NASA сделала в это день')


async def stop(update, context):
    await update.message.reply_text("BB")
    return ConversationHandler.END


def main():
    token = os.environ.get('TOKEN', '')
    app = Application.builder().token(token).build()
    app.add_handler(conv_handler)  ###размер кнопок  текст на руском?
    app.add_handler(CommandHandler('start', start))
    # app.add_handler(CommandHandler('stop', stop))
    app.add_handler(CommandHandler('photo_of_the_Earth', photo_of_the_Earth))
    app.add_handler(CommandHandler('near_Earth_asteroids', near_Earth_asteroids))
    app.add_handler(CommandHandler('photo_NASA', photo_NASA))

    app.run_polling()


if __name__ == '__main__':
    main()
