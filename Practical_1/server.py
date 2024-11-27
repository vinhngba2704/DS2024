import os
import socket
import threading

def start_server():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port = 5000
    serverSocket.bind(("127.0.0.1", 5000))
    serverSocket.listen(1)
    print(f"Server is listening on port {port}...")

    conn, addr = serverSocket.accept()
    print(f"Connection establised with address {addr}")

    command = conn.recv(1024).decode()

    if command.startswith("UPLOAD"):
        filename = command.split()[1]

        with open(filename, "wb") as file: # "wb": open file with write-binary model
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)
            print(f"{filename} is received by server!")
    
    if command.startswith("DOWNLOAD"):
        filename = command.split()[1]
        try:
            with open(filename, "rb") as file:
                print(f"Server sending {filename}")
                while chunk := file.read(1024):
                    conn.send(chunk)
                print(f"Server successfully sent {filename}")
        except FileNotFoundError:
            conn.send(b"Error: File not found")

    conn.close()
    serverSocket.close()

if __name__ == "__main__":
    start_server()
