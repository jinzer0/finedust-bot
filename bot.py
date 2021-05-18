import telebot
import logging
import requests as r
import pprint as p
import urllib.parse

chatid=1516844869
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
token = "1748668208:AAEAiTfvMkVCu6gB2nqYQjb08N7r0AraFrE"

url="http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?"
authkey="kX4iHZtMYL1MjAo7wyux6wQw9cjY+AiY/bXFbO6DTkGQgoAqoGZSfpkR+RhIi1MlNauj5CJyY1RYPyWHuMf9pQ=="


bot = telebot.TeleBot(token, parse_mode=None)

def get_dustinfo():
    file = open("setup.txt","r")
    lines = file.readlines()
    servicekey=urllib.parse.quote_plus(authkey)
    parameter = {
        "stationName": lines[0],
        "dataTerm": "DAILY",
        "pageNo": 1,
        "numOfRows": 6,
        "returnType": "json",
        "ver": 1.0,
        "serviceKey": servicekey
    }
    url=url+urllib.parse.urlencode(parameter, doseq=True)
    res = r.get(url, params=parameter)
    result = res.json()

    print(result["response"]["body"]["items"][0]["pm10Value"])



def setloc(message):
    with open("setup.txt", "w") as file:
        file.write(message.text+"\n")


def setclock(message):
    with open("setup.txt", "x") as file:
        file.write(message.text)


@bot.message_handler(commands=["start", "help"])
def send_start(message):
    bot.send_message(message.chat.id, "안녕하세요. 원하는 시간에 미세먼지 농도를 알려주는 봇입니다. 시작하시려면 /setting을 입력하세요.")
    print(message.chat.id, message.message_id)


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)


@bot.message_handler(commands="setting")
def set_up(message):
    bot.send_message(message.chat.id, "원하는 지역을 입력해주세요.\n예)종로구, 강남구, 송파구")
    text = message.text
    print(text)
    bot.register_next_step_handler(message, setloc)

    bot.send_message(message.chat.id, "원하는 시간을 입력해주세요. \n예)0730, 1400")
    bot.register_next_step_handler(message, setclock)

    file = open("setup.txt", "r")
    print(file.readlines())
    bot.send_message(message.chat.id, "설정이 완료되었습니다. /begin으로 알림을 시작하세요.")


@bot.message_handler(commands="begin")
def begin_alert(message):
    bot.


bot.polling()

userid="1516844869"
updateid="456291961"
messageid="53"
goal = url+token+"/forwardMessage"
para ={
    "chat_id": chatid,
    "from_chat_id": chatid,
    "meessage_id": 59

}
# real = url+token+"/copyMessage/"+urllib.parse.urlencode(para, doseq=True)
# print(real)
#
res = r.post(goal,data=para)
print(res)
print(res.json())