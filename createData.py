import sqlite3
import hashlib
conn = sqlite3.connect("users.db")

def hashing(s):
    hash =  hashlib.sha256()
    sbytes = s.encode()
    hash.update(sbytes)
    return hash.hexdigest()
c = conn.cursor()
#stworzenie tabeli users i wpisanie przykładowych danych
c.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        password TEXT
    )
    """)
myusers = [('jan@gmail.com', hashing('pass')), ('xyzuser@gmail.com',hashing('strongpass')), ('user1@gmail.com', hashing('haslo')), ('app@gmail.com', hashing('1234'))]
c.executemany("INSERT INTO users(name, password) VALUES(?,?)", myusers)
conn.commit()


#stworzenie tabeli configuration i wpisanie przykładowych danch
c.execute("""
    CREATE TABLE configuration (
        name TEXT,
        isdevice INTEGER,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

myconf = [("telewizor", 1, 3), ("Netflix", 0, 3), ("JBL Speaker", 1, 1), ("Eurosport", 0, 4)]
c.executemany("INSERT INTO configuration VALUES(?,?,?)", myconf)
conn.commit()


#stworzenie tabeli service i wpisanie przykładowych danych
c.execute("""
    CREATE TABLE services (
        name TEXT,
        device TEXT
    )
    """)

myservices = [("Netflix", "telewizor"), ("Netflix", "soundbar"), ("Gra PS5", "telewizor"), ("Gra PS5", "soundbar"), ("Gra PS5", "Playstation 5"),
            ("Eurosport", "telewizor"), ("Eurosport", "soundbar"), ("Playlista", "JBL Speaker")]
c.executemany("INSERT INTO services VALUES(?,?)", myservices)

c.execute("""
    CREATE TABLE specialconf(
        name TEXT,
        device TEXT,
        user_id INTAGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
""")

conn.commit()
conn.close()