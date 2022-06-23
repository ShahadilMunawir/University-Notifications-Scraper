import time
import asyncio
import requests
import threading
from bs4 import BeautifulSoup
from creds import TelegramBot, ChatID
import telebot

flag = 0
bot = telebot.TeleBot(TelegramBot.API_KEY, parse_mode=None)

@bot.message_handler(commands=["start"])
def start(msg):
    if msg.chat.id != ChatID.CS:
        bot.send_message(msg.from_user.id, f"Hi, {msg.from_user.first_name}")
    else:
        bot.reply_to(msg, "HI there, How is it going")
@bot.message_handler(commands=["updates"])
def updates(msg):
    r = requests.get("https://pareekshabhavan.uoc.ac.in/index.php/examination/notifications", verify=False).content
    soup = BeautifulSoup(r, "html.parser")
    notification_objs = soup.findAll("li", class_="notif")[:5]
    message = "*"
    for i, notification in enumerate(notification_objs):
        if i == 4:
            message += notification.text
        else:
            message += notification.text+"\n\n*"
    bot.reply_to(msg, message)

@bot.message_handler(commands=["update"])
def update(msg):
    global flag
    flag = 0
    while True:
        if flag == 0:
            r = requests.get("https://pareekshabhavan.uoc.ac.in/index.php/examination/notifications", verify=False).content
            soup = BeautifulSoup(r, "html.parser")
            file = open("updates.txt", "r")
            notification_obj = soup.findAll("li", class_="notif")[0]
            if str(msg.chat.id) == ChatID.CS:
                if file.read() != notification_obj.text:
                    link = notification_obj.a["href"].replace(" ", "%").replace("15", "2015")
                    latest_notification = notification_obj.text
                    file = open("updates.txt", "w")
                    file.write(latest_notification)
                    bot.send_message(ChatID.CS, latest_notification+"\n"+link)
            # time.sleep(3600)
        else:
            break

@bot.message_handler(commands=["stop"])
def stop(msg):
    global flag
    flag = 1
    bot.reply_to(msg, "I got stopped")
threading.Thread(target=updates)
threading.Thread(target=stop)
bot.polling()