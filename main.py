import requests
from bs4 import BeautifulSoup

r = requests.get("https://pareekshabhavan.uoc.ac.in/index.php/examination/notifications", verify=False).content
soup = BeautifulSoup(r, "html.parser")

notification_obj = soup.findAll("li", class_="notif")[0]
notification = notification_obj.text
link = notification_obj.a["href"].replace(" ", "%").replace("15", "2015")