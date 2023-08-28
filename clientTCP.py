import os.path
import pickle
import socket
import tarfile
import time
from PIL import Image


def run_client(compressed, buffer):
    HOST = "127.0.0.1"
    PORT = 50000
    INITIAL_MESSAGE = 'ready?'
    RCV_WINDOW = 64

    lst = os.listdir("compression/pillow/png")  # your directory path
    number_files = len(lst)

    for curr in range(0, number_files):
        print(f"* Client → connect to {HOST} on port {PORT} in progress...")

        data = Image.open('compression/pillow/png/disparity' + str(curr) + 'compressed.png')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))

        t0 = time.time()

        header = dict(
            size=data.size,
            msg=INITIAL_MESSAGE
        )

        print("* Client → Sending request to server")

        sock.sendall(pickle.dumps(header))

        resp = sock.recv(RCV_WINDOW)

        t1 = time.time()

        print("+ Server → " + resp.decode())

        if resp.decode() == 'Ok':
            print("* Client → sending disparity map to server")

            tar = tarfile.open('prova.tar.gz', 'w:gz')

            if compressed:
                t = 'network/time/tcp/tcp_times_compressed_' + str(buffer) + '.csv'
                tar.add("compression/pillow/png/disparity" + str(curr) + "compressed.png",
                        arcname=os.path.basename("disparity" + str(curr) + "compressed.png"))
            else:
                t = 'network/time/tcp/tcp_times_' + str(buffer) + '.csv'
                tar.add("disparity/png/disparity" + str(curr) + ".png",
                        arcname=os.path.basename("disparity" + str(curr) + ".png"))

            tar.close()

            t2 = time.time()

            sock.sendall(pickle.dumps(open('prova.tar.gz', 'rb').read()))

            sock.sendall(b"end")

            print("+ Server → " + sock.recv(RCV_WINDOW).decode())

            t3 = time.time()

            print(f"* Client → Encoding time {t2 - t1} [s]")
            print(f"* Client → Total time {t3 - t0} [s]")
            print(f"* Client → Data_transfer_time: {((t3 - t2) - ((t1 - t0) / 2))} [s]\n")

            sock.close()

            if os.path.exists(t):
                with open(t, "a") as f:
                    f.write("Frame " + str(curr) + ";" + str(t3 - t0) + "\n")
            else:
                with open(t, "w") as f:
                    f.write("Frame " + str(curr) + ";" + str(t3 - t0) + "\n")

            os.remove('prova.tar.gz')

        else:
            sock.close()


if __name__ == '__main__':
    rcv_buffer_values = [1024, 2048, 4096, 8192, 16384, 32768, 65536]

    for val in rcv_buffer_values:
        run_client(compressed=False, buffer=val)
        time.sleep(0.2)
        run_client(compressed=True, buffer=val)
