import os
import pickle
import signal
import time

import requests
import tarfile


def run_client_flask(compressed):
    payload = {"compressed": compressed}

    HOST = "127.0.0.1"
    PORT = 5000

    lst = os.listdir("compression/pillow/png")  # your directory path
    number_files = len(lst)

    for curr in range(0, number_files):
        print(f"* Client → connect to {HOST} on port {PORT} in progress...")

        payload["frame"] = curr

        t0 = time.time()

        headers = {'Content-Transfer-Encoding': 'text/plain'}
        data = "ready?"

        response = requests.post("http://127.0.0.1:5000", headers=headers, data=data, params=payload)

        t1 = time.time()

        print("+ Server → " + response.content.decode())

        if response.content.decode() == "ready":
            print("* Client → sending data to server")

            headers = {'Content-Transfer-Encoding': 'application/gzip'}

            tar = tarfile.open('prova.tar.gz', 'w:gz')

            if compressed:
                tar.add("compression/pillow/png/disparity" + str(curr) + "compressed.png",
                        arcname=os.path.basename("disparity" + str(curr) + "compressed.png"))
            else:
                tar.add("disparity/png/disparity" + str(curr) + ".png",
                        arcname=os.path.basename("disparity" + str(curr) + ".png"))

            tar.close()

            t2 = time.time()

            data = pickle.dumps(open('prova.tar.gz', 'rb').read())

            response = requests.post("http://127.0.0.1:5000", headers=headers, data=data, params=payload)

            t3 = time.time()

            print(f"* Client → encoding time {t2 - t1} [s]")
            print(f"* Client → total time: {((t3 - t2) - ((t1 - t0) / 2))} [s]")

            print("+ Server → " + response.content.decode())

            if compressed:
                TIME = 'network/time/flask/flask_times_compressed.csv'
            else:
                TIME = 'network/time/flask/flask_times.csv'

            if os.path.exists(TIME):
                with open(TIME, "a") as f:
                    f.write("Frame " + str(curr) + ";" + str(t3 - t0) + "\n")
            else:
                with open(TIME, "w") as f:
                    f.write("Frame " + str(curr) + ";" + str(t3 - t0) + "\n")

            os.remove('prova.tar.gz')


if __name__ == '__main__':
    run_client_flask(compressed=True)
    run_client_flask(compressed=False)

    response = requests.get("http://127.0.0.1:5000/exit")

    if response.content.decode().split("-")[0] == 'Shutdown':
        os.kill(int(response.content.decode().split("-")[1]), signal.SIGTERM)
