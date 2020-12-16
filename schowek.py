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