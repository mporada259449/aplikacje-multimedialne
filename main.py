import sqlite3


class Hub:
    def __init__(self):
        userFile = "users.db"
        confFile = "configurations.db"
        loggedUsers = []

    def login(self, password, login):
        pass

    def createAccount(self, login, password):
        pass

    def connectDatabase(self):
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
    hub.connectDatabase()
    #while True:
    #    pass
