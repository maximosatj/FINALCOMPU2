import socket
from datetime import datetime
import random
import os
import time
import threading
from client import Client

host = os.environ.get('HOST', '0.0.0.0')
port = int(os.environ.get('PORT', 5000))
max_clients = int(os.environ.get('MAX', 5))
                   
class Server:
    clients = []
    usernames = []
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.server.bind((host, port))
        self.server.listen(max_clients)
        print(f"Server running on {host}:{port}")

    def send_to_chat_room(self, message):
        for client in self.clients:
            if client.username == 'chat_room':
                latency = random.uniform(0.005, 1.5)
                time.sleep(latency)
                client.socket.send(message)

    def receive_connections(self):
        while True:
            # Si el socket listo es el socket del servidor, significa que hay una nueva conexión
            client, address = self.server.accept()

            client.send("@username".encode("utf-8"))
            username = client.recv(1024).decode('utf-8')

            new_client = Client(username, client, address)
            self.clients.append(new_client)
            self.usernames.append(username)

            print(f"{username} is connected with {str(address)}")
            message = f"ChatBot: {username} joined the chat!".encode("utf-8")
            self.send_to_chat_room(message)
            client.send("Connected to server".encode("utf-8"))

            thread = threading.Thread(target=self.handle_messages, args=(new_client,))
            thread.start()

    def handle_messages(self, client):
        while True:
            try:
                message = client.socket.recv(1024)
                if message == b'get_users':
                    users = self.users_connected()
                    formatted_message = 'USERS ONLINE: ' + ', '.join(users)
                    client.socket.send((formatted_message).encode('utf-8'))
                elif message:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    formatted_message = f"{current_time} {message.decode('utf-8')}"
                    self.send_to_chat_room(formatted_message.encode('utf-8'))
                else:
                    index = self.clients.index(client)
                    username = self.usernames[index]
                    self.send_to_chat_room(f"ChatBot: {username} disconnected".encode('utf-8'))
                    print(f"{username} disconnected.")
                    self.clients.remove(client)
                    self.usernames.remove(username)
                    client.socket.close()
                    break
            except:
                index = self.clients.index(client)
                username = self.usernames[index]
                self.send_to_chat_room(f"ChatBot: {username} disconnected".encode('utf-8'))
                self.clients.remove(client)
                self.usernames.remove(username)
                client.socket.close()
                break

    def users_connected(self):
        return self.usernames

if __name__ == "__main__":
    server = Server()
    server.connect()
    server.receive_connections()
