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

def get_ota_raw(codename, bot, update, isBeta):
	if isBeta == True:
		ota_req = urllib.request.Request("https://raw.githubusercontent.com/BootleggersROM-Devices/BootleggersROM-Devices.github.io/master/_devicesbeta/"+codename+".md")
	else:
		ota_req = urllib.request.Request("https://raw.githubusercontent.com/BootleggersROM-Devices/BootleggersROM-Devices.github.io/master/_devices/"+codename+".md")

	try:
		ota_resp = urllib.request.urlopen(ota_req)
	except:
		return 1
	else:
		ota_raw = ota_resp.read()
		return str(ota_raw)

def check_device_beta(codename, bot, update):
	# This will throw a special error in case of the device status. The code will throw a special number in case of a specific status
	device_beta = get_ota_raw(codename, bot, update, True)
	device_normal = get_ota_raw(codename, bot, update, False)
	if device_beta != 1 and device_normal != 1:
		return 3
	elif device_beta != 1 and device_normal == 1:
		return 2
	elif device_beta == 1 and device_normal != 1:
		return 1
	else:
		return 0

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
		reply="You're getting there, but to use this command, be sure to specify your device. For example: `/device surnia`, or, in case you want a beta version you can specify beta after your device name (For example: `/device surnia beta`) . Or, if you want to know all our shishufied (and currently supported) devices, use `/devicelist` or `/device list`."
		bot.send_message(chat_id=update.message.chat.id, text=reply, reply_to_message_id=update.message.message_id, parse_mode="Markdown")
		return

	codename = args[0]
	try:
		extraArgs = args[1]
	except IndexError:
		extraArgs = 'null'

	deviceOCode = check_device_beta(codename,bot,update)

	if "list" in codename:
		if "beta" in extraArgs:
			devicelist_callback(bot, update, True)
			return
		else:
			devicelist_callback(bot, update, False)
			return

	else:
		if "beta" in extraArgs:
			ota_raw = get_ota_raw(codename, bot, update, True)
			if ota_raw == 1:
				if deviceOCode == 1:
					reply="Sorry, but *"+codename+"* doesn't have any beta builds yet. Only stable releases for now. Remember to use `/device "+codename+"` to get those releases."
					bot.send_message(chat_id=update.message.chat.id, text=reply, reply_to_message_id=update.message.message_id, parse_mode="Markdown")
					return
				elif deviceOCode == 0:
					reply="Sorry, but *"+codename+"* isn't on our official devices list"
					bot.send_message(chat_id=update.message.chat.id, text=reply, reply_to_message_id=update.message.message_id, parse_mode="Markdown")
					return
		else:
			ota_raw = get_ota_raw(codename, bot, update, False)
			if ota_raw == 1:
				if deviceOCode == 2:
					reply="Sorry, but *"+codename+"* doesn't have any stable builds yet. Only beta releases for now. Remember to use `/device "+codename+" beta` to get those releases."
					bot.send_message(chat_id=update.message.chat.id, text=reply, reply_to_message_id=update.message.message_id, parse_mode="Markdown")
					return
				elif deviceOCode == 0:
					reply="Sorry, but *"+codename+"* isn't on our official devices list"
					bot.send_message(chat_id=update.message.chat.id, text=reply, reply_to_message_id=update.message.message_id, parse_mode="Markdown")
					return

	try:
		maintainer = re.findall(r"\\nmaintainer: (.*?)\\n", ota_raw)[0]
	except:
		maintainer = 'null'
	try:
		filename = re.findall(r"\\nfilename: (.*?)\\n", ota_raw)[0]
	except:
		filename = 'null'
	try:
		fullname = re.findall(r"\\nfullname: (.*?)\\n", ota_raw)[0]
	except:
		fullname = 'null'
	try:
		xdathread = re.findall(r"\\nxdathread: (.*?)\\n", ota_raw)[0]
	except:
		xdathread = 'null'
	try:
		notes = re.findall(r"\\nnotes: (.*?)\\n", ota_raw)[0]
	except:
		notes = 'null'
 
	latest = "http://downloads.sourceforge.net/project/bootleggersrom/builds/"+codename+"/"+filename
	latestbeta = "http://downloads.sourceforge.net/project/bootleggersrom/builds/"+codename+"/beta/"+filename
	betabuilds = "http://downloads.sourceforge.net/project/bootleggersrom/builds/"+codename+"/beta"
	builds = "http://downloads.sourceforge.net/project/bootleggersrom/builds/"+codename

	button_list = []
	if ("xda-developers" in xdathread) and (not "beta" in extraArgs):
		button_list.extend([InlineKeyboardButton("XDA Thread", url=xdathread)])

	if ("beta" in extraArgs):
		button_list.extend([
		InlineKeyboardButton("Latest Build", url=latestbeta),
		InlineKeyboardButton("Beta Builds", url=betabuilds),
		InlineKeyboardButton("Stable builds", url=builds)
		])
	else:
		button_list.extend([
		InlineKeyboardButton("Latest Build", url=latest),
		InlineKeyboardButton("All Builds", url=builds)
		])

	reply_buttons = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
	if (not "beta" in extraArgs):
		reply_text ="*BootleggersROM for "+fullname+" ("+codename+")\nMaintainer:* "+maintainer+"\n*Latest Build:* `"+filename+"`\n"
	else:
		if (notes is not 'null'):
			reply_text ="*BootleggersROM for "+fullname+" ("+codename+")*\n*Maintainer:* "+maintainer+"\n*Latest Build:* `"+filename+"`\n*Build notes:* "+notes+"\n*DISCLAIMER:* This is a beta build just for testing. Please, don't pull a Xiaomi Global on us and send logs when things gets broken."
		else:
			reply_text ="*BootleggersROM for "+fullname+" ("+codename+")*\n*Maintainer:* "+maintainer+"\n*Latest Build:* `"+filename+"`\n*DISCLAIMER:* This is a beta build just for testing. Please, don't pull a Xiaomi Global on us and send logs when things gets broken."

	bot.send_message(chat_id=update.message.chat_id, text=reply_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_buttons, reply_to_message_id=update.message.message_id)

# Woraround to parse args on devicelist
def devicelist_args_callback(bot, update, args):
	if len(args) <= 0:
		devicelist_callback(bot, update, False)
		return

	try:
		extraArgs = args[0]
	except IndexError:
		extraArgs = 'null'

	if ("beta" in extraArgs):
		devicelist_callback(bot, update, True)
		return
	else:
		devicelist_callback(bot, update, False)
		return

# callback function for device list handler
def devicelist_callback(bot, update, isBeta):
	# Check this every time because we update info very often
	if isBeta == True:
		otaURL = "https://bootleggersrom-devices.github.io/api/devices-beta.json"
	else:
		otaURL = "https://bootleggersrom-devices.github.io/api/devices.json"
	with urllib.request.urlopen(otaURL) as url:
		data = json.loads(url.read().decode())
	message = update.effective_message
	if isBeta == True:
		infoDevList = "<b>List of our supported devices currently in beta:</b>"
	else:
		infoDevList = "<b>List of our currently supported devices:</b>"

	for key in data:
		infoDevList += "\n· " + key

	#if infoDevList = "":
	#  infoDevListmsg = "Sorry, but there's no official devices yet.
	bot.send_message(chat_id=update.message.chat_id, text=infoDevList, parse_mode=ParseMode.HTML, reply_to_message_id=update.message.message_id)

start_handler = CommandHandler('start', start_callback)
devicelist_handler = CommandHandler('devicelist', devicelist_args_callback, pass_args=True)
device_handler = CommandHandler('device', device_callback, pass_args=True)
devices_handler = CommandHandler('devices', devicelist_args_callback, pass_args=True)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(device_handler)
dispatcher.add_handler(devicelist_handler)
dispatcher.add_handler(devices_handler)

updater.start_polling()
