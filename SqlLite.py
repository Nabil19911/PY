import sqlite3
with sqlite3.connect("try.db") as db:
    cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS user(userID INTEGER PRIMARY KEY, username VARCHAR(20) NOT NULL,
firstname VARCHAR(20) NOT NULL, surname VARCHAR(20) NOT NULL, password VARCHAR(20) NOT NULL);""")

cursor.execute("""INSERT INTO user(username, firstname, surname, password) VALUES("text_User","Bill", "Smith", 
"password")""")
db.commit()


def newUser():
    found = 0
    while found == 0:
        username = input("please enter a username")
        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            finduser = ("SELECT * FROM user WHERE username = ?")
            cursor.execute(finduser, [(username)])
        if cursor.fetchall():
            print("that username is already in use")
        else:
            found = 1

newUser()

cursor.execute("SELECT * FROM user;")
print(cursor.fetchall())
