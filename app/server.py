import socket
import asyncio
from datetime import datetime
from dataclasses import dataclass
import random
import select
import argparse

parser = argparse.ArgumentParser(description='Chat server')
parser.add_argument('--host', type=str, default='localhost', help='Host')
parser.add_argument('--port', type=int, default=8080, help='Port')
parser.add_argument('--max', type=int, default=5, help='Max connections')
args = parser.parse_args()

#
                   
class Server:
    clients = []
    usernames = []
    chat_room = ''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockets = [server]

    def connect(self):
        self.server.bind((args.host, args.port))
        self.server.listen(args.max)
        print(f"Server running on {args.host}:{args.port}")

    async def send_to_chat_room(self, message):
        for client in self.clients:
            if client.username == 'chat_room':
                print(f'Procesando mensaje {message}')
                latency = random.uniform(0.005, 1.5)
                await asyncio.sleep(latency)
                client.socket.send(message)
                print(f'Mensaje enviado {message}')

    async def accept_connection(self):
        # Si el socket listo es el socket del servidor, significa que hay una nueva conexión
        client, address = self.server.accept()
        self.sockets.append(client)

        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')

        new_client = Client(username, client, address)

        self.clients.append(new_client)
        self.usernames.append(username)

        print('Connecting...')
        latency = random.uniform(0.005, 1.5)
        await asyncio.sleep(latency)

        print(f"{username} is connected with {str(address)}")

        message = f"ChatBot: {username} joined the chat!".encode("utf-8")
        await self.send_to_chat_room(message)
        client.send("Connected to server".encode("utf-8"))

    async def handle_message(self, s):
        try:
            message = s.recv(1024)
            if message == b'get_users':
                users = 'USERS: '+', '.join(self.users_connected())
                s.send(users.encode('utf-8'))
            elif message:
                current_time = datetime.now().strftime("%H:%M:%S")
                formatted_message = f"{current_time} {message.decode('utf-8')}"
                await self.send_to_chat_room(formatted_message.encode('utf-8'))
            else:
                peername = s.getpeername()
                print(f'El cliente {peername} se ha desconectado')
                index = self.sockets.index(s)
                client = self.clients[index-1]
                await self.send_to_chat_room(f'{client.username} se ha desconectado'.encode('utf-8'))
                s.close()
                self.sockets.remove(s)
                self.clients.remove(client)
                self.usernames.remove(client.username)
        except Exception as e:
            print(f'Error al recibir mensaje del cliente {e}')
            s.close()
            self.sockets.remove(s)
            index = self.sockets.index(s)
            client = self.clients[index-1]
            self.clients.remove(client)
            self.usernames.remove(client.username)
            await self.send_to_chat_room(f'{client.username} se ha desconectado'.encode('utf-8'))

    def receive_connections(self):
        
        while True:
            # Usar select para esperar hasta que alguno de los sockets esté listo para ser leído
            ready_to_read, _, _ = select.select(self.sockets, [], [])
    
            for s in ready_to_read:
                if s is self.server:
                    asyncio.run(self.accept_connection())
                else:
                    # Si el socket listo no es el socket del servidor, significa que hay un nuevo mensaje
                    asyncio.run(self.handle_message(s))
                    
   
    def users_connected(self):
        return self.usernames

@dataclass
class Client:
    username: str
    socket: socket.socket
    address: str

if __name__ == "__main__":
    server = Server()
    server.connect()
    server.receive_connections()
