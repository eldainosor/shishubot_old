from shishu_bot.config import Config
from telegram.ext import Updater, CommandHandler
import logging, urllib.request

TOKEN = Config.API_KEY
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

def get_ota_raw(codename):
    ota_url = "https://raw.githubusercontent.com/BootleggersROM-Devices/BootleggersROM-Devices.github.io/master/_devices/"+codename+".md"
    ota_req = urllib.request.Request(ota_url)
    ota_resp = urllib.request.urlopen(ota_req)
    ota_raw = ota_resp.read()
    return str(ota_raw)

# callback function for start handler
def start_callback(bot, update):
    if update.message.chat.type=="private":
        bot.send_message(chat_id=update.message.chat_id, text="Hi there")

# callback function for device handler
def device_callback(bot, update, args):
    codename = args[0]
    ota_raw = get_ota_raw(codename)

start_handler = CommandHandler('start', start_callback)
device_handler = CommandHandler('device', device_callback, pass_args=True)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(device_handler)

updater.start_polling()