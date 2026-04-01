import pandas as pd
import os
from os import listdir
from tqdm import tqdm


CHUNK_SIZE = 300_000 # adjust this to process more or less data at same time
SAMPLE_FRAC = 0.01 # adjust this to sample more or less data

station_dtypes = {
    "start_station_id": "string",
    "end_station_id": "string"
}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
TRIPDATA_DIR = os.path.join(DATA_DIR, "tripdata")
OUTPUT_FILE = os.path.join(DATA_DIR, "sampled_data.csv")

files = [f for f in listdir(TRIPDATA_DIR) if f.endswith(".csv")]
dfs = []

for f in tqdm(files, desc="Processing files"):
    chunk_list = []

    chunk_iter = pd.read_csv(os.path.join(TRIPDATA_DIR, f), chunksize=CHUNK_SIZE, dtype=station_dtypes)
    for chunk in tqdm(chunk_iter, desc=f"Sampling {f}", leave=False):
        chunk_sample = chunk.sample(frac=SAMPLE_FRAC, random_state=42)
        chunk_list.append(chunk_sample)

    dfs.append(pd.concat(chunk_list, ignore_index=True))

df = pd.concat(dfs, ignore_index=True)
df.head()
df.to_csv(OUTPUT_FILE, index=False)