import os
import socket 
import threading

def start_client():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    clientSocket.connect(("127.0.0.1", 5000))
    
    req = input("Request <UPLOAD filename or DOWNLOAD filename>: ")
    clientSocket.send(req.encode())

    filename = req.split()[1]
    if req.startswith("UPLOAD"):
        try:
            with open(filename, "rb") as file:
                print(f"Client Uploading {filename}")
                while chunk := file.read(1024):
                    clientSocket.send(chunk)
                print(f"{filename} is uploaded by client")
        except FileNotFoundError:
            print("File not found")

    if req.startswith("DOWNLOAD"):
        with open(filename, "wb") as file:
            print(f"Client Downloading {filename}")
            while True:
                data = clientSocket.recv(1024)
                if not data:
                    break
                file.write(data)
            print(f"Client successfully downloaded {filename}")
    
    clientSocket.close()

if __name__ == "__main__":
    start_client()
        
