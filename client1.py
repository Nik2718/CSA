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


def add(client, input_string):
    send_message(client, "ADD")
    send_message(client, input_string)
    print(get_message(client))

def search(client, input_string):
    send_message(client, "SEARCH")
    send_message(client, input_string)
    l, answer = get_list(client)
    print(answer)
    for ent in l:
        print(ent)

def delete(client, input_string):
    send_message(client, "DELETE")
    send_message(client, input_string)
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

do_proceed = True
while do_proceed:
    input_string = input(">")

    #Divide a command from data
    input_string = input_string.strip()
    command = input_string.split(' ')[0]
    command = command.split('\t')[0]
    input_string = input_string[len(command):len(input_string)]
    input_string = input_string.strip()

    if command == "ADD":
        add(client, input_string)
    elif command == "SEARCH":
        search(client, input_string)
    elif command == "DELETE":
        delete(client, input_string)
    elif command == "DISPLAY":
        display(client)
    elif command == "H":
        print("------------------------------")
        print("ADD - to add new entry")
        print("\tADD name; surname, patronymic; number; note")
        print("\tIf a field is unknown, leave it empty")
        print("\tAnyway there must be 4 semicolons")
        print("------------------------------")
        print("SEARCH - to search for all entries which meet the requirements")
        print("\tSEARCH name; surname, patronymic; number; ignored")
        print("\tIf a field can be arbitrary, leave it empty")
        print("\tAnyway there must be 4 semicolons")
        print("\tData after the 4-th semicolon will be ignored")
        print("------------------------------")
        print("DELETE - to delete all entries which meet the requirements")
        print("\tDELETE name; surname, patronymic; number; ignored")
        print("\tIf a field can be arbitrary, leave it empty")
        print("\tAnyway there must be 4 semicolons")
        print("\tData after the 4-th semicolon will be ignored")
        print("------------------------------")
        print("DISPLAY - to show the entire phone book")
        print("------------------------------")
        print("QUIT - to disconnect with the server")
        print("------------------------------")
        print("H - to show a list of commands")
        print("------------------------------")
    elif command == "QUIT":
        send_message(client, "QUIT")
        print("Disconnection")
        do_proceed = False
    elif command == "":
        pass
    else:
        print("This command is unknown")