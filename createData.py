import sqlite3

conn = sqlite3.connect("users.db")

c = conn.cursor()

#c.execute("""CREATE TABLE users (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    name TEXT,
#    password TEXT
#)""")
#conn.commit()
#myusers = [('jan', 'pass'), ('xyzuser','strongpass'), ('user1', 'haslo'), ('app', '1234')]
#c.executemany("INSERT INTO users(name, password) VALUES(?,?)", myusers)
#conn.commit()
c.execute("SELECT * FROM users")
print(c.fetchall())
conn.commit()
conn.close()
