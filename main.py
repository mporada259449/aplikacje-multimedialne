import sqlite3


class Hub:
    def __init__(self):
        self.userFile = "users.db"
        self.connUsers = sqlite3.connect(self.userFile)
        self.c = self.connUsers.cursor()
        self.loggedUsers = []
        self.usedDevices = []

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

    def startDevice(self, device, login):
        self.c.execute("""SELECT id FROM users WHERE name==?""",(login,))
        loginid = self.c.fetchall()
        self.c.execute("""SELECT * FROM configuration
                            WHERE name==? AND user_id==?
        """,(device,loginid[0][0]))

    def startApp(self):
        pass

    def stopDevice(self):
        pass
    
    def stopApp(self):
        pass

    def addConf(self, username, conf, isDevice):
        #jeżeli jest zalogowany
        if username in self.loggedUsers:
            #znajdź id
            self.c.execute("""
                SELECT id FROM users
                WHERE name==?
            """,(username,))
            userid = self.c.fetchone()
            #znajdz czy istnieje konfiguracja
            self.c.execute("""
                SELECT * FROM configuration
                WHERE name==? AND user_id==?
            """,(conf, userid[0]))
            #jeżeli nie istnieje to dodaj
            if self.c.fetchall() == []:
                self.c.execute("INSERT INTO configuration VALUES(?,?,?)", (conf, isDevice, userid[0]))
                self.connUsers.commit()
                return True
            else:
                #jeśli konfiguracja jest już zapisana
                print("Configuration has been already added")
                return False
        else:
            #jeśli nie jesteś zalogowany
            print("You are not logged.")
            return False


    #def addApp(self, username, service):
    #    #jeżeli jest zalogowany
    #    if username in self.loggedUsers:
    #        #znajdź id
    #        self.c.execute("""
    #            SELECT id FROM users
    #            WHERE name==?
    #        """,(username,))
    #        userid = self.c.fetchone()
    #        #znajdz czy istnieje konfiguracja
    #        self.c.execute("""
    #            SELECT * FROM configuration
    #            WHERE name==? AND user_id==?
    #        """,(service, userid[0]))
    #        #jeżeli nie istnieje to dodaj
    #        if self.c.fetchall() == []:
    #            self.c.execute("INSERT INTO configuration VALUES(?,?,?)", (service, 0, userid[0]))
    #            self.connUsers.commit()
    #            return True
    #        else:
    #            #jeśli konfiguracja jest już zapisana
    #            print("Service has been already added to configuration")
    #            return False
    #    else:
    #        #jeśli nie jesteś zalogowany
    #        print("You are not logged.")
    #        return False

    def restartHub(self):
        self.loggedUsers = []

    def powerOff(self):
        self.connUsers.close()

if __name__=="__main__":
    hub = Hub()
    hub.loggedUsers.append("jan")
    print(hub.addConf(username="jan", conf="Netflix", isDevice=False))
    hub.c.execute("SELECT * FROM configuration")
    print(hub.c.fetchall())
    hub.powerOff()
    #while True:
    #    pass
