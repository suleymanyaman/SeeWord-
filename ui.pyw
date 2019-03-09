from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import subprocess
import sqlite3
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta, date
from functools import partial

#Clear history is problematic
#Closing is problematic


#p = subprocess.Popen("seeword.py",  shell=True)
db = sqlite3.connect("data.sqlite")
cursor = db.cursor()



def process(d):
    global date
    y=int(d[6:]) # year
    m=int(d[:2]) #month
    d=int(d[3:5]) #day

    formatted_date=date(y,m,d)

    return formatted_date

def closeEvent(self,event):
    choice = QMessageBox.question(self, "Quit", "Do you want to quit SeeWord?", QMessageBox.Yes, QMessageBox.No)
    if choice == QMessageBox.Yes:
        #subprocess.call(['taskkill', '/F', '/T', '/PID', str(p.pid)])
        event.accept()
    else:
        event.ignore()

pattern = re.compile(r'[^.!?]+[.!?]', re.MULTILINE | re.DOTALL)
url = "http://www.spanishdict.com/translate/"

app = QApplication(sys.argv)

#Add a word

add_word_frame = QFrame()
add_word_frame.setFixedSize(300,300)

word_label = QLabel("Word:", add_word_frame)
meaning_label=QLabel("Meaning:", add_word_frame)

word = QLineEdit(add_word_frame)
word.setGeometry(90,80,80,25)
word_label.setGeometry(50, 65, 50, 50)

meaning = QLineEdit(add_word_frame)
meaning.setGeometry(90,110,80,25)
meaning_label.setGeometry(38, 95, 50,50)

def add_word():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("SeeWord")
    msg.setText("Congratulations! ")
    msg.setInformativeText("The word was added successfully.")
    global word
    global meaning
    word_text = word.text().strip()
    meaning_text = meaning.text()
    sample_sentences = []
    r = requests.get(url + word_text)
    soup = BeautifulSoup(r.content, "html.parser")

    for div in soup.find_all('div', {'class': 'dictionary-neodict-example'}):
        for s in div:
            s = s.text
            result = pattern.match(s)
            if result:
                sample_sentences.append(s)

    cursor.execute("INSERT INTO words (word,meaning,sentence,date) VALUES (?,?,?,?)", (word_text, meaning_text, sample_sentences[0], process(datetime.today().strftime("%m/%d/%Y"))))
    db.commit()
    sample_sentences.clear()


    word.setText("")
    meaning.setText("")
    msg.exec_()


add_button = QPushButton("Add",add_word_frame)
add_button.setGeometry(90,150,80,25)
add_button.clicked.connect(add_word)

#Delete word



def delete_word():
    global cursor
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("SeeWord")
    msg.setText("Congratulations! ")
    msg.setInformativeText("The word was deleted successfully.")
    cursor.execute("DELETE FROM words WHERE word ='{}'".format(delete_entry.text()))
    db.commit()
    msg.exec_()



#Control panel
control_panel=QFrame()
control_panel.setFixedSize(300,300)
l1=QLabel("SeeWord", control_panel)
l2=QLabel("\nControl Panel", control_panel)

font_1 = QFont("Times", 12, QFont.Bold)
font_2 =  QFont("Times", 9, QFont.Bold)

l1.setFont(font_1)
l1.setGeometry(100,-30,100,100)
l2.setGeometry(90, -10, 100,100)
l2.setFont(font_2)

return_to_main=QPushButton("Return to control panel ",add_word_frame)
return_to_main.setGeometry(70,180,125,25)
return_to_main.clicked.connect(add_word_frame.hide)
return_to_main.clicked.connect(control_panel.show)


word_list = QListWidget(control_panel)
word_list.setGeometry(10,10,200,250)
cursor.execute("SELECT * FROM words")
rows = cursor.fetchall()
for row in rows:
    word_list.addItem(row[1] + ":" + row[2])


add_button = QPushButton("Add a word",control_panel)
add_button.setGeometry(215, 50, 80,50)
add_button.clicked.connect(control_panel.hide)
add_button.clicked.connect(add_word_frame.show)

def get_row():
    row = word_list.currentItem().text()
    index_colon = row.index(":")
    word = row[:index_colon]
    cursor.execute("DELETE FROM words WHERE word ='{}'".format(word))
    db.commit()
    cursor.execute("SELECT * FROM words")
    print(cursor.fetchall())
    word_list.takeItem(word_list.currentRow())

delete=QPushButton("Delete a word", control_panel)
delete.setGeometry(215,100,80,50)
delete.clicked.connect(get_row)



control_panel.closeEvent = partial(closeEvent, control_panel)

control_panel.show()
sys.exit(app.exec())
