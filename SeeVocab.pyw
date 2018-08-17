import MySQLdb
from random import choice
from win10toast import ToastNotifier
import time
from datetime import datetime, timedelta

time.sleep(30)


today_date=datetime.today()
today=datetime.today().strftime("%x")

dead_line=today_date-timedelta(days=2)



db = MySQLdb.connect(host="localhost", user="root", passwd="", db="spanish_vocabulary")

cursor = db.cursor()

cursor2=db.cursor()

toaster=ToastNotifier()

logs={}

while True:
    cursor2.execute("SELECT * FROM logs")
    log_data = cursor2.fetchall()
    for log in log_data:
        logs[log[0]]=log[1]

    if dead_line.strftime("%x") in logs.values():
        cursor2.execute("DELETE FROM logs")
        db.commit()

    cursor.execute("SELECT * FROM words")
    word_pair=choice((cursor.fetchall()))
    word_choice = word_pair[0]+" : "+word_pair[1] + "\n\n"+word_pair[2]
    if word_pair[0] not in logs:
        toaster.show_toast("Word of the Hour", word_choice,duration=5)
        cursor.execute("INSERT INTO logs VALUES(%s, %s)", (word_pair[0], today))
        db.commit()

    else:
        continue

    time.sleep(900)



