#******************************************************************************
import socket
import threading
import book

MESSAGE_LENGTH = 64
PORT = 5050
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_ADDR = (SERVER_IP, PORT)
FORMAT = "utf-8"
MAXIMUM_NUMBER_OF_CLIENTS = 10

вщс
get_entry(client)




def handle_client(client, client_addr, phone_book, lock):
    print(f"Client {client_addr} connected.")
    is_connected = True
    while is_connected:
        message = get_from_client(client)
        if message == "QUIT":
            is_connected = False
        if message == "ADD":
            ent, is_correct = get_entry(client)
            if is_correct:
                lock.acquire()
                phone_book.add(ent)
                phone_book.save()
                lock.release()
        if message == "SEARCH":
            ent, is_correct = get_entry(client)
            if is_correct:
                l = phone_book.select(ent.name, 
                                      ent.surname,
                                      ent.patronymic,
                                      ent.number)
                #send to client
                #...
        if message == "DELETE":
            ent, is_correct = get_entry(client)
            if is_correct:
                lock.acquire()
                phone_book.delete(ent)
                phone_book.save()
                lock.release()
    client.close()

def get_from_client(client):
    length = client.recv(MESSAGE_LENGTH).decode(FORMAT)
    if length:
        length = int(length)
        message = client.recv(length).decode(FORMAT)
        #client.send("Message received".encode(FORMAT))
        return message

def send_to_client(client, message):
    pass



def get_entry(server, client, adr):
    return (book.Entry(1,2,3,4,5), True)


def start(server, phone_book):
    server.listen(MAXIMUM_NUMBER_OF_CLIENTS)
    print(f"Server is listening on {SERVER_IP}")
    lock = threading.Lock()
    while True:
        client, client_addr = server.accept()
        thread = threading.Thread(target=handle_client, 
                                  args=(client, client_addr, phone_book, lock))
        thread.start()
        print(f"Active connections {threading.active_count() - 1}")



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDR)

phone_book = book.Book()
print("Server is starting...")
start(server, phone_book)