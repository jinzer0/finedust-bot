import telebot
import logging
import requests as r
import datetime
import time
import urllib.parse

chatid = 1516844869
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
token = "1748668208:AAEAiTfvMkVCu6gB2nqYQjb08N7r0AraFrE"

bot = telebot.TeleBot(token, parse_mode="MarkdownV2")


def get_dustinfo():
    authkey = "kX4iHZtMYL1MjAo7wyux6wQw9cjY+AiY/bXFbO6DTkGQgoAqoGZSfpkR+RhIi1MlNauj5CJyY1RYPyWHuMf9pQ=="
    url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?"
    file = open("setup.txt", "r")
    line = file.readline()
    servicekey = urllib.parse.quote_plus(authkey)
    parameter = {
        "serviceKey": "kX4iHZtMYL1MjAo7wyux6wQw9cjY+AiY/bXFbO6DTkGQgoAqoGZSfpkR+RhIi1MlNauj5CJyY1RYPyWHuMf9pQ==",
        "dataTerm": "DAILY",
        "pageNo": 1,
        "numOfRows": 6,
        "returnType": "json",
        "ver": 1.0,
    }

    url = url + urllib.parse.urlencode(parameter, doseq=True)
    url = url + f"&stationName={line.strip()}"

    res = r.get(url)
    result = res.json()

    pm10 = result["response"]["body"]["items"][0]["pm10Value"]
    pm25 = result["response"]["body"]["items"][0]["pm25Value"]
    time = result["response"]["body"]["items"][0]["dataTime"].split()
    timestamp = time[1]
    print("Got the information...")

    file.close()

    return pm10, pm25, timestamp


def set_grade(result):
    pm10 = int(result[0])
    pm25 = int(result[1])

    if pm10 in [i for i in range(16)]:
        pm10grade = "최고"
    elif pm10 in [i for i in range(16, 31)]:
        pm10grade = "좋음"
    elif pm10 in [i for i in range(31, 41)]:
        pm10grade = "보통"
    elif pm10 in [i for i in range(41, 51)]:
        pm10grade = "보통"
    elif pm10 in [i for i in range(51, 76)]:
        pm10grade = "나쁨"
    elif pm10 in [i for i in range(76, 101)]:
        pm10grade = "아주나쁨"
    elif pm10 in [i for i in range(101, 151)]:
        pm10grade = "매우나쁨"
    else:
        pm10grade = "최악"

    if pm25 in [i for i in range(9)]:
        pm25grade = "최고"
    elif pm25 in [i for i in range(9, 16)]:
        pm25grade = "좋음"
    elif pm25 in [i for i in range(16, 21)]:
        pm25grade = "보통"
    elif pm25 in [i for i in range(21, 26)]:
        pm25grade = "보통"
    elif pm25 in [i for i in range(26, 38)]:
        pm25grade = "나쁨"
    elif pm25 in [i for i in range(38, 51)]:
        pm25grade = "아주나쁨"
    elif pm25 in [i for i in range(51, 76)]:
        pm25grade = "매우나쁨"
    else:
        pm25grade = "최악"

    return pm10grade, pm25grade


def alarm():
    with open("setup.txt") as f:
        clock = f.readlines()
        clock = clock[1]

    hour = int(clock[0:2])
    minute = int(clock[2:4])

    KST=datetime.timezone(datetime.timedelta(hours=9))
    current = datetime.datetime.now(tz=KST)

    aim = current.replace(hour=hour, minute=minute, second=00)

    gap = (aim - current).total_seconds()

    if gap < 0:
        gap = gap + 86400
    print(f"Time left... {gap}")
    return gap


def setloc(message):
    user_info(message)

    with open("setup.txt", "w") as file:
        file.write(message.text + "\n")

        bot.send_message(message.chat.id, "원하는 시간을 입력해주세요\. \n예\)0730, 1425")
        bot.register_next_step_handler(message, setclock)


def setclock(message):
    user_info(message)

    with open("setup.txt", "a") as file:
        file.write(message.text)

    bot.send_message(message.chat.id, "설정이 완료되었습니다\. /begin으로 알림을 시작하세요\.")


def user_info(message):
    epochtime = message.date
    user_id = message.chat.id
    message_id = message.message_id
    username_first = message.chat.first_name
    username_last = message.chat.last_name
    user_message = message.text

    realtime=time.localtime(epochtime+32400)

    text = f"""
USER : {username_first} {username_last}
ID : {user_id}
MESSAGE : {user_message}
ID_MESSAGE : {message_id}
DATE : {realtime.tm_year}-{realtime.tm_mon}-{realtime.tm_mday} {realtime.tm_hour}:{realtime.tm_min}:{realtime.tm_sec}"""
    print(text)


@bot.message_handler(commands=["start", "help"])
def send_start(message):
    user_info(message)

    bot.send_message(message.chat.id, "안녕하세요\. 원하는 시간에 미세먼지 농도를 알려주는 봇입니다\. 시작하시려면 /setting을 입력하세요\.")
    print(message.chat.id, message.message_id)


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)


@bot.message_handler(commands=["setting"])
def set_up(message):
    user_info(message)

    bot.send_message(message.chat.id, "원하는 지역을 입력해주세요\.\n예\)종로구, 강남구, 송파구")
    text = message.text
    print(text)
    bot.register_next_step_handler(message, setloc)


@bot.message_handler(commands=["begin"])
def begin_alert(message):
    user_info(message)
    print("\n")

    result = get_dustinfo()
    grade = set_grade(result)
    text = f"""
*_{result[2]} 기준_*
미세먼지 : {result[0]} \- {grade[0]}
초미세먼지 : {result[1]} \- {grade[1]}
"""

    bot.send_message(message.chat.id, text)

    with open("setup.txt", "r") as f:
        clock = f.readlines()
        clock = clock[1]
        hour = clock[0:2]
        minute = clock[2:4]

    time.sleep(0.5)
    text = f"""
알림이 켜졌습니다\.
다음 알림은 *_{hour}시 {minute}분_*에 발송됩니다\.
지역 혹은 시간을 바꾸시려면 /setting을 입력하세요\."""

    bot.send_message(message.chat.id, text)
    while True:
        print("\n\n")
        secs = alarm()
        time.sleep(secs)

        result = get_dustinfo()


        grade = set_grade(result)
        text = f"""
*_{result[2]} 기준_*
미세먼지 : {result[0]} \- {grade[0]}
초미세먼지 : {result[1]} \- {grade[1]}
"""

        bot.send_message(message.chat.id, text)
        time.sleep(3)


@bot.message_handler(commands=["test"])
def test_markdown(message):
    text = """
    *bold \*text*
_italic \*text_
__underline__
~strikethrough~
*bold _italic bold ~italic bold strikethrough~ __underline italic bold___ bold*
[inline URL](http://www.example.com/)
[inline mention of a user](tg://user?id=123456789)
`inline fixed-width code`
```
pre-formatted fixed-width code block
```
```python
pre-formatted fixed-width code block written in the Python programming language
```"""
    bot.send_message(message.chat.id, text)


bot.enable_save_next_step_handlers(delay=2)

bot.polling()
