import os
import requests
import zipfile
from tqdm import tqdm

YEAR = 2021
BASE_URL = "https://s3.amazonaws.com/tripdata"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "data", "tripdata")

os.makedirs(OUTPUT_DIR, exist_ok=True)

year_file = f"{YEAR}-citibike-tripdata.zip"
url = f"{BASE_URL}/{year_file}"

print(f"Downloading {year_file}...")

response = requests.get(url, stream=True)
response.raise_for_status()

total_size = int(response.headers.get('content-length', 0))
chunk_size = 1024 * 1024

zip_path = os.path.join(OUTPUT_DIR, year_file)

with open(zip_path, "wb") as f, tqdm(
    total=total_size, unit='B', unit_scale=True, desc='Downloading', ncols=80
) as pbar:
    for chunk in response.iter_content(chunk_size=chunk_size):
        if chunk:
            f.write(chunk)
            pbar.update(len(chunk))

print("Extracting main zip...")

with zipfile.ZipFile(zip_path, 'r') as z:
    for file in tqdm(z.namelist(), desc='Extracting main ZIP', ncols=80):
        z.extract(file, OUTPUT_DIR)

os.remove(zip_path)
print("Extracting nested monthly zips...")

year_dir = os.path.join(OUTPUT_DIR, f"{YEAR}-citibike-tripdata")
search_root = year_dir if os.path.isdir(year_dir) else OUTPUT_DIR

zip_files = []
for root, dirs, files in os.walk(search_root):
    dirs[:] = [d for d in dirs if d != "__MACOSX"]
    for file in files:
        if file.endswith(".zip"):
            zip_files.append(os.path.join(root, file))

for nested_path in zip_files:
    rel_name = os.path.relpath(nested_path, OUTPUT_DIR)
    print(f"Extracting {rel_name}...")

    with zipfile.ZipFile(nested_path, 'r') as z:
        members = [m for m in z.namelist() if "__MACOSX" not in m]
        for nested_file in tqdm(members, desc=f"Extracting {os.path.basename(nested_path)}", ncols=80):
            z.extract(nested_file, OUTPUT_DIR)

    os.remove(nested_path)

print("Cleaning up non-CSV files and stray folders...")

for root, dirs, files in os.walk(OUTPUT_DIR, topdown=False):
    for d in dirs:
        if d == "__MACOSX":
            macosx_path = os.path.join(root, d)
            for sub_root, sub_dirs, sub_files in os.walk(macosx_path, topdown=False):
                for sub_file in sub_files:
                    os.remove(os.path.join(sub_root, sub_file))
                for sub_dir in sub_dirs:
                    os.rmdir(os.path.join(sub_root, sub_dir))
            if os.path.isdir(macosx_path):
                os.rmdir(macosx_path)

    for file in files:
        if not file.lower().endswith(".csv"):
            os.remove(os.path.join(root, file))

    if root != OUTPUT_DIR and not os.listdir(root):
        os.rmdir(root)

print("✅ Done. All CSVs ready.")