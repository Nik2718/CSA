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

def add(client, data_string):
    send_message(client, "ADD")
    send_message(client, data_string)
    print(get_message(client))

def search(client, data_string):
    send_message(client, "SEARCH")
    send_message(client, data_string)
    l, answer = get_list(client)
    print(answer)
    for ent in l:
        print(str(ent)+"\n")

def search_note(client, note):
    send_message(client, "SEARCH_NOTE")
    send_message(client, note)
    l, answer = get_list(client)
    print(answer)
    for ent in l:
        print(str(ent)+"\n")

def delete(client, data_string):
    send_message(client, "DELETE")
    send_message(client, data_string)
    print(get_message(client))

def display(client):
    send_message(client, "SEARCH")
    send_message(client, ";;;;")
    l, answer = get_list(client)
    print(answer)
    for ent in l:
        print(str(ent)+"\n")

def print_help():
    print("""\
    ------------------------------
    ADD - to add a new entry
    \tADD surname; name; patronymic; number; note
    \tIf a field is unknown, leave it empty
    \tAnyway there must be 4 semicolons
    ------------------------------
    SEARCH - to search for all entries which meet the requirements
    \tSEARCH surname; name; patronymic; number; ignored
    \tIf a field can be arbitrary, leave it empty
    \tAnyway there must be 4 semicolons
    \tData after the 4-th semicolon will be ignored
    ------------------------------
    SEARCH_NOTE - to search a piece of text in all notes of the phone book
    \tSEARCH_NOTE text
    ------------------------------
    DELETE - to delete all entries which meet the requirements
    \tDELETE surname; name; patronymic; number; ignored
    \tIf a field can be arbitrary, leave it empty
    \tAnyway there must be 4 semicolons
    \tData after the 4-th semicolon will be ignored
    ------------------------------
    DISPLAY - to show the entire phone book
    ------------------------------
    QUIT - to disconnect with the server
    ------------------------------
    H - to show a list of commands
    ------------------------------""")

def divide_input(input_string):
    input_string = input_string.strip()
    command = input_string.split(' ')[0]
    command = command.split('\t')[0]
    data_string = input_string[len(command):len(input_string)]
    data_string = data_string.strip()
    return (command, data_string)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(SERVER_ADDR)

print("Enter your request")
print("Type H to get a list of commands")

do_proceed = True
while do_proceed:
    input_string = input(">")
    command, data_string = divide_input(input_string)

    if command == "ADD":
        add(client, data_string)
    elif command == "SEARCH":
        search(client, data_string)
    elif command == "SEARCH_NOTE":
        search_note(client, data_string)
    elif command == "DELETE":
        delete(client, data_string)
    elif command == "DISPLAY":
        display(client)
    elif command == "H":
        print_help()
    elif command == "QUIT":
        send_message(client, "QUIT")
        print("Disconnection")
        do_proceed = False
    elif command == "":
        pass
    else:
        print("This command is unknown")