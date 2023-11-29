import socket
import threading
from datetime import datetime
from constants import HOST, PORT

username = input("Enter your username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.send(username.encode("utf-8"))

def write_messages():
    while True:
        message_content = input('')
        current_time = datetime.now().strftime("%H:%M:%S")
        message = f"{current_time} {username}: {message_content}"
        client.send(message.encode('utf-8'))

write_thread = threading.Thread(target=write_messages)
write_thread.start()
