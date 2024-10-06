import obspy
import obspy.signal.trigger
import numpy as np
from pathlib import Path
import pandas as pd
from scipy import signal
from scipy.ndimage import gaussian_filter1d
import io
import base64

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Union

base_dir = Path("../data/space_apps_2024_seismic_detection")
STREAM_RESAMPLE = 4


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


@app.get("/landerdata/{planet}")
def lander_api(planet: str, q: Union[str, None] = None):
    filename = q[:-5]  # remove the .json
    X_train, y_train, X_test, train_filenames, test_filenames = data[planet]

    ftype = "train" if filename in [f.stem for f in train_filenames] else "test"
    arr = None
    if ftype == "train":
        idx = [f.stem for f in train_filenames].index(filename)
        stream = X_train[idx].copy()
        arr = y_train[idx]
    else:
        idx = [f.stem for f in test_filenames].index(filename)
        stream = X_test[idx].copy()

    plt.figure(figsize=(10, 6))
    plt.plot(stream[0].times(), stream[0].data)
    plt.axis("off")

    # Save the image to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png", bbox_inches="tight", pad_inches=0)
    img_buffer.seek(0)
    plt.close()
    hf_str = base64.b64encode(img_buffer.getvalue()).decode()

    stream.resample(STREAM_RESAMPLE)
    plt.figure(figsize=(10, 6))
    plt.plot(stream[0].times(), stream[0].data)
    plt.axis("off")

    # Save the image to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png", bbox_inches="tight", pad_inches=0)
    img_buffer.seek(0)
    plt.close()
    lf_str = base64.b64encode(img_buffer.getvalue()).decode()
    return {
        "lf_signal": f"data:image/png;base64,{lf_str}",
        "hf_signal": f"data:image/png;base64,{hf_str}",
    }


@app.get("/stalta/{planet}")
def stalta_api(planet: str, q: Union[str, None] = None):
    filename = q[:-5]  # remove the .json
    X_train, y_train, X_test, train_filenames, test_filenames = data[planet]

    ftype = "train" if filename in [f.stem for f in train_filenames] else "test"
    arr = None
    if ftype == "train":
        idx = [f.stem for f in train_filenames].index(filename)
        stream = X_train[idx].copy()
        arr = y_train[idx]
    else:
        idx = [f.stem for f in test_filenames].index(filename)
        stream = X_test[idx].copy()

    stream.resample(STREAM_RESAMPLE)
    if planet == "moon":
        arr_time, out = make_stalta_prediction(stream, 600, 10000)
    else:
        arr_time, out = make_stalta_prediction(stream, 12, 60)

    return {
        "planet": planet,
        "filename": filename,
        "arr_time": arr,
        "arr_time_pred": arr_time,
    }


@app.get("/spectogram/{planet}")
def spectogram_api(planet: str, q: Union[str, None] = None):
    print(planet, q)
    filename = q[:-5]  # remove the .json
    X_train, y_train, X_test, train_filenames, test_filenames = data[planet]

    ftype = "train" if filename in [f.stem for f in train_filenames] else "test"
    arr = None
    if ftype == "train":
        idx = [f.stem for f in train_filenames].index(filename)
        stream = X_train[idx].copy()
        arr = y_train[idx]
    else:
        idx = [f.stem for f in test_filenames].index(filename)
        stream = X_test[idx].copy()

    # stream.resample(STREAM_RESAMPLE)
    if planet == "moon":
        arr_time, stream2, sxx, t = make_spectogram_prediction(stream, 1, 2)
    else:
        arr_time, stream2, sxx, t = make_spectogram_prediction(stream, 1, 2)

    # Create the spectrogram image
    plt.figure(figsize=(10, 6))
    plt.imshow(sxx, cmap=cm.jet, aspect="auto")
    plt.axis("off")

    # Save the image to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png", bbox_inches="tight", pad_inches=0)
    img_buffer.seek(0)
    plt.close()

    # Encode the image to base64
    img_str = base64.b64encode(img_buffer.getvalue()).decode()

    return {
        "planet": planet,
        "filename": filename,
        "arr_time": arr,
        "arr_time_pred": arr_time,
        "spectogram": f"data:image/png;base64,{img_str}",
    }


@app.get("/hf_sections/{planet}")
def high_frequency_sections_api(planet: str, q: Union[str, None] = None):
    print(planet, q)
    filename = q[:-5]  # remove the .json
    X_train, y_train, X_test, train_filenames, test_filenames = data[planet]

    ftype = "train" if filename in [f.stem for f in train_filenames] else "test"
    arr = None
    if ftype == "train":
        idx = [f.stem for f in train_filenames].index(filename)
        stream = X_train[idx].copy()
        arr = y_train[idx]
    else:
        idx = [f.stem for f in test_filenames].index(filename)
        stream = X_test[idx].copy()

    stream = stream.filter("lowpass", freq=1.0)
    stream = stream.filter("highpass", freq=2.0)
    f, t, sxx = signal.spectrogram(stream[0].data, stream[0].stats.sampling_rate)
    maxpwr = np.max(sxx, axis=0)
    smoothed_maxpwr = gaussian_filter1d(maxpwr, sigma=5)
    # normalise to be between 0 and 1
    smoothed_maxpwr = (smoothed_maxpwr - np.min(smoothed_maxpwr)) / (
        np.max(smoothed_maxpwr) - np.min(smoothed_maxpwr)
    )
    peaks = signal.find_peaks(smoothed_maxpwr, prominence=1e-2)[0]
    widths, width_heights, left_ips, right_ips = signal.peak_widths(
        smoothed_maxpwr, peaks, rel_height=0.5
    )
    left_times = t[left_ips.astype(int)]
    right_times = t[right_ips.astype(int)]
    widths = np.abs(left_times - right_times)

    x = np.arange(len(smoothed_maxpwr))
    xp, yp = x[peaks], smoothed_maxpwr[peaks]

    plt.figure(figsize=(10, 6), dpi=300)
    plt.plot(stream[0].times(), stream[0].data)
    for peak in peaks:
        time = t[peak]
        plt.axvline(time, c="r", linestyle="--", alpha=0.5)

    for left, right in zip(left_times, right_times):
        # plt.axvline(left, color="g", linewidth=2)
        # plt.axvline(right, color="g", linewidth=2)
        plt.fill_between(
            [left, right], plt.ylim()[0], plt.ylim()[1], color="g", alpha=0.2
        )
    # plt.axis("off")

    # Save the image to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png", bbox_inches="tight", pad_inches=0)
    img_buffer.seek(0)
    plt.close()

    # Encode the image to base64
    img_str = base64.b64encode(img_buffer.getvalue()).decode()

    return {
        "planet": planet,
        "filename": filename,
        "hf_regions": f"data:image/png;base64,{img_str}",
    }


@app.get("/importance/{planet}")
def importance_api(planet: str, q: Union[str, None] = None):
    print(planet, q)
    filename = q[:-5]  # remove the .json
    path = Path(f"../data/data_importance/{filename}.png")

    # Read and display the image using matplotlib
    img = plt.imread(path)
    plt.figure(figsize=(10, 6))
    plt.imshow(img)
    plt.axis("off")

    # Save the displayed image to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png", bbox_inches="tight", pad_inches=0)
    img_buffer.seek(0)
    plt.close()

    # Get the image data from the buffer
    img_data = img_buffer.getvalue()

    # Encode the image to base64
    img_str = base64.b64encode(img_data).decode()

    return {
        "planet": planet,
        "filename": filename,
        "importance": f"data:image/png;base64,{img_str}",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
