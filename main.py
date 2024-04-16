import os

import aiohttp
from dotenv import load_dotenv
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup

load_dotenv()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

reply_keyboard = [['/start', '/info', '/photo_of_the_Earth', '/weather_on_Mars', '/photo_NASA']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет,{user.mention_html()}! Это телеграмм бот NASA, выбери, что именно тебя интересует:)"
        rf'', reply_markup=markup)


async def info(update, context):
    await update.message.reply_html('{photo_of_the_Earth} - фото земли по дате;'
                                    '{weather_on_Mars} - погода на марсе;'
                                    '{photo_NASA} - фото которое сделала NASA в определенную дату')


async def photo_of_the_Earth(update, context):
    await update.message.reply_html('Введите дату которая вас интересует, и мы отправим вам фото земли в этот день')


async def weather_on_Mars(update, context):
    await update.message.reply_html('*здесь будет погода')

async def photo_NASA(update, context):
    await update.message.reply_html('Введите интересующую вас дату, и мы вышлем вам фото которое NASA сделала в это день')


def main():
    token = os.environ.get('TOKEN', '')
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('info', info))
    app.add_handler(CommandHandler('photo_of_the_Earth', photo_of_the_Earth))
    app.add_handler(CommandHandler('weather_on_Mars', weather_on_Mars))
    app.add_handler(CommandHandler('photo_NASA', photo_NASA))
    app.run_polling()


if __name__ == '__main__':
    main()
