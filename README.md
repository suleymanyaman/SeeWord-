# SeeWord-
A desktop application, working as a reminder, to make the acquisition of vocabulary in language learning easier. 

The program works via a SQLite database. As a user, you add the target language words you encounter in different sources to the database
via UI panel. The program, every hour, sends you a Windows 10 notification at the right bottom corner of the screen, consisting of a random word, its meaning and the example sentence. The example sentence is directly scraped from spanishdict.com; you don't need to do anything about it. The rationale behind the application is to keep the words within the attention of the learner. A sample database was provided (data.sqlite) in order for you too see how it works. Just replace the 

How to install from the scratch?

1 - Click setup_seeword. This will create the necessary tables for the program. 

2 - Open ui.pyw (the main script). As you have no words registered yet, the listbox will appear empty.

3 - Add some words with their meanings. 

4 - Restart the program. 
