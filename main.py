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
        #czy user jest zalogowany
        if login not in self.loggedUsers:
            print("User is not logged")
            return False
        #czy użądzenie nie jest używane
        if device in self.usedDevices:
            print("Device is used by another user")
            return False

        self.c.execute("""SELECT id FROM users WHERE name==?""",(login,))
        loginid = self.c.fetchall()
        if len(loginid) != 0:
            #znalezienie konfiguracji
            self.c.execute("""SELECT * FROM configuration
                                WHERE name==? AND user_id==?
                            """,(device,loginid[0]))
            #jeżeli konfiguracja nie istnieje
            if len(self.c.fetchall())==0:
                print("It is not valid configuration for this user")
                return False
            else:
                #jeżeli konfiguracja istnieje
                self.usedDevices.append(device)
                print(f"{device} is turned on")
                self.connUsers.commit()
                return True
                


    def startService(self):
        pass

    def stopDevice(self):
        pass
    
    def stopService(self):
        pass

    def addDevice(self, username, device):
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
            """,(device, userid[0]))
            #jeżeli nie istnieje to dodaj
            if self.c.fetchall() == []:
                self.c.execute("INSERT INTO configuration VALUES(?,?,?)", (device, 1, userid[0]))
                self.connUsers.commit()
                return True
            else:
                #jeśli konfiguracja jest już zapisana
                print("Configuration has been already added")
                self.connUsers.commit()
                return False
        else:
            #jeśli nie jesteś zalogowany
            print("You are not logged.")
            self.connUsers.commit()
            return False

    def addService(self, username, service):
        #jeżeli jest zalogowany
        if username in self.loggedUsers:
            self.c.execute("""
                SELECT * FROM services
                WHERE name=?
            """,(service,))
            #jeżeli serwis nie istnieje 
            if len(self.c.fetchall()) == 0:
                print("Service doesn't exist")
                self.connUsers.commit()
                return False
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
            """,(service, userid[0]))
            #jeżeli nie istnieje to dodaj
            if self.c.fetchall() == []:
                self.c.execute("INSERT INTO configuration VALUES(?,?,?)", (service, 0, userid[0]))
                self.connUsers.commit()
                return True
            else:
                #jeśli konfiguracja jest już zapisana
                print("Service has been already added to configuration")
                self.connUsers.commit()
                return False
        else:
            #jeśli nie jesteś zalogowany
            print("You are not logged.")
            self.connUsers.commit()
            return False

    def restartHub(self):
        self.loggedUsers = []
        self.usedDevices = []

    def powerOff(self):
        self.connUsers.close()

if __name__=="__main__":
    hub = Hub()
    hub.loggedUsers.append("xyzuser")
    print(hub.addService(username="xyzuser", service="Netflix"))
    hub.c.execute("SELECT * FROM configuration")
    print(hub.c.fetchall())
    hub.powerOff()
    #while True:
    #    pass
