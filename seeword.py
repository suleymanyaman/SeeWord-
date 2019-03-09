import sqlite3
from random import choice
from win10toast import ToastNotifier
import time
from datetime import datetime, timedelta, date


db = sqlite3.connect("seeworddb.db")
cursor = db.cursor()

toaster=ToastNotifier()

logs={}


cursor.execute("SELECT * FROM words")


def process(d):
    global date
    y=int(d[6:]) # year
    m=int(d[:2]) #month
    d=int(d[3:5]) #day

    formatted_date=date(y,m,d)

    return formatted_date


ten_days = []
this_month=[]
today = process(datetime.today().strftime("%m/%d/%Y"))

cursor.execute("SELECT * FROM words")
for i in (cursor.fetchall()):
    if (today - datetime.strptime(i[4], "%Y-%m-%d").date()).days <= 10:  # For 10 days
        ten_days.append(i)


    elif datetime.today().strftime("%d") == "30" and int((i[4])[5:7]) == datetime.today().month:  # Last Month
        this_month.append(i)

while True:

    cursor.execute("SELECT words.word, logs.date FROM words, logs WHERE words.id = word_id ")
    log_data=cursor.fetchall()
    for log in log_data:
        logs[log[0]]=log[1]

    if len(logs)>1:
        cursor.execute("SELECT * FROM `logs` ORDER BY `logs`.`date` ASC")
        last_date = datetime.strptime(cursor.fetchone()[1], "%Y-%m-%d").date()
        delta = today - last_date
        if delta.days >= 2:
            cursor.execute("DELETE FROM logs")
            db.commit()

    cursor.execute("SELECT * FROM words")

    #Processing the special conditions like 10 days, end_of_month etc.

    # 10 days
    if set([x[1] for x in ten_days ]) & set(logs.keys())  != set([x[1] for x in ten_days]):
        word_row = choice(ten_days)
        if word_row[1] in logs:
            continue
        else:
            ten_word_content = word_row[1]+":"+word_row[2]+"\n\n"+word_row[3]
            toaster.show_toast("Word of the Hour", ten_word_content)
            cursor.execute("INSERT INTO logs VALUES(?, ?)", (word_row[0], today))
            db.commit()

    elif set([x[1] for x in this_month]) & set(logs.keys()) != set([x[1] for x in this_month]):
        word_row_month = choice(this_month)
        if word_row_month[1] in logs:
            continue
        else:
            month_word_content = word_row_month[1]+":"+word_row_month[2]+"\n\n"+word_row_month[3]
            toaster.show_toast("Word of the Hour", month_word_content)
            cursor.execute("INSERT INTO logs VALUES(?, ?)", (word_row_month[0], today))
            db.commit()

    else:
        random_choice = choice(cursor.fetchall())
        random_content = random_choice[1]+":"+random_choice[2]+"\n\n"+random_choice[3]
        toaster.show_toast("Word of the Hour", random_content)
        cursor.execute("INSERT INTO logs (word_id, date) VALUES(?, ?)", (random_choice[0], today))
        db.commit()

    time.sleep(3600)








