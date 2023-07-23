import os
import pickle
import socket
import time
from os.path import exists
import numpy as np
from PIL import Image

HOST = "127.0.0.1"
PORT = 50001
RCV_WINDOW = 4096
TIME = 'network/time'
CLIENT_DATA = 'network/data'

if not exists(TIME):
    os.makedirs(TIME)
elif exists(TIME + "/time.csv"):
    os.remove(TIME + "/time.csv")

if not exists(CLIENT_DATA):
    os.makedirs(CLIENT_DATA)

print(f"+ Server → {HOST} waiting on port {PORT}...")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()
conn, addr = sock.accept()

start = time.time()

header = pickle.loads(conn.recv(RCV_WINDOW))

print("* Client → " + str(header['msg']))

if header['msg'] == "ready?":
    print("+ Server → sending confirm to client")
    conn.send(b"Ok")
else:
    exit(-1)

buffer = b""
while True:
    data = conn.recv(RCV_WINDOW)
    if not data:
        break
    buffer += data

data = pickle.loads(buffer)

end = time.time()

print("+ Server → data receved correctly")

print(f"+ Server → Time to decode data {end - start} [s]")
print(f"+ Server → Total time: {end - header['time']} [s]")

conn.close()

new_im = Image.fromarray(np.array(data), 'L')

new_im.save(CLIENT_DATA + '/client_data.png', quality=90, optimize=True)

with open(TIME + "/time.csv", 'a+') as file:
    file.write(f"Server decoding;{end - start}\n")
    file.write(f"Total time;{end - header['time']}\n")

sock.listen()
conn, addr = sock.accept()

print("+ Server → sending feedback to client")

conn.send(b'Data received correctly')

conn.close()