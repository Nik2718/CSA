import socket

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
    print("If a field can be arbitrary, leave it empty")
    print("Anyway there must be 4 semicolons")
    print("If a command was SEARCH or DELETE, 'note' field will be ignored")
    s = input("...")
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
    command = command.strip()
    if command == "ADD":
        add(client)
    elif command == "SEARCH":
        search(client)
    elif command == "DELETE":
        delete(client)
    elif command == "DISPLAY":
        display(client)
    elif command == "H":
        print("ADD - to add new entry")
        print("SEARCH - to search for all entries which meet the requirements")
        print("DELETE - to delete all entries which meet the requirements")
        print("QUIT - to disconnect with the server")
        print("H - to show a list of commands")
    elif command == "QUIT":
        send_message(client, "QUIT")
        print("Disconnection")
        proceed = False
    elif command == "":
        pass
    else:
        print("This command is unknown")