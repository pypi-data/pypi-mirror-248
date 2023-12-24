#%%
import csv
import sys
from pathlib import Path
from tqdm import tqdm

csv.field_size_limit(sys.maxsize)

CSV_DIR = Path.joinpath(Path.home(), "data/github_archive_analytics/repo_info/")
OUTPUT_FILE = Path.joinpath(Path.home(), "data/github_archive_analytics/unique_repos.csv")
user_logins = set()
csv_files = list(CSV_DIR.glob("*.csv"))

with open(OUTPUT_FILE, "w") as f_out:
    writer = csv.writer(f_out)
    for file in tqdm(csv_files):
        with open(file, "r") as f_in:
            reader = csv.reader(f_in)
            for row in reader:
                if row[0] in user_logins:
                    continue
                user_logins.add(row[0])
                writer.writerow(row)
