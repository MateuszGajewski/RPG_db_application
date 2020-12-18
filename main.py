from databaseConnection import connection
from appJar import gui
from PIL import Image, ImageTk
import datetime

class window():

    def __init__(self):
        self.database = None
        self.lista = []
        self.createdInt = 1
        self.tabOfAb = 1
        self.lista_class = ["---------"]
        self.lista_sex = ["N", "F", "M"]
        self.lista_stat = []
        for i in range(21):
            self.lista_stat.append(i)
        self.lista_tab = ["Karty Postaci", "Klasy & Umiejętności", "Rasy & Pochodzenie", "Zarządzanie danymi"]
        for t in range(len(self.lista_tab)):
            tmp = ""
            n = len(max(self.lista_tab))-len(self.lista_tab[t])
            while(n > 0):
                tmp += " "
                n -= 1
            self.lista_tab[t] = self.lista_tab[t] + tmp


    def createDB(self):
        if self.database is not None and self.createdInt == 1:
            a = self.database.cursor().execute('select * from klasy')
            for row in a:
                self.lista.append(row)
            app.openTab("Start", self.lista_tab[1])
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
            pwd = app.getEntry("Password ")
            self.database = connection(usr, pwd)
            app.destroySubWindow("Logowanie")

    def sendCharacter(self):
        nazwa = app.getEntry("Nazwa Postaci")
        levela = app.getOptionBox("Level Postaci")
        plec  = app.getOptionBox("Płeć")
        rasa  = app.getEntry("Rasa")
        pochodzenia = app.getEntry("Pochodzenie")
        klasa  = app.getOptionBox("Klasa")
        wiek  = app.getEntry("Wiek")
        wzrost = app.getEntry("Wzrost")
        waga = app.getEntry("Waga")
        skora = app.getEntry("Kolor skóry")
        wlosy = app.getEntry("Kolor włosów")
        oczy = app.getEntry("Kolor oczów")
        hp = app.getEntry("HP")
        sta = app.getEntry("STA")
        strg = app.getOptionBox("STR")
        dex = app.getOptionBox("DEX")
        con = app.getOptionBox("CON")
        inte = app.getOptionBox("INT")
        wis = app.getOptionBox("WIS")
        cha = app.getOptionBox("CHA")
        self.database.cursor().execute(f"insert into Postacie values (POSTACIE_SEQ.NEXTVAL,'{nazwa}', {levela}, {wiek}, {wzrost}, {waga}, '{plec}', '{skora}',"
                                       f"'{wlosy}', '{oczy}', {hp}, {sta}, {strg}, {dex}, {con}, {inte}, {wis}, {cha}, '{rasa}', '{pochodzenia}', '{klasa}')")
        self.database.cursor().execute("commit")
        app.infoBox("Nowa Postać", "Nastąpiło poprawne dodanie postaci do bazy danych", parent=None)

    def doNothing(self):
        pass

    def makeLogin(self):
        with app.subWindow('Logowanie', modal = True):
            app.setResizable(canResize=False)
            app.showSubWindow("Logowanie")
            app.setBg("indianred")
            #duma = app.addImage("dragon", "login.gif")
            #app.setBgImage(duma)
            #photo = ImageTk.PhotoImage(Image.open("login.gif"))
            app.setSize(400,200)
            app.setSticky("new")
            app.addImage("smog", "goraLogin.gif")

            app.setPadding([20,5])
            app.addLabelEntry("Username")
            app.addLabelSecretEntry("Password ")

            app.addButtons(["Login ", "Cancel"], self.confirm)
            app.setFocus("Username")

            app.setPadding([0, 0])
            app.setSticky("sew")
            app.addImage("smog2", "dolLogin.gif")

    def makeLogOut(self):
        app.enableMenuItem("Open", "Login")
        app.disableMenuItem("Open", "Log Out")
        self.database = None
        self.lista = []
        self.createdInt = 1
        self.lista_class = ["---------"]
        app.openTab("Start", self.lista_tab[1])
        app.changeOptionBox("Wybierz klasę", self.lista_class, 0, 0)
        app.changeOptionBox("Klasa", self.lista_class, 0, 0)
        app.stopTab()
        app.infoBox("Wylogowywanie", "Nastąpiło poprawne wylogowanie z Bazy Danych", parent=None)

    def createTableOfClass(self):
        if self.database is not None and self.createdInt == 1:
            self.lista_class = []
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
            app.openTab("Start", self.lista_tab[0])
            app.changeOptionBox("Klasa", self.lista_class, 1, 0)
            app.stopTab()
            app.openTab("Start", self.lista_tab[1])
            app.changeOptionBox("Wybierz klasę", self.lista_class , 1 , 0)
            app.setStretch("both")
            app.setSticky("news")
            app.setPadding([20, 20])
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
        app.setSize(1280, 880)
        fileMenu = ["Login", "Log Out"]
        app.addMenuList("Open", fileMenu, [win.makeLogin, win.makeLogOut])
        app.disableMenuItem("Open", "Log Out")

        app.startTabbedFrame("Start")

        app.startTab(win.lista_tab[0])
        app.setStretch("column")
        app.setSticky("new")
        app.addImage("tlo1", "dnd2.gif", 0, colspan=4)

        app.setPadding([20, 0])
        app.setStretch("column")
        app.setSticky("w")
        app.addLabel("KartaPos", "Karta Postaci", 1, 0)
        app.addButtons(["Zatwierdź postać"], win.sendCharacter, 1, 1)

        app.setSticky("w")
        app.addLabelEntry("Nazwa Postaci", 2, 0)
        app.addLabelOptionBox("Level Postaci", win.lista_stat, 2, 1)
        app.addLabelOptionBox("Płeć", win.lista_sex, 2, 2)

        app.addLabelEntry("Rasa", 3, 0)
        app.addLabelEntry("Pochodzenie", 3, 1)
        app.addLabelOptionBox("Klasa", win.lista_class, 3, 2)

        app.addLabelEntry("Wiek", 4, 0)
        app.addLabelEntry("Wzrost", 4, 1)
        app.addLabelEntry("Waga", 4, 2)

        app.addLabelEntry("Kolor skóry", 5, 0)
        app.addLabelEntry("Kolor włosów", 5, 1)
        app.addLabelEntry("Kolor oczów", 5, 2)

        app.setSticky("e")
        app.addLabelEntry("HP", 6, 0)
        app.setSticky("w")
        app.addLabelEntry("STA", 6, 1)
        app.setSticky("w")
        #app.addLabelEntry("Plik z avatarem", 7, 1, colspan=2)

        app.setSticky("w")
        app.addLabelOptionBox("STR", win.lista_stat, 7, 0)
        app.addLabelOptionBox("DEX", win.lista_stat, 8, 0)
        app.addLabelOptionBox("CON", win.lista_stat, 9, 0)
        app.addLabelOptionBox("INT", win.lista_stat, 10, 0)
        app.addLabelOptionBox("WIS", win.lista_stat, 11, 0)
        app.addLabelOptionBox("CHA", win.lista_stat, 12, 0)

        app.setPadding([0,0])
        app.setSticky("nwes")
        app.addImage("krol", "krol.gif", 1, 3, rowspan=50)
        #app.addImage("avatar", "avatar.gif", 8, 1)

        #app.setImageSize("avatar", width=300, height=300)
        #app.setImage("avatar", "avatar.gif")

        app.setBg(colour="beige", override=False)
        app.stopTab()


        app.startTab(win.lista_tab[1])
        app.setStretch("column")
        app.setSticky("new")
        app.addImage("tlo2", "dnd2.gif", 0, colspan=2)

        app.setStretch('column')
        app.setSticky('wen')
        app.addLabel('bottom3', '', 1, colspan=2)
        app.setLabelBg("bottom3", "darkred")


        app.setStretch('column')
        app.setSticky('wen')
        app.setPadding([20, 4])

        app.addLabelOptionBox("Wybierz klasę", win.lista_class , 2 , 0)
        app.addButtons(["Wyświetl umiejętności klasy"], win.createTableOfAbilities, 2, 1)

        app.registerEvent(win.createTableOfClass)
        #app.addLabel("loop", "New Row", app.getRow(), 0)
        #app.addButtons(["Show Classes"], win.createTableOfClass)
        app.stopTab()


        app.startTab(win.lista_tab[2])
        app.setStretch("column")
        app.setSticky("new")
        app.addImage("tlo3", "dnd2.gif")
        app.stopTab()


        app.startTab(win.lista_tab[3])
        app.setStretch("column")
        app.setSticky("new")
        app.addImage("tlo4", "dnd2.gif")

        app.setStretch('column')
        app.setSticky('wen')
        app.addLabel('bottom2', '', 1, colspan=2)
        app.setLabelBg("bottom2", "darkred")

        app.setStretch('column')
        app.setSticky('wen')
        app.addLabel('postac', '', 2, 0)
        app.setLabelBg("postac", "indianred")
        app.addLabel('postaca', '', 2, 1)
        app.setLabelBg("postaca", "indianred")
        app.addLabel('postacb', '', 2, 2)
        app.setLabelBg("postacb", "indianred")

        app.addLabel("")


        app.stopTab()
        app.stopTabbedFrame()


        app.setTabbedFrameBg("Start", "darkred")
        #app.setTabBg(title = "Start", tab = win.lista_tab[0], colour="darkred")
        #app.buttons(['LOGIN', 'EXIT'], win.login)
        #app.registerEvent(win.createDB)
        #app.setTabbedFrameSelectedTab("Start", "2")