import socket
import threading
from datetime import datetime
from constants import HOST, PORT 
from dataclasses import dataclass


@dataclass
class Server:
    clients = []
    usernames = []
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.server.bind((HOST, PORT))
        self.server.listen()
        print(f"Server running on {HOST}:{PORT}")

    def send_to_chat_room(self, message):
        self.clients[0].send(message)

    def handle_messages(self, client):
        while True:
            try:
                message = client.recv(1024)
                current_time = datetime.now().strftime("%H:%M:%S")
                formatted_message = f"{current_time} {message.decode('utf-8')}"
                self.send_to_chat_room(formatted_message.encode('utf-8'))
            except:
                index = self.clients.index(client)
                username = self.usernames[index]
                self.send_to_chat_room(f"ChatBot: {username} disconnected".encode('utf-8'))
                self.clients.remove(client)
                self.usernames.remove(username)
                client.close()
                break

    def receive_connections(self):
        while True:
            client, address = self.server.accept()

            print(client, address)

            client.send("@username".encode("utf-8"))
            username = client.recv(1024).decode('utf-8')

            self.clients.append(client)
            self.usernames.append(username)

            print(f"{username} is connected with {str(address)}")

            message = f"ChatBot: {username} joined the chat!".encode("utf-8")
            self.send_to_chat_room(message)
            client.send("Connected to server".encode("utf-8"))

            thread = threading.Thread(target=self.handle_messages, args=(client,))
            thread.start()



if __name__ == "__main__":
    server = Server()
    server.connect()
    server.receive_connections()
