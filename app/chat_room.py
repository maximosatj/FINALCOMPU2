import socket
import threading
from constants import HOST, PORT

username = 'chat_room'

#Check argpars coneection to server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                print(message)
        except:
            print("An error occurred")
            client.close()
            break


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()
