import pickle
import shutil
import statistics
import time
import os
from os.path import exists

import pandas as pd
from flask import Flask, request

import init


def flask_statistic():
    frame = pd.read_csv("network/time/flask/flask_times.csv")

    frame.columns = ['data']

    val = frame['data'].values

    new = [float(x.split(';')[1]) for x in val]

    with open('network/time/flask/flask_times.csv', 'a') as f:
        f.write(f"\ntot;{sum(new)}\n")
        f.write(f"\nmean;{statistics.mean(new)}\n")
        f.write(f"median;{statistics.median(new)}\n")
        f.write(f"stdev;{statistics.stdev(new)}\n")
        f.write(f"mode;{statistics.mode(new)}\n")

    frame = pd.read_csv("network/time/flask/flask_times_compressed.csv")

    frame.columns = ['data']

    val = frame['data'].values

    new = [float(x.split(';')[1]) for x in val]

    with open('network/time/flask/flask_times_compressed.csv', 'a') as f:
        f.write(f"\ntot;{sum(new)}\n")
        f.write(f"\nmean;{statistics.mean(new)}\n")
        f.write(f"median;{statistics.median(new)}\n")
        f.write(f"stdev;{statistics.stdev(new)}\n")
        f.write(f"mode;{statistics.mode(new)}\n")


app = Flask(__name__)
TIME = 'network/time/flask'


@app.route('/', methods=['POST'])
def result():
    if request.args.get("compressed") == 'True':
        CLIENT_DATA = 'network/data/flask/compressed'
    else:
        CLIENT_DATA = 'network/data/flask/not_compressed'

    if not exists(CLIENT_DATA):
        os.makedirs(CLIENT_DATA)

    start = time.time()

    msg = "ready"

    if request.data == b'ready?':
        print(f"* Client → {request.data.decode()}")
        print(f"+ Server → sending {msg} to client")
        return msg
    else:
        tar = pickle.loads(request.data)

        file = open(CLIENT_DATA + "/frame" + request.args.get("frame") + "_flask.tar.gz", "wb")

        file.write(tar)

        end = time.time()

        print(f"+ Server → decoding time: {end - start}")

        print(f"+ Server → received all data from client")

        return "Received"


@app.route('/exit', methods=['GET'])
def statistic():
    flask_statistic()
    return 'Shutdown-' + str(os.getpid())


if __name__ == '__main__':
    if not exists(TIME):
        os.makedirs(TIME)

    if exists(TIME + "/flask_times.csv"):
        os.remove(TIME + "/flask_times.csv")

    if exists(TIME + "/flask_times_compressed.csv"):
        os.remove(TIME + "/flask_times_compressed.csv")

    shutil.rmtree('network/data/flask/compressed', ignore_errors=True)
    shutil.rmtree('network/data/flask/not_compressed', ignore_errors=True)

    init.disparity_compression()

    app.run(threaded=True, host="0.0.0.0", port=5000)
    app.run(debug=True)