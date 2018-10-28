from tkinter import *
import MySQLdb
import requests
from bs4 import BeautifulSoup
import re
from random import choice
from win10toast import ToastNotifier
import time
from datetime import datetime, timedelta, date
from threading import Thread

root = Tk()

db = MySQLdb.connect(host="localhost", user="root", passwd="", db="spanish_words")

cursor = db.cursor()

cursor2=db.cursor()

toaster=ToastNotifier()

logs={}



def process(d):
    global date
    y=int(d[6:]) # year
    m=int(d[:2]) #month
    d=int(d[3:5]) #day

    formatted_date=date(y,m,d)

    return formatted_date

def main_thread():
    while True:
        today = process(datetime.today().strftime("%m/%d/%Y"))
        cursor2.execute("SELECT words.word, logs.date FROM words, logs WHERE words.id = word_id ")
        log_data=cursor2.fetchall()
        for log in log_data:
            logs[log[0]]=log[1]

        if len(logs)>1:
            cursor2.execute("SELECT * FROM `logs` ORDER BY `logs`.`date` ASC")
            last_date = datetime.strptime(cursor2.fetchone()[1], "%Y-%m-%d").date()
            delta = today - last_date
            if delta.days >= 2:
                cursor2.execute("DELETE FROM logs")
                db.commit()


        cursor.execute("SELECT * FROM words")
        word_pair=choice((cursor.fetchall()))
        word_choice = word_pair[1]+" : "+word_pair[2] + "\n\n"+word_pair[3]
        if word_pair[1] not in logs:
            toaster.show_toast("Word of the Hour", word_choice,duration=20)
            cursor2.execute("INSERT INTO logs VALUES(%s, %s)", (word_pair[0], today))
            db.commit()

        else:
            continue



        time.sleep(dict[option_changed()])



t1=Thread(target=main_thread)
t1.start()


######### UI PART ###########


cursor3 = db.cursor()



pattern = re.compile(r'[^.!?]+[.!?]', re.MULTILINE | re.DOTALL)
url = "http://www.spanishdict.com/translate/"



def add_word(event=None):
    word = entry_1.get()
    meaning = entry_2.get()
    sample_sentences = []
    r = requests.get(url + word)
    soup = BeautifulSoup(r.content, "html.parser")

    for div in soup.find_all('div', {'class': 'dictionary-neodict-example'}):
        for s in div:
            s = s.text
            result = pattern.match(s)
            if result:
                sample_sentences.append(s)

    cursor3.execute("INSERT INTO words VALUES (%s,%s,%s,%s)", ('NULL', word, meaning, sample_sentences[0]))
    db.commit()
    sample_sentences.clear()
    entry_1.delete(0, END)
    entry_2.delete(0,END)



root.geometry('300x300')
root.title("SeeWord")

label_0 = Label(root, text="SeeWord",width=20,font=("bold", 20))
label_0.place(x=10,y=40)


label_1 = Label(root, text="Word:",width=20,font=("bold", 10))
label_1.place(x=10,y=130)


entry_1 = Entry(root, textvariable=StringVar())
entry_1.pack()
entry_1.place(x=122, y=130)



label_2 = Label(root, text="Meaning:",width=20,font=("bold", 10))
label_2.place(x=10,y=180)



entry_2 = Entry(root, textvariable=StringVar())
entry_2.pack()
entry_2.place(x=122,y=180)




send_button=Button(root, text='Add',width=20,bg='brown',fg='white',command=add_word)
send_button.pack()
send_button.place(x=100,y=250)


root.mainloop()


