import os
import pickle
import socket
import statistics
import time
from os.path import exists

import pandas as pd

import init


def tcp_statistics(buffer):
    frame = pd.read_csv("network/time/tcp/tcp_times_" + str(buffer) + ".csv")

    frame.columns = ['data']

    value = frame['data'].values

    new = [float(x.split(';')[1]) for x in value]

    with open('network/time/tcp/tcp_times_' + str(buffer) + '.csv', 'a') as f:
        f.write(f"\ntot;{sum(new)}\n")
        f.write(f"\nmean;{statistics.mean(new)}\n")
        f.write(f"median;{statistics.median(new)}\n")
        f.write(f"stdev;{statistics.stdev(new)}\n")
        f.write(f"mode;{statistics.mode(new)}\n")

    frame = pd.read_csv("network/time/tcp/tcp_times_compressed_" + str(buffer) + ".csv")

    frame.columns = ['data']

    value = frame['data'].values

    new = [float(x.split(';')[1]) for x in value]

    with open('network/time/tcp/tcp_times_compressed_' + str(buffer) + '.csv', 'a') as f:
        f.write(f"\ntot;{sum(new)}\n")
        f.write(f"\nmean;{statistics.mean(new)}\n")
        f.write(f"median;{statistics.median(new)}\n")
        f.write(f"stdev;{statistics.stdev(new)}\n")
        f.write(f"mode;{statistics.mode(new)}\n")


def run_server(compressed, buffer):
    HOST = "127.0.0.1"
    PORT = 50000
    RCV_WINDOW = buffer
    TIME = 'network/time/tcp'

    if compressed:
        CLIENT_DATA = 'network/data/tcp/compressed'
        if not exists(TIME):
            os.makedirs(TIME)
        elif exists(TIME + "/tcp_times_compressed_" + str(buffer) + ".csv"):
            os.remove(TIME + "/tcp_times_compressed_" + str(buffer) + ".csv")
    else:
        CLIENT_DATA = 'network/data/tcp/not_compressed'
        if not exists(TIME):
            os.makedirs(TIME)
        elif exists(TIME + "/tcp_times_" + str(buffer) + ".csv"):
            os.remove(TIME + "/tcp_times_" + str(buffer) + ".csv")

    if not exists(CLIENT_DATA):
        os.makedirs(CLIENT_DATA)

    lst = os.listdir("compression/pillow/png")  # your directory path
    number_files = len(lst)

    count = 0

    while count < number_files:
        print(f"+ Server → {HOST} waiting on port {PORT}...")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
            exit(0)

        buffer = b""
        while True:
            data = conn.recv(RCV_WINDOW)
            if b"end" in data:
                buffer += data[: (len(data) - len(b"end"))]
                break
            buffer += data

        data = pickle.loads(buffer)

        end = time.time()

        file = open(CLIENT_DATA + "/frame" + str(count) + "_tcp.tar.gz", "wb")

        count = count + 1

        file.write(data)

        print("+ Server → data receved correctly")

        print(f"+ Server → Time to decode data {end - start} [s]")

        print("+ Server → sending feedback to client \n")

        conn.send(b'Data received correctly')

        conn.close()


if __name__ == '__main__':
    rcv_buffer_values = [1024, 2048, 4096, 8192, 16384, 32768, 65536]

    init.disparity_compression()

    for val in rcv_buffer_values:
        run_server(compressed=False, buffer=val)
        run_server(compressed=True, buffer=val)

    for val in rcv_buffer_values:
        tcp_statistics(val)