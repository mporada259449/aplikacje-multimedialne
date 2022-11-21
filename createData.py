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
#c.execute("""DROP TABLE configuration""")
#c.execute("""
#   CREATE TABLE configuration (
#        name TEXT,
#        isdevice INTEGER,
#        user_id INTEGER,
#        FOREIGN KEY(user_id) REFERENCES users(id)
#    )
#""")
#c.execute("""
#    CREATE TABLE services (
#        name TEXT,
#        device TEXT
#    )
#""")
#myservices = [("Netfilx", "telewizor"), ("Netfilx", "soundbar"), ("PS Network", "telewizor"), ("PS Network", "soundbar"), ("PS Network", "Playstation 5")]
#c.executemany("INSERT INTO services VALUES(?,?)", myservices)
c.execute("""UPDATE services
            SET name='Netflix'
            WHERE name='Netfilx'
""")
c.execute("SELECT * FROM services")
print(c.fetchall())
conn.commit()
conn.close()
