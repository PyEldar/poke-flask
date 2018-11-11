"""Searches online forum for trainer codes and stores them in MongoDB"""

from urllib.request import urlopen
from datetime import datetime
import re

from bs4 import BeautifulSoup
import pymongo

codes = []
base_url = "https://gbatemp.net/threads/pokemon-go-friend-code-thread.508383/page-"
for x in range(8, 92):
    url = base_url + str(x)
    print(url)
    html = urlopen(url)
    soup = BeautifulSoup(html)
    messages = soup.find_all("blockquote", class_="messageText SelectQuoteContainer ugc baseHtml")
    message = ",".join([Member.get_text() for Member in messages])
    codes += re.findall(r"\d\d\d\d \d\d\d\d \d\d\d\d", message) + re.findall(r"\d\d\d\d\d\d\d\d\d\d\d\d", message)

db = pymongo.MongoClient().pokeflask
for code in codes:
    if not (db.trainers.find({"code": code}).count() > 0):
        db.trainers.insert_one({"name": "", "code": code, "when": datetime.utcnow()})
    else:
        print("already exists")