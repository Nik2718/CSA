import socket
import book

MESSAGE_LENGTH = 64
SERVER_PORT = 5050
FORMAT = 'utf-8'
SERVER_IP = "127.0.0.1"
SERVER_ADDR = (SERVER_IP, SERVER_PORT)

def send_message(client, message):
    message = str(message)
    message = message.encode(FORMAT)
    message_length = len(message)
    sent_length = str(message_length).encode(FORMAT)
    sent_length += b' ' * (MESSAGE_LENGTH - len(sent_length))
    client.send(sent_length)
    client.send(message)

def get_message(client):
    length = client.recv(MESSAGE_LENGTH).decode(FORMAT)
    if length:
        length = int(length)
        message = client.recv(length).decode(FORMAT)
    return message



def get_list(client):
    answer = get_message(client)
    list_length = int(get_message(client))
    l = []
    for i in range(0, list_length):
        l.append(get_message(client))
    return (l, answer)


def input_entry():
    print("Input name; surname; patronymic; number; note")
    print("A field can be empty, but each ';' is necessary")
    s = input(">")
    return s

def add(client):
    send_message(client, "ADD")
    s = input_entry()
    send_message(client, s)
    print(get_message(client))

def search(client):
    send_message(client, "SEARCH")
    s = input_entry()
    send_message(client, s)
    l, answer = get_list(client)
    print(answer)
    for ent in l:
        print(ent)

def delete(client):
    send_message(client, "DELETE")
    s = input_entry()
    send_message(client, s)
    print(get_message(client))

def display(client):
    send_message(client, "SEARCH")
    send_message(client, ";;;;")
    l, answer = get_list(client)
    print(answer)
    for ent in l:
        print(ent)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(SERVER_ADDR)

print("Enter your request")
print("Type H to get a list of commands")

proceed = True
while proceed:
    command = input(">")
    command = command.replace(" ", "")
    command = command.replace("\t", "")
    if command == "ADD":
        add(client)
    elif command == "SEARCH":
        search(client)
    elif command == "DELETE":
        delete(client)
    elif command == "DISPLAY":
        display(client)
    elif command == "H":
        print("ADD...")
        print("SEARCH...")
        print("DELETE...")
        print("QUIT...")
        print("H...")
    elif command == "QUIT":
        send_message(client, "QUIT")
        print("Disconnection")
        proceed = False
    elif command == "":
        pass
    else:
        print("This command is unknown")