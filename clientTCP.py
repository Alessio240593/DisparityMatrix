import pickle
import socket
import time
from PIL import Image

HOST = "127.0.0.1"
PORT = 50001
INITIAL_MESSAGE = 'ready?'
RCV_WINDOW = 64
TIME = 'network/time/time.csv'

print(f"* Client → connect to {HOST} on port {PORT} in progress...")

data = Image.open('compression/pillow/png/disparity0compressed.png')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

start = time.time()

header = dict(
    size=data.size,
    msg=INITIAL_MESSAGE,
    time=start
)

print("* Client → Sending request to server")

sock.sendall(pickle.dumps(header))

resp = sock.recv(RCV_WINDOW)

print("+ Server → " + resp.decode())

if resp.decode() == 'Ok':
    print("* Client → sending disparity map to server")

    sock.sendall(pickle.dumps(data))

    end = time.time()

    sock.close()

    print(f"* Client → Time to encode disparity map: {end - start} [s]")

    with open(TIME, 'a+') as file:
        file.write(f"Client encoding;{end - start}\n")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    print("+ Server → " + sock.recv(RCV_WINDOW).decode())

    sock.close()
else:
    sock.close()