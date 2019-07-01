from shishu_bot.config import Config
from telegram.ext import Updater, CommandHandler

TOKEN = Config.API_KEY

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# callback function for start handler
def start_callback(bot, update):
    if update.message.chat.type=="private":
        bot.send_message(chat_id=update.message.chat_id, text="Hi there")

start_handler = CommandHandler('start', start_callback)

dispatcher.add_handler(start_handler)

updater.start_polling()