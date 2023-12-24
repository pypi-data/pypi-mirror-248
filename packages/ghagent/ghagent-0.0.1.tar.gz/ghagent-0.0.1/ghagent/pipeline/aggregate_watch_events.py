#%%
import csv
from pathlib import Path
from tqdm import tqdm

DATA_DIR = Path.joinpath(Path.home(), "data/github_archive_analytics")
WATCH_EVENTS_DIR = Path.joinpath(DATA_DIR, "watch_events")
WATCH_EVENTS_FILE = Path.joinpath(DATA_DIR, "watch_events.csv")

KEY_ATTRIBUTES = ["stargazer_login", "stargazer_url", "repo_full_name", "repo_url", "created_at"]
ADDITIONAL_ATTRIBUTES = []

def aggregate_watch_events(prefix=""):
    files = list(WATCH_EVENTS_DIR.iterdir())
    if prefix:
        files = [file for file in files if file.name.startswith(prefix)]
    with open(WATCH_EVENTS_FILE, "w+") as f:
        writer = csv.writer(f)
        writer.writerow(KEY_ATTRIBUTES + ADDITIONAL_ATTRIBUTES)
        for file in tqdm(files):
            with open(file, "r") as infile:
                reader = csv.reader(infile)
                for idx, row in enumerate(reader):
                    if idx == 0:
                        continue
                    writer.writerow(row)

aggregate_watch_events()