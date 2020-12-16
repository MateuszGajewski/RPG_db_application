from databaseConnection import connection
from appJar import gui
from datetime import datetime

class window():

    def __init__(self):
        self.database = None
        self.lista = []
        self.createdInt = 1;

    def createDB(self):
        if self.database is not None and self.createdInt == 1:
            a = self.database.cursor().execute('select * from klasy')
            for row in a:
                self.lista.append(row)
            app.openTab("Start", "2")
            for obiekt in self.lista:
                app.label(obiekt)
            self.createdInt = 0;

    def login(self, btn):
        if btn == 'LOGIN':
            self.makeLogin()
            app.showSubWindow('Logowanie')
        else:
            app.stop()

    def confirm(self, button):
        if button == "Cancel":
            app.destroySubWindow("Logowanie")
        else:
            app.enableMenuItem("Open", "Log Out")
            app.disableMenuItem("Open", "Login")
            usr = app.getEntry("Username")
            pwd = app.getEntry("Password")
            self.database = connection(usr, pwd)
            app.destroySubWindow("Logowanie")

    def doNothing(self):
        pass

    def makeLogin(self):
        with app.subWindow('Logowanie', modal = True):
            app.showSubWindow("Logowanie")
            app.setSize(400,200)
            #app.setBgImage("okurwa.jpg")
            app.setBg("orange")
            #app.setFont(18)
            app.addLabel("title", "Logowanie do bazy RPG")
            app.setLabelBg("title", "blue")
            app.setLabelFg("title", "orange")
            app.addLabelEntry("Username")
            app.addLabelSecretEntry("Password")
            app.addButtons(["Login", "Cancel"], self.confirm)
            app.setFocus("Username")

    def makeLogOut(self):
        app.enableMenuItem("Open", "Login")
        app.disableMenuItem("Open", "Log Out")
        self.database = None
        self.lista = []
        self.createdInt = 1;
        app.infoBox("Wylogowywanie", "Nastąpiło poprawne wylogowanie z Bazy Danych", parent=None)

    def createTableOfClass(self):
        if self.database is not None and self.createdInt == 1:
            self.createdInt = 0;
            klasyLista = []
            klasyDBNaglowek = self.database.cursor().execute("select column_name from user_tab_cols where table_name = 'KLASY'")
            klasyDB = self.database.cursor().execute('select * from klasy')
            tmp = []
            for row in klasyDBNaglowek:
                row = str(row).replace("('", "").replace("',)", "")
                tmp.append(row)
            klasyLista.append(tmp)
            for row in klasyDB:
                tmp = []
                for item in row:
                    tmp.append(item)
                klasyLista.append(tmp)
            app.openTab("Start", "2")
            app.setSticky("new")
            app.setPadding([20, 20])
            app.addTable("tabela_klas", klasyLista, action=self.doNothing, addRow = None)
            app.stopTab()
        else:
            app.infoBox("Błąd", "Nie można wykonać operacji, ponieważ nie zalogowano się do Bazy Danych", parent=None)

if __name__ == "__main__" :

    win = window()
    with gui('Baza Danych RPG') as app:
        app.setSize(1280, 720)
        fileMenu = ["Login", "Log Out"]
        app.addMenuList("Open", fileMenu, [win.makeLogin, win.makeLogOut])
        app.disableMenuItem("Open", "Log Out")
        app.startTabbedFrame("Start")
        app.startTab("1")
        #app.registerEvent(win.createDB)
        #app.registerEvent(win.createTableOfClass)
        app.stopTab()
        app.startTab("2")
        app.setSticky("n")
        app.addButtons(["Show Classes"], win.createTableOfClass)
        #app.addLabel("loop", "New Row", app.getRow(), 0)
        #app.addButtons(["Show Classes"], win.createTableOfClass)
        app.stopTab()
        app.startTab("3")
        app.stopTab()
        app.stopTabbedFrame()

        #app.buttons(['LOGIN', 'EXIT'], win.login)
        #app.registerEvent(win.createDB)
        #app.setTabbedFrameSelectedTab("Start", "2")