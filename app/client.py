import socket
import threading
import asyncio
import os
import argparse
from dataclasses import dataclass

@dataclass
class Client:
    username: str
    socket: socket.socket
    address: str

class ClientManagment:

    def write_messages(self):
        while True:
            message_content = input("-> ")
            if message_content == "exit":
                client.close()
                os._exit(0)
            elif message_content == 'back':
                break
            else:
                message = f"{username}: {message_content}"
                client.send(message.encode('utf-8'))

    def receive_messages(self):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == "@username":
                    client.send(username.encode("utf-8"))
                elif message.startswith("USERS ONLINE: "):
                    print(message)
                else:
                    print(f"\nSERVER MESSAGE: {message}")
            except:
                print("An error occurred")
                client.close()
                break

    async def compress_file(self):
        print("Compressing file...")
        await asyncio.sleep(5)
        print("File compressed successfully")

    async def connect_to_server(self):
        print("Establishing connection with the server...")
        await asyncio.sleep(3)
        print("Connected to server")

    async def request_users(self):
        print("Requesting users...")
        await asyncio.sleep(5)
        print("Users received")

    async def send_file(self, file_name):
        task1 = asyncio.create_task(self.compress_file())
        task2 = asyncio.create_task(self.connect_to_server())

        await asyncio.gather(task1, task2)

        print(f"Sending file '{file_name}' ...")
        await asyncio.sleep(5)
        client.send(f"{username} sent a file --> {file_name}".encode('utf-8'))
        print(f"File '{file_name}' sent successfully")

    async def get_users_connected(self):
        task1 = asyncio.create_task(self.connect_to_server())
        task2 = asyncio.create_task(self.request_users())

        await asyncio.gather(task1, task2)

        client.send("get_users".encode('utf-8'))
        await asyncio.sleep(3)

    def menu(self):
        while True:
            print("1. Send messages")
            print("2. Send file")
            print("3. Users connected")
            print("4. Exit")
            option = input("Enter an option: ")
            if option == "1":
                self.write_messages()
            elif option == "2":
                file = input("Enter the file name: ")
                asyncio.run(self.send_file(file))
            elif option == "3":
                asyncio.run(self.get_users_connected())
            elif option == "4":
                client.send("".encode('utf-8'))
                client.close()
                os._exit(0)
            else:
                print("Invalid option")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chat Room Server')
    parser.add_argument('-ht', '--host', type=str, help='Host IP', required=True)
    parser.add_argument('-p', '--port', type=int, help='Port', required=True)
    args = parser.parse_args()

    host = args.host
    port = args.port

    username = input("Enter your username: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    client_managment = ClientManagment()
    receive_thread = threading.Thread(target=client_managment.receive_messages)
    receive_thread.start()
    client_managment.menu()
