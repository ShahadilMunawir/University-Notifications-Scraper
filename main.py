import time
import asyncio
import requests
from bs4 import BeautifulSoup
from creds import TelegramBot, ChatID
from telebot.async_telebot import AsyncTeleBot

flag = 0
bot = AsyncTeleBot(TelegramBot.API_KEY, parse_mode=None)

@bot.message_handler(commands=["start"])
async def start(msg):
    if msg.chat.id != ChatID.CS:
        await bot.send_message(msg.from_user.id, f"Hi, {msg.from_user.first_name}")
    else:
        await bot.reply_to(msg, "HI there, How is it going")

@bot.message_handler(commands=["updates"])
async def updates(msg):
    r = requests.get("https://pareekshabhavan.uoc.ac.in/index.php/examination/notifications", verify=False).content
    soup = BeautifulSoup(r, "html.parser")
    notification_objs = soup.findAll("li", class_="notif")[:5]
    message = "*"
    for i, notification in enumerate(notification_objs):
        if i == 4:
            message += notification.text
        else:
            message += notification.text+"\n\n*"
    await bot.reply_to(msg, message)

@bot.message_handler(commands=["update"])
def update(msg):
    while True:
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
                time.sleep(3600)
asyncio.run(bot.polling())