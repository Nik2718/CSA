#******************************************************************************
import socket
import threading
import book

MESSAGE_LENGTH = 64
PORT = 5050
SERVER_IP = "127.0.0.1"
SERVER_ADDR = (SERVER_IP, PORT)
FORMAT = "utf-8"
MAXIMUM_NUMBER_OF_CLIENTS = 10

def start(server, phone_book):
    server.listen(MAXIMUM_NUMBER_OF_CLIENTS)
    print(f"Server is listening....")
    lock = threading.Lock()
    while True:
        client, client_addr = server.accept()
        thread = threading.Thread(target=handle_client,
                                  args=(client, client_addr, phone_book, lock))
        thread.start()
        print(f"Active connections {threading.active_count() - 1}")

def handle_client(client, client_addr, phone_book, lock):
    print(f"Client {client_addr} connected.")
    is_connected = True
    while is_connected:
        message = get_message(client)
        if message == "QUIT":
            is_connected = False
        elif message == "ADD":
            add(client, phone_book, lock)
        elif message == "SEARCH":
            search(client, phone_book, lock)
        elif message == "SEARCH_NOTE":
            search_note(client, phone_book, lock)
        elif message == "DELETE":
            delete(client, phone_book, lock)
        else:
            pass
    client.close()

def get_message(client):
    length = client.recv(MESSAGE_LENGTH).decode(FORMAT)
    if length:
        length = int(length)
        message = client.recv(length).decode(FORMAT)
        #client.send("Message received".encode(FORMAT))
        return message
    return ""

def send_message(client, message):
    message = str(message)
    message = message.encode(FORMAT)
    message_length = len(message)
    sent_length = str(message_length).encode(FORMAT)
    sent_length += b' ' * (MESSAGE_LENGTH - len(sent_length))
    client.send(sent_length)
    client.send(message)

def send_list(client, l, answer):
    send_message(client, answer)
    list_length = len(l)
    send_message(client, list_length)
    for element in l:
        send_message(client, element)

#return a tuple of an Entry object and a boolean variable
#True is in the case of success
def get_entry(client):
    message = get_message(client)
    l = message.split(";")
    if len(l) != 5:
        return (book.Entry("", "", "", "", ""), False)
    for i in range(0,5):
        l[i] = l[i].strip()
    return (book.Entry(l[0], l[1], l[2], l[3], l[4]), True)

def add(client, phone_book, lock):
    ent, is_correct = get_entry(client)
    if (ent.surname == "" and
        ent.name == "" and
        ent.patronymic == "" and
        ent.number == ""):
        send_message(client, "The empty entry will not be added")
        return
    if is_correct:
        if (ent.surname == "" and
        ent.name == "" and
        ent.patronymic == "" and
        ent.number == ""):
            send_message(client, "The empty entry will not be added")
            return

        lock.acquire()
        phone_book.add(ent)
        phone_book.save()
        lock.release()
        send_message(client, "An entry was added")
    else:
        send_message(client, "An incorrect query")

def search(client, phone_book, lock):
    ent, is_correct = get_entry(client)
    if is_correct:
        lock.acquire()
        l = phone_book.search(ent.surname,
                              ent.name,
                              ent.patronymic,
                              ent.number)
        lock.release()
        if l == []:
            send_list(client, l, "No data")
        else:
            send_list(client, l, "The result of the search query")
    else:
        send_list(client, [], "An incorrect query")

def search_note(client, phone_book, lock):
    text = get_message(client)
    if text == "":
        send_list(client, [], "Empty text")
        return
    lock.acquire()
    l = phone_book.search_note(text)
    lock.release()
    if l == []:
        send_list(client, l, "No data")
    else:
        send_list(client, l, "The result of the search in notes")

def delete(client, phone_book, lock):
    ent, is_correct = get_entry(client)
    if is_correct:
        lock.acquire()
        phone_book.delete(ent.surname, ent.name, ent.patronymic, ent.number)
        phone_book.save()
        lock.release()
        send_message(client, "All entries which meet the requirements were deleted")
    else:
        send_message(client, "An incorrect query")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDR)

phone_book = book.Book()
print("Server is starting...")
start(server, phone_book)