import socket
import threading
import argparse

username = 'chat_room'

parser = argparse.ArgumentParser(description='Chat Room Server')
parser.add_argument('-ht', '--host', type=str, help='Host IP', required=True)
parser.add_argument('-p', '--port', type=int, help='Port', required=True)
args = parser.parse_args()

host = args.host
port = args.port

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

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
