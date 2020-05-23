import socket
import json

s = socket.socket()
port = 9999
s.connect(('127.0.0.1', port))
# message = s.recv(1024).decode()
# print(message)


def populate_menu():
    print("Menu")
    print("1. Find customer")
    print("2. Add customer")
    print("3. Delete customer")
    print("4. Update customer age")
    print("5. Update customer address")
    print("6. Update customer phone")
    print("7. Print report")
    print("8. Exit")


program_status = True

while program_status:
    populate_menu()
    val = input("Select : ")
    if val == '1':
        data = input("Enter Name of the User to Find >> ")
        s.send(bytes(json.dumps({ 'val' : val, 'data' : data}), 'utf-8'))
        print(s.recv(1024).decode())
    if val == '2':
        name = input("Enter Name of the User >> ")
        age = input("Enter Age of the User >> ")
        address = input("Enter Address of the User >> ")
        phone = input("Enter Phone of the User >> ")
        s.send(bytes(json.dumps({ 'val' : val, 'name' : name, 'age': age, 'address' : address, 'phone' : phone}), 'utf-8'))
        print(s.recv(1024).decode())
    # print(type(val))
    if val == '8':
        program_status = False
    # s.send(bytes(val, 'utf-8'))
    # # s.send(bytes('Message to Server', 'utf-8'))
    # print(s.recv(1024).decode())
