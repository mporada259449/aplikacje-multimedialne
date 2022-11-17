import sqlite3

conn = sqlite3.connect("users.db")

c = conn.cursor()

#c.execute("""CREATE TABLE users (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    name TEXT,
 #  password TEXT
#)""")
#conn.commit()
#myusers = [('jan', 'pass'), ('xyzuser','strongpass'), ('user1', 'haslo'), ('app', '1234')]
#c.executemany("INSERT INTO users(name, password) VALUES(?,?)", myusers)
#conn.commit()
#c.execute("SELECT * FROM users")
#print(c.fetchall())
c.execute("""DROP TABLE configuration""")
c.execute("""
   CREATE TABLE configuration (
        name TEXT,
        isdevice INTEGER,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
""")
conn.commit()
conn.close()
