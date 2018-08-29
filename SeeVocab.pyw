import MySQLdb
from random import choice
from win10toast import ToastNotifier
import time
from datetime import datetime, timedelta

db = MySQLdb.connect(host="localhost", user="root", passwd="", db="spanish_vocabulary")

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

today =process(datetime.today().strftime("%m/%d/%Y"))



while True:

    cursor2.execute("SELECT words.word, logs.date FROM words, logs WHERE words.id = word_id ")
    log_data=cursor2.fetchall()
    for log in log_data:
        logs[log[0]]=log[1]


    cursor.execute("SELECT * FROM words")
    word_pair=choice((cursor.fetchall()))
    word_choice = word_pair[1]+" : "+word_pair[2] + "\n\n"+word_pair[3]
    if word_pair[1] not in logs:
        toaster.show_toast("Word of the Hour", word_choice,duration=10)
        cursor2.execute("INSERT INTO logs VALUES(%s, %s)", (word_pair[0], today))
        db.commit()

    else:
        continue


    cursor2.execute("SELECT * FROM logs LIMIT 1")
    last_date = datetime.strptime(cursor2.fetchone()[1], "%Y-%m-%d").date()
    delta = today - last_date
    if delta.days >= 2:
        cursor2.execute("DELETE FROM logs")
        db.commit()


    time.sleep(900)
