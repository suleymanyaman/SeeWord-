import MySQLdb
import os
import requests
from bs4 import BeautifulSoup
import re

db = MySQLdb.connect(host="localhost", user="root", passwd="", db="spanish_vocabulary")

cursor = db.cursor()

#Scraping the sentences from www.spanishdict.com

sample_sentences=[]

pattern = re.compile(r'[¿A-Z].*?[\.!?] ', re.MULTILINE | re.DOTALL)
url = "http://www.spanishdict.com/translate/"

while True:
    word = input("Word:")
    meaning=input("Meaning:")
    r = requests.get(url + word)
    soup = BeautifulSoup(r.content, "html.parser")



    for div in soup.find_all('div', {'class': 'dictionary-neodict-example'}):
        for s in div:
            s = s.text
            result = pattern.match(s)
            if result:
                sample_sentences.append(s)



    cursor.execute("INSERT INTO words VALUES (%s,%s,%s)", (word, meaning, sample_sentences[0]))
    os.system('cls') 
    db.commit()
    sample_sentences.clear()


