from databaseConnection import connection
from appJar import gui

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
            usr = app.getEntry("Username")
            pwd = app.getEntry("Password")
            self.database = connection(usr, pwd)
            app.destroySubWindow("Logowanie")

    def makeLogin(self):
        app.disableMenuItem("Open", "Login")
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
            app.addButtons(["Submit", "Cancel"], self.confirm)
            app.setFocus("Username")

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
            app.addTable("tabela_klas", klasyLista)
            app.stopTab()

if __name__ == "__main__" :

    win = window()
    with gui('Baza Danych RPG') as app:
        app.setSize(1280, 720)
        app.startTabbedFrame("Start")
        app.startTab("1")
        #app.registerEvent(win.createDB)
        app.registerEvent(win.createTableOfClass)
        app.stopTab()
        app.startTab("2")
        app.stopTab()
        app.startTab("3")
        app.stopTab()
        app.stopTabbedFrame()

        fileMenu = ["Login"]
        app.addMenuList("Open", fileMenu, [win.makeLogin])
        #app.buttons(['LOGIN', 'EXIT'], win.login)
        #app.registerEvent(win.createDB)
        #app.setTabbedFrameSelectedTab("Start", "2")