import sqlite3


class Hub:
    def __init__(self):
        self.userFile = "users.db"
        self.connUsers = sqlite3.connect(self.userFile)
        self.loggedUsers = []

    def login(self, password, login):
        pass

    def createAccount(self, login, password):
        pass

    def startDevice(self):
        pass

    def startApp(self):
        pass

    def addDevice(self):
        pass

    def addApp(self):
        pass

    def restartHub(self):
        pass
if __name__=="__main__":
    hub = Hub()
    c = hub.connUsers.cursor()

    c.execute("SELECT * FROM users")
    ans  = c.fetchall()
    hub.connUsers.commit()
    hub.connUsers.close()
    print(ans)
    #while True:
    #    pass
