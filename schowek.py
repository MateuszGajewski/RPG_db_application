import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir= r"c:\Users\Admin\Desktop\sem5\instantclient_19_9")

def connection(user, password):
    dsn_tns = cx_Oracle.makedsn('admlab2.cs.put.poznan.pl', '1521', service_name='dblab02_students.cs.put.poznan.pl')
    conn = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)
    return conn




c = connection('inf141249', 'inf141249')
a = c.cursor()

a.execute("insert into jezyki values('elficki')")
a.execute('select * from jezyki')
for row in a:
    print (row[0])
#c.commit()
#c.close()








from databaseConnection import connection
from appJar import gui

def press(button):
    if button == "Cancel":
        app.stop()
    else:
        usr = app.getEntry("Username")
        pwd = app.getEntry("Password")
        a = connection(usr, pwd).cursor()
        a.execute('select * from jezyki')
        for row in a:
            print(row[0])

# create a GUI variable called app
app = gui("Login Window", "400x200")
app.setBg("orange")
app.setFont(18)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Logowanie do bazy RPG")
app.setLabelBg("title", "blue")
app.setLabelFg("title", "orange")

app.addLabelEntry("Username")
app.addLabelSecretEntry("Password")

# link the buttons to the function called press
app.addButtons(["Submit", "Cancel"], press)

app.setFocus("Username")

# start the GUI
app.go()





self.createdInt2 = 0;
            umiejLista = []
            umiejDBNaglowek = self.database.cursor().execute("select column_name from user_tab_cols where table_name = 'UMIEJETNOSCI'")
            query = ("select * from umiejetnosci u inner join umiejetnoscidlaklasy uk where uk.umiejetnosc = u.nazwa and uk.klasa = %s")
            umiejDB = self.database.cursor().execute(query, (klasa))
            tmp = []
            for row in umiejDBNaglowek:
                row = str(row).replace("('", "").replace("',)", "")
                tmp.append(row)
            umiejLista.append(tmp)
            for row in umiejDB:
                tmp = []
                self.lista_class.append(row[0])
                for item in row:
                    tmp.append(item)
                umiejDB.append(tmp)





for pole in range(15):
    app.addLabel(str(pole), "a", pole // 5, pole % 3)
for pole in range(15):
    if pole % 5 == 0:
        app.setLabelBg(str(pole), "LightYellow")
    if pole % 5 == 2:
        app.setLabelBg(str(pole), "LemonChiffon")
    if pole % 5 == 4:
        app.setLabelBg(str(pole), "LightGoldenRodYellow")