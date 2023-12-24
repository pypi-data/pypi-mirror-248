import os
import gzip
import requests
import duckdb
import shutil
from pathlib import Path
from tqdm import tqdm
from datetime import datetime, timedelta

def download_github(date: str, output_dir: str):
    urls = [f"https://data.gharchive.org/{date}-{hour}.json.gz" for hour in range(0, 24)]
    download_dir = Path.joinpath(output_dir, "download", date)
    os.makedirs(download_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    # step 1: download the file form gharchive
    for url in urls:
        print(f"Downloading {url}")
        filename = Path.joinpath(download_dir, url.split("/")[-1])
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
    # step 2: unzip the file to download_dir
    for file in download_dir.glob("*.gz"):
        print(f"Extracting file {file.name}")
        output_file_path = Path.joinpath(download_dir, file.name[:-3])
        with gzip.open(file, 'rb') as f_in:
            with open(output_file_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    # step 3: aggregate the file to archive_dir as a single date.parquet
    print(f"Aggregating json files to {date}.parquet")
    parquet_file = Path.joinpath(output_dir, f"{date}.parquet")
    query = f"COPY (SELECT * FROM read_json_auto('{download_dir}/*.json', ignore_errors=true)) TO '{parquet_file}';"
    try:
        duckdb.sql(query)
    except Exception as e:
        print(f"Error aggregating json files: {e}")
        print(f"Query: {query}")
    # step 4: delete the download_dir
    for file_path in download_dir.glob('*'):
        try:
            if file_path.is_file():
                print(f"Deleting file {file_path}")
                file_path.unlink()
        except Exception as e:
            print(f"Error deleting file: {e}")
    download_dir.rmdir()

def gen_date_list(start_date: str, end_date: str):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    date_list = []

    while start_date <= end_date:
        date_list.append(end_date.strftime('%Y-%m-%d'))
        end_date -= timedelta(days=1)
    return date_list

OUTPUT_DIR = Path.joinpath(Path.home(), "/datasets/github-events")
date_list = gen_date_list("2022-01-01", "2022-05-13")

for date in tqdm(date_list):
    print("Fetching date: ", date)
    download_github(date, OUTPUT_DIR)
