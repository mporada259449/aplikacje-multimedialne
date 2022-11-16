import sqlite3


class Hub:
    def __init__(self):
        self.userFile = "users.db"
        self.connUsers = sqlite3.connect(self.userFile)
        self.c = self.connUsers.cursor()
        self.loggedUsers = []

    def login(self, password, login):
        self.c.execute("""
            SELECT password FROM users
            WHERE name==?
        """, (login,))
        ans = self.c.fetchall()
        self.connUsers.commit()
        if ans == []:
            return False
        elif password==ans[0][0]:
            self.loggedUsers.append(login)
            return True
        else:
            return False 
        
    def createAccount(self, login, password):
        self.c.execute("""
            SELECT name FROM users
            WHERE name==?
        """,(login,))
        ans = self.c.fetchall()
        self.connUsers.commit()
        if ans == []:
            self.c.execute("""
                INSERT INTO users(name, password) VALUES(?,?)
            """,(login, password))
            self.connUsers.commit()
            return True
        else:
            return False 

    def startDevice(self):
        pass

    def startApp(self):
        pass

    def stopDevice(self):
        pass
    
    def stopApp(self):
        pass

    def addDevice(self):
        pass

    def addApp(self):
        pass

    def restartHub(self):
        self.loggedUsers = []

    def powerOff(self):
        self.connUsers.close()

if __name__=="__main__":
    hub = Hub()
    print(hub.createAccount(login="login02", password="haslo1234"))
    print(hub.login(password="haslo1234", login="login02"))
    hub.powerOff()
    #while True:
    #    pass
