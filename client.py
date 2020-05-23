import socket

s = socket.socket()
port = 9999
s.connect(('127.0.0.1', port))
message = s.recv(1024).decode()
print(message)


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
    print(type(val))
    if val == '8':
        program_status = False
    s.send(bytes(val, 'utf-8'))
    # s.send(bytes('Message to Server', 'utf-8'))
    print(s.recv(1024).decode())