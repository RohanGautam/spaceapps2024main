import obspy
from obspy.clients.fdsn import Client
from obspy.core import UTCDateTime
import obspy.signal.trigger
from scatseisnet import ScatteringNetwork
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import dates as mdates
import sklearn.decomposition
from sklearn.decomposition import FastICA, PCA
from sklearn.cluster import KMeans, DBSCAN
import umap
from tqdm.auto import tqdm
from pathlib import Path
import pandas as pd
import datetime
from scipy import signal
from matplotlib import cm
from scipy.ndimage import gaussian_filter1d
import seaborn as sns
import json


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Union

base_dir = Path("../data/space_apps_2024_seismic_detection")


def load_lunar(base_dir: Path):
    print("> Loading lunar")
    cat_file = (
        base_dir / "data/lunar/training/catalogs/apollo12_catalog_GradeA_final.csv"
    )
    cat = pd.read_csv(cat_file)
    # for convenient access
    cat["arrival_time"] = pd.to_datetime(cat["time_abs(%Y-%m-%dT%H:%M:%S.%f)"])
    cat["arrival_time_rel"] = cat["time_rel(sec)"]

    train_dir = base_dir / "data/lunar/training/data/"
    test_dir = base_dir / "data/lunar/test/data/"

    # get from df so we can match with arrival times
    train_filenames = [train_dir / f"S12_GradeA/{x}.mseed" for x in cat.filename]
    test_filenames = list(test_dir.rglob("*.mseed"))

    print("training data: ", len(list(train_dir.rglob("*.mseed"))))
    print("test data: ", len(test_filenames))

    for i, f in enumerate(train_filenames):
        if "evid00029" in str(f):
            train_filenames[i] = Path(
                "../data/space_apps_2024_seismic_detection/data/lunar/training/data/S12_GradeA/xa.s12.00.mhz.1971-04-13HR02_evid00029.mseed"
            )
    train_streams = []
    for f in train_filenames:
        try:
            train_streams.append(obspy.read(f))
        except Exception as e:
            print(f"Error reading file {f}: {e}")

    test_streams = []
    for f in test_filenames:
        try:
            test_streams.append(obspy.read(f))
        except Exception as e:
            print(f"Error reading file {f}: {e}")
    arr_times = cat["arrival_time_rel"].to_numpy()
    return train_streams, arr_times, test_streams, train_filenames, test_filenames


def load_martian(base_dir: Path):
    print("> Loading martian")
    base_dir = Path("../data/space_apps_2024_seismic_detection")
    cat_file = (
        base_dir / "data/mars/training/catalogs/Mars_InSight_training_catalog_final.csv"
    )
    cat = pd.read_csv(cat_file)
    # for convenient access
    cat["arrival_time"] = pd.to_datetime(cat["time_abs(%Y-%m-%dT%H:%M:%S.%f)"])
    cat["arrival_time_rel"] = cat["time_rel(sec)"]
    train_dir = base_dir / "data/mars/training/data/"
    test_dir = base_dir / "data/mars/test/data/"

    # get from df so we can match with arrival times
    train_filenames = [train_dir / f"{x[:-4]}.mseed" for x in cat.filename]
    test_filenames = list(test_dir.rglob("*.mseed"))

    print("training data: ", len(list(train_dir.rglob("*.mseed"))))
    print("test data: ", len(test_filenames))

    train_streams = []
    for f in train_filenames:
        try:
            train_streams.append(obspy.read(f))
        except Exception as e:
            print(f"Error reading file {f}: {e}")

    test_streams = []
    for f in test_filenames:
        try:
            test_streams.append(obspy.read(f))
        except Exception as e:
            print(f"Error reading file {f}: {e}")
    arr_times = cat["arrival_time_rel"].to_numpy()
    return train_streams, arr_times, test_streams, train_filenames, test_filenames


def make_stalta_prediction(stream, sta_len=120, lta_len=600, trg_on=3):
    out = obspy.signal.trigger.classic_sta_lta(
        stream[0].data,
        nsta=sta_len * stream[0].stats.sampling_rate,
        nlta=lta_len * stream[0].stats.sampling_rate,
    )
    t = obspy.signal.trigger.trigger_onset(out, trg_on, 1)
    assert len(t) > 0
    arr_time = stream[0].times()[t[0, 0]]
    return arr_time, out


def make_spectogram_prediction(stream, fl=1, fh=2):
    stream2 = stream.copy()
    stream2 = stream2.filter("lowpass", freq=fl)
    stream2 = stream2.filter("highpass", freq=fh)
    f, t, sxx = signal.spectrogram(stream2[0].data, stream[0].stats.sampling_rate)
    maxpwr = np.max(sxx, axis=0)
    # smooth it
    smoothed_maxpwr = gaussian_filter1d(maxpwr, sigma=5)  # Adjust sigma as needed
    # peaks = signal.find_peaks(smoothed_maxpwr, width=10, threshold=1e3)[0]
    peaks = signal.find_peaks(smoothed_maxpwr)[0]
    assert len(peaks) > 0
    max_val_peak = peaks[np.argmax(smoothed_maxpwr[peaks])]
    return t[max_val_peak], stream2, sxx, t


data = {
    "moon": load_lunar(base_dir),
    "mars": load_martian(base_dir),
}

print("Loaded waveforms")


app = FastAPI()
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Quiver API"}


@app.get("/stalta/{planet}")
def read_item(planet: str, q: Union[str, None] = None):
    filename = q[:-5]  # remove the .json
    X_train, y_train, X_test, train_filenames, test_filenames = data[planet]

    ftype = "train" if filename in [f.stem for f in train_filenames] else "test"
    arr = None
    if ftype == "train":
        idx = [f.stem for f in train_filenames].index(filename)
        stream = X_train[idx]
        arr = y_train[idx]
    else:
        idx = [f.stem for f in test_filenames].index(filename)
        stream = X_test[idx]

    if planet == "moon":
        arr_time, out = make_stalta_prediction(stream, 600, 10000)
    else:
        arr_time, out = make_stalta_prediction(stream, 120, 600)

    return {
        "planet": planet,
        "filename": filename,
        "arr_time": arr,
        "arr_time_pred": arr_time,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
