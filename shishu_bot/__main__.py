from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler
import logging, os, re, urllib.request, json

ENV = bool(os.environ.get('ENV', False))
if ENV:
    TOKEN = os.environ.get('TOKEN', None)
else:
    from shishu_bot.config import Config
    TOKEN = Config.API_KEY

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

def get_ota_raw(codename, bot, update):
    ota_url = "https://raw.githubusercontent.com/BootleggersROM-Devices/BootleggersROM-Devices.github.io/master/_devices/"+codename+".md"
    ota_req = urllib.request.Request(ota_url)
    try:
        ota_resp = urllib.request.urlopen(ota_req)
    except:
        return 1
    else:
        ota_raw = ota_resp.read()
        return str(ota_raw)

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

# callback function for start handler
def start_callback(bot, update):
    if update.message.chat.type=="private":
        bot.send_message(chat_id=update.message.chat_id, text="Hi there", reply_to_message_id=update.message.message_id)

# callback function for device handler
def device_callback(bot, update, args):
    if len(args) <= 0:
        reply="You're getting there, but to use this command, be sure to specify your device. For example: `/device surnia`"
        bot.send_message(chat_id=update.message.chat.id, text=reply, reply_to_message_id=update.message.message_id,parse_mode="Markdown")

    codename = args[0]
    ota_raw = get_ota_raw(codename, bot, update)
    if ota_raw == 1:
        reply="Sorry, but "+codename+" isn't on our official devices list"
        bot.send_message(chat_id=update.message.chat.id, text=reply, reply_to_message_id=update.message.message_id)

    maintainer = re.findall(r"\\nmaintainer: (.*?)\\n", ota_raw)[0]
    filename = re.findall(r"\\nfilename: (.*?)\\n", ota_raw)[0]
    fullname = re.findall(r"\\nfullname: (.*?)\\n", ota_raw)[0]
    xdathread = re.findall(r"\\nxdathread: (.*?)\\n", ota_raw)[0]
    latest = "http://downloads.sourceforge.net/project/bootleggersrom/builds/"+codename+"/"+filename
    builds = "http://downloads.sourceforge.net/project/bootleggersrom/builds/"+codename

    button_list = [
    InlineKeyboardButton("XDA Thread", url=xdathread),
    InlineKeyboardButton("Latest Build", url=latest),
    InlineKeyboardButton("All Builds", url=builds)
    ]

    reply_buttons = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
    reply_text ="*BootleggersROM for "+fullname+" ("+codename+")\nMaintainer:* "+maintainer+"\n*Latest Build:* `"+filename+"`\n"

    bot.send_message(chat_id=update.message.chat_id, text=reply_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_buttons, reply_to_message_id=update.message.message_id)

# callback function for device list handler
def devicelist_callback(bot, update):
  # Check this every time because we update info very often
  with urllib.request.urlopen("https://bootleggersrom-devices.github.io/api/devices.json") as url:
    data = json.loads(url.read().decode())
  message = update.effective_message
  infoDevList = "<b>List of our currently supported devices:</b>"
  for key in data:
    infoDevList += "\n· " + key
  print(infoDevList)
  #if infoDevList = "":
  #  infoDevListmsg = "Sorry, but there's no official devices yet.
  bot.send_message(chat_id=update.message.chat_id, text=infoDevList, parse_mode=ParseMode.HTML, reply_to_message_id=update.message.message_id)

start_handler = CommandHandler('start', start_callback)
devicelist_handler = CommandHandler('devicelist', devicelist_callback)
device_handler = CommandHandler('device', device_callback, pass_args=True)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(device_handler)
dispatcher.add_handler(devicelist_handler)

updater.start_polling()
