from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import telegram.update
import logging

token = "1748668208:AAEAiTfvMkVCu6gB2nqYQjb08N7r0AraFrE"

updater = Updater(token=token, use_context=True)
dispatch = updater.dispatcher

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

loc = ""
time = ""

def setloc(location):
    global loc
    loc = location


def settime(timee):
    global time
    time=timee


def getinfo(location, time):


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="""
    안녕하세요. 사용자가 원하는 시간에 지정된 지역의 미세먼지 농도를 알려주는 봇입니다.
    시작하시려면 /set 을 입력해주세요.
    현재는 서울 지역만 가능합니다. """)


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def set_location(update, context):
    global output
    context.bot.send_message(chat_id=update.effective_chat.id, text="설정하려는 지역을 입력해주세요. 예)종로구, 강남구, 송파구")
    text=update.message.text
    print(update.message.text)
    print(update.message.message_id)
    print(update.message.chat)
    return setloc(text)


def set_time(update, context):
    global time
    context.bot.send_message(chat_id=update.effective_chat.id, text="설정하려는 시간을 입력해주세요. 예)9 30, 15 00")
    time = update.message.text
    return settime(time)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def begin(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Alarm started...")
    getinfo(loc, time)


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatch.add_handler(echo_handler)

start_handler = CommandHandler('start', start)
dispatch.add_handler(start_handler)

caps_handler = CommandHandler('caps', caps)
dispatch.add_handler(caps_handler)

set_loc_handler = CommandHandler("location", set_location)
dispatch.add_handler(set_loc_handler)

set_time_handler = CommandHandler("time", set_time)
dispatch.add_handler(set_time_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatch.add_handler(unknown_handler)

updater.start_polling()
