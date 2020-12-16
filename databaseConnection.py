import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir= r"c:\Users\Admin\Desktop\sem5\instantclient_19_9")

def connection(user, password):
    dsn_tns = cx_Oracle.makedsn('admlab2.cs.put.poznan.pl', '1521', service_name='dblab02_students.cs.put.poznan.pl')
    conn = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)
    return conn