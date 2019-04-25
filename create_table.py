import sqlite3

con = sqlite3.connect('database.db')
curs = con.cursor()

user = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username varchar(50),password varchar(100))"
item = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name varchar(25), price real)"

curs.execute(user)
curs.execute(item)

con.commit()
con.close()