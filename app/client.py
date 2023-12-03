import socket
import threading
from constants import HOST, PORT
import asyncio
import os

username = input("Enter your username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def write_messages():
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

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                print(f"\nMENSAJE DEL SERVIDOR: {message}")
        except:
            print("An error occurred")
            client.close()
            break

async def compress_file():
    print("Compressing file...")
    await asyncio.sleep(5)
    print("File compressed successfully")

async def connect_to_server():
    print("Establishing connection with the server...")
    await asyncio.sleep(3)
    print("Connected to server")

async def request_users():
    print("Requesting users...")
    await asyncio.sleep(5)
    print("Users received")

async def send_file(file_name):
    task1 = asyncio.create_task(compress_file())
    task2 = asyncio.create_task(connect_to_server())

    await asyncio.gather(task1, task2)

    print(f"Sending file '{file_name}' ...")
    await asyncio.sleep(5)
    print(f"File '{file_name}' sent successfully")

async def get_users_connected():
    task1 = asyncio.create_task(connect_to_server())
    task2 = asyncio.create_task(request_users())

    await asyncio.gather(task1, task2)

    client.send("get_users".encode('utf-8'))
    await asyncio.sleep(3)


def menu():
    while True:
        print("1. Send messages")
        print("2. Send file")
        print("3. Users connected")
        print("4. Exit")
        option = input("Enter an option: ")
        if option == "1":
            write_messages()
        elif option == "2":
            file = input("Enter the file name: ")
            asyncio.run(send_file(file))
        elif option == "3":
            asyncio.run(get_users_connected())
        elif option == "4":
            client.send("".encode('utf-8'))
            client.close()
            os._exit(0)
        else:
            print("Invalid option")

if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()
    menu()
