import sqlite3



class Hub:
    def __init__(self):
        self.userFile = "users.db"
        self.connUsers = sqlite3.connect(self.userFile)
        self.c = self.connUsers.cursor()
        self.loggedUsers = []
        self.usedDevices = []
        self.usedServices = []
        self.network = "siec"


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


    def createAccount(self, login, password, network):
        if self.network != network:
            return False
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
        #czy urządzenie nie jest używane
        if device in self.usedDevices:
            print("Device is used by another user")
            return False

        self.c.execute("""SELECT id FROM users WHERE name==?""",(login,))
        loginid = self.c.fetchone()
        #znalezienie konfiguracji
        self.c.execute("""SELECT * FROM configuration
                            WHERE name==? AND user_id==?
                        """,(device,int(loginid[0])))
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
    
                
    def startService(self, service, login):
        if login not in self.loggedUsers:
            #niezalogowany
            print("User is not logged")
            return False
        #zanlezienie id użytkownika
        self.c.execute("SELECT id FROM users WHERE name==?",(login,))
        userid = self.c.fetchone()
        #czy istnieje konfiguracja dla tego usera
        self.c.execute("""
            SELECT * FROM configuration
            WHERE name==? AND user_id==?
        """, (service, int(userid[0])))
        if len(self.c.fetchall())!=0:
            self.c.execute("""
                SELECT device FROM services
                WHERE name==?
            """, (service,))
            deviceList = [i[0] for i in self.c.fetchall()]
            for i in deviceList:
                if i[0] in self.usedDevices:
                    print("Device is used by another user")
                    self.connUsers.commit()
                    return False
            self.usedServices.append(service)
            for i in deviceList:
                self.usedDevices.append(i)
            print(f"{service} is tured on")
            self.connUsers.commit()
            return True
                
        else:
            print("It is not valid configuration for this user")
            self.connUsers.commit()
            return False
        

    def stopDevice(self, device, login):
        #jeśli nie jest uruchomione
        if login not in self.loggedUsers:
            print("user is not logged")
        if device not in self.usedDevices:
            print("Device is not turned on")
            return False
        
        self.c.execute("""SELECT id FROM users WHERE name==?""",(login,))
        loginid = self.c.fetchone()

        #znalezienie konfiguracji
        self.c.execute("""SELECT * FROM configuration
                            WHERE name==? AND user_id==?
                        """,(device,int(loginid[0])))
        #jeżeli konfiguracja nie istnieje
        if len(self.c.fetchall())==0:
            print("It is not valid configuration for this user")
            return False
        else:
            #jeżeli konfiguracja istnieje
            self.usedDevices.remove(device)
            print(f"{device} is turned off")
            self.connUsers.commit()
            return True
          
    
    def stopService(self, login, service):
        if login not in self.loggedUsers:
            print("User is not logged")
            return False
        if service not in self.usedServices:
            print("Service is not turned on")
            return False

        self.c.execute("""SELECT id FROM users WHERE name==?""",(login,))
        userid = self.c.fetchone()
        self.c.execute(
            """SELECT * FROM configuration
               WHERE name==? AND user_id==?
            """, (service, int(userid[0])))
        if len(self.c.fetchall()) != 0:
            self.c.execute("""
                SELECT device FROM services
                WHERE name==?
            """,(service,))
            deviceList = [i[0] for i in self.c.fetchall()] 
            for i in deviceList:
                try:
                    self.usedDevices.remove(i)
                except ValueError:
                    print(f"{i} has been already turned off")
            self.usedServices.remove(service)
            self.connUsers.commit()
            print(f"{service} is turned off")
            return True
        else:
            print("There is no such service in user configuration")
            self.connUsers.commit()
            return False

        
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
    currentuser= ""
    while True:
        print("""1. Log in
                 2. Create Account
                 3. Change current user
                 4. Add device to configuration
                 5. Add service to configuration
                 6. Turn on a device
                 7 .Turn on a service
                 8. Turn off a device
                 9. Turn off a service
                 10. Turn on the hub
                 11. Reset the hub
        """)
        ans = int(input("What do you want to do?: "))
        if ans==1:
            login = input("Login: ")
            password = input("Password: ")
            result = hub.login(password=password, login=login)
            if result:
                currentuser=login
                print("You are now logged")
            else:
                print("Can not sign up")
        elif ans==2:
            pass
        elif ans==3:
            pass
        elif ans==4:
            pass
        elif ans==5:
            pass
        elif ans==6:
            pass
        elif ans==7:
            pass
        elif ans==8:
            pass
        elif ans==9:
            pass
        elif ans==10:
            hub.powerOff()
        elif ans==11:
            hub.restartHub()

