import socket


def read_file():
    print("Loaded Data base from files")


def connect_data_base():
    print("Data base Connected")


def load_data():
    print("Loaded Data")


def start_socket_server(no_of_connections):
    s = socket.socket()
    print("Socket Created")
    port = 9999
    s.bind(('', port))
    print("Socket Binding on Port %s" % (port))
    s.listen(no_of_connections)
    print("Socket is listening")
    while True:
        c, addr = s.accept()
        print(c)
        print(addr)
        c.send(bytes('Thank you for connecting', 'utf-8'))
        while c:
            print(c.recv(1024).decode())
            c.send(bytes('Got Your Message', 'utf-8'))


if __name__ == '__main__':
    no_of_connections = 100
    read_file()
    connect_data_base()
    load_data()
    start_socket_server(no_of_connections)
