from shishu_bot.config import Config
from telegram.ext import Updater, CommandHandler
import logging

TOKEN = Config.API_KEY
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# callback function for start handler
def start_callback(bot, update):
    if update.message.chat.type=="private":
        bot.send_message(chat_id=update.message.chat_id, text="Hi there")

# callback function for device handler
def device_callback(bot, update, args):
    bot.send_message(chat_id=update.message.chat_id, text=args[0])

start_handler = CommandHandler('start', start_callback)
device_handler = CommandHandler('device', device_callback, pass_args=True)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(device_handler)

updater.start_polling()