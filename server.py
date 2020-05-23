import socket
import sqlite3
import csv
import re
import random
import json


def clean_age(data):
    try:
        r = re.sub(r"\W", "", data)
        return int(r)
    except Exception as e:
        # print(e)
        return -1


def clean_other_data(data):
    try:
        # print(data)
        r = re.sub(' +', ' ', data)
        return r.strip()
    except Exception as e:
        # print(e)
        return ''


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


def insert_record(conn_insert, name, age, addr, phone):
    try:
        conn_insert.execute(
            "INSERT INTO USERS (NAME, AGE, ADDRESS, PHONE) VALUES ('{name}', {age}, '{addr}', '{phone}')".format(
                name=name, age=age, addr=addr, phone=phone))
        conn_insert.commit()
    except Exception as e:
        print(e)
        return None


def read_file_and_load_data(conn_for_insert):
    print("Loaded Data base from file")
    with open('data.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        for row in csv_reader:
            try:
                insert_record(conn_for_insert, clean_name(row[0], "NAME"), clean_age(row[1]), clean_other_data(row[2]),
                              clean_other_data(row[3]))
            except Exception as e:
                print("Skipping the Record As Invalid Input is provided >> " + '|'.join(row))
            # print(clean_age(row[1]))


def connect_data_base():
    print("Data base Connected")
    # conn = sqlite3.connect('UserMaster_{name}.db'.format(name = str(random.randrange(100, 199, 3))))
    conn = sqlite3.connect('UserMaster.db')
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


def find_user(name, conn):
    try:
        msg = ''
        result = conn.execute("SELECT NAME, AGE, ADDRESS, PHONE from USERS where NAME = '{name}'".format(name=name))
        print(result)
        for row in result:
            msg  = "\n*******************************************\n"
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
            return 'customer not found'
        else:
            return msg
    except Exception as e:
        print(e)
        return "customer not found"


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
                    c.send(bytes(user,'utf-8'))
                else:
                    print("Error Occured. Please try again")
            except Exception as e:
                print(e)
                c.send(bytes('Got Your Message', 'utf-8'))
            # c.send(bytes('Got Your Message', 'utf-8'))


if __name__ == '__main__':
    no_of_connections = 100
    conn = connect_data_base()
    # create_table(conn)
    # read_file_and_load_data(conn)
    start_socket_server(no_of_connections, conn)
