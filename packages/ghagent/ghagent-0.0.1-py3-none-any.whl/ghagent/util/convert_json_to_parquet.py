#%%
import csv
import duckdb
from pathlib import Path
from tqdm import tqdm

GITHUB_EVENTS_NFS_DIR = Path.joinpath(Path.home(), "nfs/datasets/github-events")
JSON_DIR = Path.joinpath(Path.home(), "nfs/datasets/github-archives-json")
S3_ENDPOINT = "192.168.1.3:9000"

def aggregate_json_to_s3_parquet(con, date: str):
    parquet_file = f"s3://github-archives/{date}.parquet"
    print(f"Processing {date} to {parquet_file}")
    query = f"""
COPY (SELECT * FROM read_json_auto('{JSON_DIR}/{date}-*.json', ignore_errors=true)) TO '{parquet_file}';""".strip()
    con.execute(query)

def get_all_dates():
    all_dates = set()
    for file in JSON_DIR.glob("*"):
        if file.is_file():
            all_dates.add(file.name[:10])
    return list(all_dates)

def process_s3():
    con = duckdb.connect()
    con.execute(f"""
INSTALL httpfs;
LOAD httpfs;
SET s3_endpoint='{S3_ENDPOINT}';
SET s3_url_style='path';
SET s3_use_ssl=false;""".strip())
    for date in tqdm(get_all_dates()):
        aggregate_json_to_s3_parquet(con, date)
    con.close()

def aggregate_json_to_nfs_parquet(con, date: str):
    parquet_file =  Path.joinpath(GITHUB_EVENTS_NFS_DIR, f"{date}.parquet")
    print(f"Processing {date} to {parquet_file}")
    query = f"""
COPY (SELECT * FROM read_json_auto('{JSON_DIR}/{date}-*.json', ignore_errors=true)) TO '{parquet_file}';""".strip()
    con.execute(query)

def process_nfs():
    con = duckdb.connect()
    for date in tqdm(get_all_dates()):
        aggregate_json_to_nfs_parquet(con, date)
    con.close()

process_nfs()
# %%