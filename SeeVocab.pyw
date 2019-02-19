from tkinter import *
from tkinter import messagebox
import MySQLdb
import requests
from bs4 import BeautifulSoup
import re
from random import choice
from win10toast import ToastNotifier
import time
from datetime import datetime, timedelta, date
from threading import Thread
import six 

root = Tk()
import tkinter
import tempfile

ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
    b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
    b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

root.iconbitmap(default="C:/Users/asus/Desktop/SeeWord/transparent.ico")

db = MySQLdb.connect(host="45.63.101.196", user="suleyman_yaman", passwd="19971234", db="suleyman_seeword")

cursor = db.cursor()

#cursor2=db.cursor()

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
        global db
        cursor2 = db.cursor()
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
            db = MySQLdb.connect(host="45.63.101.196", user="suleyman_yaman", passwd="19971234", db="suleyman_seeword")
            cursor2  = db.cursor()
            cursor2.execute("INSERT INTO logs VALUES(%s, %s)", (word_pair[0], today))
            db.commit()

        else:
            continue



        time.sleep(3600)



t1=Thread(target=main_thread)
t1.start()


######### UI PART ###########


cursor3 = db.cursor()


pattern = re.compile(r'[^.!?]+[.!?]', re.MULTILINE | re.DOTALL)
url = "http://www.spanishdict.com/translate/"



def view_the_words():
    tk = Toplevel()
    scrollbar = Scrollbar (tk)
    word_list = Listbox(tk, height=30, width=30, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    MySQLdb.connect(host="45.63.101.196", user="suleyman_yaman", passwd="19971234", db="suleyman_seeword")
    cursor.execute("SELECT * FROM words")
    word_list.pack(side=LEFT, fill=BOTH)
    rows = cursor.fetchall()
    for row in rows:
        word_list.insert(END, row[1]+":"+row[2])

def delete_frame():
    tk=Toplevel()
    tk.geometry("500x100")
    note = Label(tk, text="Enter the word you want to delete.")
    note.place(x=30, y=10)
    word_deleted = Entry(tk)
    word_deleted.pack()
    word_deleted.place(x=30, y=45)

    def delete_word():
        cursor.execute("DELETE FROM words WHERE word = '{}' ".format(word_deleted.get()))
        db.commit()
        messagebox._show("SeeWord", "The word you chose was deleted succesfully.")

    delete_button = Button(tk, text="Delete", width=5, bg='brown', fg='white', command=delete_word)
    delete_button.pack()
    delete_button.place(x=170, y=45)


root.geometry('400x400')
root.title("SeeWord")

label_0 = Label(root, text="SeeWord\n Control Panel",width=20,font=("bold", 20))
label_0.place(x=10,y=40)

def add_word_frame():
    tk = Toplevel()
    label_1 = Label(tk, text="Word:",width=20,font=("bold", 10))
    label_1.place(x=10,y=130)

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


        db = MySQLdb.connect(host="45.63.101.196", user="xxxxx", passwd="xxxxx", db="xxxxx")
        cursor3 = db.cursor()
        cursor3.execute("INSERT INTO words VALUES (%s,%s,%s,%s)", ("NULL", word, meaning, sample_sentences[0]))
        db.commit()
        sample_sentences.clear()
        entry_1.delete(0, END)
        entry_2.delete(0, END)


    entry_1 = Entry(tk, textvariable=StringVar())
    entry_1.bind("<Return>", add_word)
    entry_1.pack()
    entry_1.place(x=122, y=130)


    label_2 = Label(tk, text="Meaning:",width=20,font=("bold", 10))
    label_2.place(x=10,y=180)


    entry_2 = Entry(tk, textvariable=StringVar())
    entry_2.bind("<Return>", add_word)
    entry_2.pack()
    entry_2.place(x=122,y=180)

    add_button = Button(tk, text='Add a word', width=20, bg='brown', fg='white', command=add_word)
    add_button.pack()
    add_button.place(x=100, y=250)



send_button=Button(text='Add a word',width=20,bg='brown',fg='white',command=add_word_frame)
send_button.pack()
send_button.place(x=100,y=150)


view_words=Button(root, text="View the words", width=20, bg='brown', fg='white', command=view_the_words)
view_words.pack()
view_words.place(x=100, y=200)

delete_words=Button(root, text="Delete a word", width=20, bg='brown', fg='white', command=delete_frame)
delete_words.pack()
delete_words.place(x=100, y=250)


root.mainloop()
