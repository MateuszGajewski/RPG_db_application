from databaseConnection import connection
from appJar import gui
import datetime

class window():

    def __init__(self):
        self.database = None
        self.lista = []
        self.createdInt = 1
        self.tabOfAb = 1
        self.lista_class = ["---------"]

    def createDB(self):
        if self.database is not None and self.createdInt == 1:
            a = self.database.cursor().execute('select * from klasy')
            for row in a:
                self.lista.append(row)
            app.openTab("Start", "Klasy & Skills")
            for obiekt in self.lista:
                app.label(obiekt)
            self.createdInt = 0


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
        self.createdInt = 1
        self.lista_class = ["---------"]
        app.openTab("Start", "Klasy & Skills")
        app.changeOptionBox("Wybierz klasę", self.lista_class, 0, 0)
        app.stopTab()
        app.infoBox("Wylogowywanie", "Nastąpiło poprawne wylogowanie z Bazy Danych", parent=None)

    def createTableOfClass(self):
        if self.database is not None and self.createdInt == 1:
            self.createdInt = 0
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
                self.lista_class.append(row[0])
                for item in row:
                    tmp.append(item)
                klasyLista.append(tmp)

            app.openTab("Start", "Klasy & Skills")
            app.changeOptionBox("Wybierz klasę", self.lista_class , 1 , 0)
            app.setStretch("both")
            app.setSticky("news")
            app.setPadding([20, 0])
            app.addTable("tabela_klas", klasyLista, wrap="700", colspan=3)
            app.stopTab()

    def createTableOfAbilities(self):
        if self.tabOfAb > 1:
            app.destroySubWindow("Umiejętność wybranej klasy")
        if self.database is not None:
            self.tabOfAb += 1;
            klasa = app.getOptionBox("Wybierz klasę")
            self.createdInt2 = 0;
            umiejLista = []
            umiejDBNaglowek = self.database.cursor().execute("select column_name from user_tab_cols where table_name = 'UMIEJETNOSCI'")
            query = (f"select nazwa, opis_umiejetnosci, poziom, dmg, heal, def, p_d, nazwa_dodatku from Umiejetnosci u inner join UmiejetnosciDlaKlas uk on uk.umiejetnosc = u.nazwa where uk.klasa = '{klasa}'")
            umiejDB = self.database.cursor().execute(query)
            tmp = []
            for row in umiejDBNaglowek:
                row = str(row).replace("('", "").replace("',)", "")
                tmp.append(row)
            umiejLista.append(tmp)
            for row in umiejDB:
                tmp = []
                self.lista_class.append(row[0])
                for item in row:
                    if item == None:
                        item = '-'
                    tmp.append(item)
                umiejLista.append(tmp)
            self.tabOfAb += 1
            with app.subWindow("Umiejętność wybranej klasy", modal=True):
                app.showSubWindow("Umiejętność wybranej klasy")
                app.setSize(1280, 720)
                app.setStretch("column")
                app.setSticky("ew")
                app.addImage(f"klasy{self.tabOfAb}", "dnd2.gif", colspan=3)
                app.setStretch("both")
                app.setSticky("news")
                app.setPadding([20, 20])
                app.addTable(f"tabela_umiejetnosci_dla_klas{self.tabOfAb}", umiejLista, wrap="500")

if __name__ == "__main__" :

    win = window()
    with gui('Baza Danych RPG') as app:
        app.setResizable(canResize=True)
        app.setSize(1280, 720)
        fileMenu = ["Login", "Log Out"]
        app.addMenuList("Open", fileMenu, [win.makeLogin, win.makeLogOut])
        app.disableMenuItem("Open", "Log Out")
        app.startTabbedFrame("Start")
        app.startTab("Character Card")
        app.setStretch("column")
        app.setSticky("ew")
        app.addImage("tlo1", "dnd2.gif")
        #app.registerEvent(win.createDB)
        #app.registerEvent(win.createTableOfClass)
        app.stopTab()
        app.startTab("Klasy & Skills")
        app.setStretch("column")
        app.setSticky("new")
        app.addImage("tlo2", "dnd2.gif", colspan=3)
        app.setStretch("column")
        app.setSticky("ew")
        app.setPadding([20, 20])
        app.addLabelOptionBox("Wybierz klasę", win.lista_class , 1 , 0)
        app.addButtons(["Wyświetl umiejętności klasy"], win.createTableOfAbilities, 1, 1)
        app.addLabel("p1", "", 1, 2)
        app.registerEvent(win.createTableOfClass)
        #app.addLabel("loop", "New Row", app.getRow(), 0)
        #app.addButtons(["Show Classes"], win.createTableOfClass)
        app.stopTab()
        app.startTab("Rasy & Pochodzenie")
        app.setStretch("column")
        app.setSticky("new")
        app.addImage("tlo3", "dnd2.gif")
        app.stopTab()
        app.startTab("Zarządzanie zasobami")
        app.setStretch("column")
        app.setSticky("new")
        app.addImage("tlo4", "dnd2.gif")
        app.stopTab()
        app.stopTabbedFrame()

        #app.buttons(['LOGIN', 'EXIT'], win.login)
        #app.registerEvent(win.createDB)
        #app.setTabbedFrameSelectedTab("Start", "2")