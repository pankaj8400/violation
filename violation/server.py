import os
from socket import *

# Configuration
host = ''  # Bind to all available interfaces
port = 7777
save_path = 'received_images'  # Directory to save received files

# Create directory if it does not exist
os.makedirs(save_path, exist_ok=True)

# Setup server socket
s = socket(AF_INET, SOCK_STREAM)
s.bind((host, port))
s.listen(5)
print("Server listening for connections...")

conn, addr = s.accept()
print(f"Connected by {addr}")

def receive_file():
    while True:
        # Receive the length of the file name
        filename_length = conn.recv(4)
        if not filename_length:
            break

        filename_length = int.from_bytes(filename_length, byteorder='big')
        filename = conn.recv(filename_length).decode()

        if filename == 'END':
            break  # End-of-transfer signal
     

        # Prepare to receive the file data
        filepath = os.path.join(save_path, filename)
        with open(filepath, 'wb') as f:
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                f.write(chunk)
        print(f"Received and saved file: {filename}")

try:
    receive_file()

finally:
    conn.close()
    s.close()





# from socket import *

# host = "192.168.1.33"  # The IP address of your Windows machine
# port = 7777

# # Create a socket object
# s = socket(AF_INET, SOCK_STREAM)

# # Bind the socket to the specified host and port
# s.connect((host, port))

# data = s.recv(1024)
# print("recieved",data.decode())

# s.close









'''
import os
from socket import *

# Configuration
host = '192.168.1.33'  # Server IP address
port = 7777
folder_path ="C:\\Users\\Pankaj Kumar Dubey\\Music\\images"  # Folder containing images

# Setup client socket
s = socket(AF_INET, SOCK_STREAM)
s.connect((host, port))

try:
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            # Send the length of the file name
            filename_length = len(filename).to_bytes(4, byteorder='big')
            s.sendall(filename_length)
            s.sendall(filename.encode())

            # Send the file data
            with open(filepath, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    s.sendall(chunk)

            print(f"Sent file: {filename}")

finally:
    s.close()
'''
