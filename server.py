import socket
import sqlite3
import csv
import re
import random
import json
import pprint

USER_NOT_FOUND = 'customer not found'


def clean_age(data):
    try:
        r = re.sub(r"\W", "", data)
        return int(r)
    except Exception as e:
        # print(e)
        return -1


def clean_age_error(data):
    try:
        r = re.sub(r"\W", "", data)
        return int(r)
    except Exception as e:
        raise Exception(e)


def clean_other_data(data):
    try:
        # print(data)
        r = re.sub(' +', ' ', data)
        return r.strip()
    except Exception as e:
        # print(e)
        return ''


def clean_other_data_eror(data):
    try:
        # print(data)
        r = re.sub(' +', ' ', data)
        return r.strip()
    except Exception as e:
        raise Exception(e)


def clean_name(data, col_type='NONE'):
    try:
        # print(data)
        r = re.sub(r"[\n\t]*", '', data).strip()
        # print(r)
        r = re.sub(r"\s\s+", " ", r)
        if col_type == "NAME" and r == '':
            raise Exception("Empty Name")
        elif r == '':
            return None
        else:
            return r
    except Exception as e:
        # print(e)
        raise Exception(e)


def insert_record_clean(conn_insert, name, age, addr, phone):
    try:
        name = clean_name((name))
        age = clean_age(age)
        addr = clean_other_data(addr)
        phone = clean_other_data(phone)
        conn_insert.execute(
            "INSERT INTO USERS (NAME, AGE, ADDRESS, PHONE) VALUES ('{name}', {age}, '{addr}', '{phone}')".format(
                name=name, age=age, addr=addr, phone=phone))
        conn_insert.commit()
    except Exception as e:
        print(e)
        raise Exception(e)


def insert_record(conn_insert, name, age, addr, phone):
    try:
        conn_insert.execute(
            "INSERT INTO USERS (NAME, AGE, ADDRESS, PHONE) VALUES ('{name}', {age}, '{addr}', '{phone}')".format(
                name=name, age=age, addr=addr, phone=phone))
        conn_insert.commit()
    except Exception as e:
        print(e)
        return None


def delete_user(name, conn_delete):
    try:
        conn_delete.execute("DELETE FROM USERS WHERE NAME = '{name}'".format(name=name))
        return None
    except Exception as e:
        raise Exception(e)


def update_details(name, detail, detail_type, conn_update):
    try:
        if detail_type == 'age':
            detail = clean_age_error(detail)
            query = "UPDATE USERS SET {detail_type} = {detail} where name = '{name}'"
        else:
            detail = clean_other_data_eror(detail)
            query = "UPDATE USERS SET {detail_type} = '{detail}' where name = '{name}'"
        conn_update.execute(query.format(detail_type=detail_type, name=name, detail=detail))
        conn_update.commit()
        result = conn_update.total_changes
        print("No of updated Rows >> " + str(result))
        if result == 1:
            return 'Updated Details Successfully'
        else:
            return "Failed to Update. Either No User Found or Details are in invalid fromat"
    except Exception as e:
        raise Exception(e)
    
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def get_report(report_conn):
    try:
        cursor = report_conn.execute("SELECT NAME, CASE when AGE < 0 THEN NULL ELSE AGE END AS AGE, ADDRESS, "
                                     "PHONE from USERS ORDER BY NAME ASC")
        data = cursor.fetchall()
        print(data)
        msg =     "\n--------------------------------------------------------------------------------------------------------------------------------\n"
        msg = msg + "┆***************************************************     "+ color.BOLD + color.UNDERLINE + color.BLUE + "REPORT" + color.END + color.END + color.END +"     ************************************************************┆"
        msg = msg + "\n--------------------------------------------------------------------------------------------------------------------------------\n"
        msg = msg + "┆ "+ color.RED + color.BOLD +"Name" + color.END + color.END + "\t\t\t\t┆ "+ color.RED + color.BOLD +"Age"+ color.END + color.END\
              + "\t\t┆ "+ color.RED + color.BOLD + "Address" + color.END + color.END +  "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t┆ "+ color.RED + color.BOLD + "Phone" + color.END + color.END + "\t\t\t\t\t┆\n"
        msg = msg + "--------------------------------------------------------------------------------------------------------------------------------\n"
        for row in data:
            msg = msg + "┆ " +  row[0] + " "*(18-len(row[0])) + "┆ " + str(row[1]) + " "*(10-len(str(row[1]))) + "┆ " + row[2] + " "*(70 - len(row[2])) + "┆ " + row[3] + " "*(22-len(row[3])) + "┆\n"
        msg = msg + "--------------------------------------------------------------------------------------------------------------------------------\n"
        print(msg)
        return msg
    except Exception as e:
        raise Exception(e)


def read_file_and_load_data(conn_for_insert):
    print("Loaded Data base from file")
    with open('data.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        for row in csv_reader:
            try:
                insert_record(conn_for_insert, clean_name(row[0], "NAME"), clean_age(row[1]), clean_other_data(row[2]),
                              clean_other_data(row[3]))
            except Exception as e:
                print("Skipping the Record As Invalid Input is provided >> " + ':'.join(row))
            # print(clean_age(row[1]))


def connect_data_base():
    print("Data base Connected")
    conn = sqlite3.connect('UserMaster_{name}.db'.format(name = str(random.randrange(100, 199, 3))))
    # conn = sqlite3.connect('UserMaster.db')
    return conn


def create_table(conn_for_tbl):
    print("Creating DB Tables")
    try:
        result = conn_for_tbl.execute('''CREATE TABLE USERS
         (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
         NAME           TEXT    NOT NULL,
         AGE            INT     NULL,
         ADDRESS        TEXT NULL,
         PHONE VARCHAR(256) NULL);''')
        print(result)
    except Exception as e:
        print(e)


def load_data():
    print("Loaded Data")


def find_user(name, conn_user_find):
    try:
        msg = ''
        result = conn_user_find.execute("SELECT NAME, AGE, ADDRESS, PHONE from USERS where NAME = '{name}'".format(name=name))
        print(result)
        for row in result:
            msg = "\n*******************************************\n"
            msg = msg + "Customer Details Found\n"
            msg = msg + "*******************************************\n"
            msg = msg + "Name >> " + row[0] + "\n"
            if row[1] < 0:
                msg = msg + "Age >> Not Available\n"
            else:
                msg = msg + "Age >> " + str(row[1]) + "\n"
            msg = msg + "Address >> " + row[2] + "\n"
            msg = msg + "Phone >> " + row[3] + "\n"
            msg = msg + "*******************************************\n"
        
        if msg == '':
            return USER_NOT_FOUND
        else:
            return msg
    except Exception as e:
        print(e)
        return USER_NOT_FOUND


def start_socket_server(connections, conn):
    s = socket.socket()
    print("Socket Created")
    port = 9999
    s.bind(('', port))
    print("Socket Binding on Port %s" % (port))
    s.listen(connections)
    print("Socket is listening")
    while True:
        c, addr = s.accept()
        print(c)
        print(addr)
        msg = get_report(conn)
        c.send(bytes(msg, 'utf-8'))
        # c.send(bytes('Thank you for connecting', 'utf-8'))
        while c:
            try:
                msg = c.recv(1024).decode()
                msg = json.loads(msg)
                print(msg)
                if msg['val'] == '1':
                    print(type(msg))
                    print(msg['data'])
                    # c.send(bytes('Searching ...', 'utf-8'))
                    user = find_user(msg['data'], conn)
                    c.send(bytes(user, 'utf-8'))
                elif msg['val'] == '2':
                    user = find_user(msg['name'], conn)
                    if user == USER_NOT_FOUND:
                        insert_record_clean(conn, msg['name'], msg['age'], msg['address'], msg['phone'])
                        c.send(bytes('\nAdded User Successfully\n', 'utf-8'))
                    else:
                        c.send(bytes('\nUser Already Exists\n', 'utf-8'))
                elif msg['val'] == '3':
                    user = find_user(msg['name'], conn)
                    if user == USER_NOT_FOUND:
                        c.send(bytes(USER_NOT_FOUND, 'utf-8'))
                    else:
                        delete_user(msg['name'], conn)
                        c.send(bytes('\nDeleted User Successfully\n', 'utf-8'))
                elif msg['val'] == '4':
                    result = update_details(msg['name'], msg['age'], 'age', conn)
                    c.send(bytes(result, 'utf-8'))
                elif msg['val'] == '5':
                    result = update_details(msg['name'], msg['address'], 'address', conn)
                    c.send(bytes(result, 'utf-8'))
                elif msg['val'] == '6':
                    result = update_details(msg['name'], msg['phone'], 'phone', conn)
                    c.send(bytes(result, 'utf-8'))
                elif msg['val'] == '7':
                    msg = get_report(conn)
                    c.send(bytes(msg, 'utf-8'))
                elif msg['val'] == '8':
                    c.close()
                else:
                    print("Error Occurred. Please try again")
            except Exception as e:
                print(e)
                try:
                    c.send(bytes('Something Went Wrong. Try Again with Proper Fields', 'utf-8'))
                except Exception as e:
                    s.close()
                    start_socket_server(1, conn)
            # c.send(bytes('Got Your Message', 'utf-8'))


if __name__ == '__main__':
    no_of_connections = 1
    conn = connect_data_base()
    create_table(conn)
    read_file_and_load_data(conn)
    start_socket_server(no_of_connections, conn)
