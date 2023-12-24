#%%
import ast
import csv
from pathlib import Path
from tqdm import tqdm

DATA_DIR = Path.joinpath(Path.home(), "data/github_archive_analytics")
USER_INFO_DIR = Path.joinpath(DATA_DIR, "user_info")
USER_INFO_FILE = Path.joinpath(DATA_DIR, "user_info.csv")

key_attributes = ["login", "id", "type", "site_admin", "name", "company", "blog", "location", "email", "hireable", "bio", "twitter_username", "public_repos", "public_gists", "followers", "following", "created_at", "updated_at"]
additional_attributes = ["original_login"]

def aggregate_user_info(prefix=""):
    files = list(USER_INFO_DIR.iterdir())
    if prefix:
        files = [file for file in files if file.name.startswith(prefix)]
    with open(USER_INFO_FILE, "w+") as f:
        writer = csv.writer(f)
        writer.writerow(key_attributes + additional_attributes)
        for file in tqdm(files):
            print("Processing file: ", file.name)
            with open(file, "r") as infile:
                reader = csv.reader(infile)
                for idx, row in enumerate(reader):
                    if idx == 0:
                        continue
                    obj = ast.literal_eval(row[2])
                    new_row = [obj[key] for key in key_attributes]
                    new_row.append(row[0]) # add original login
                    writer.writerow(new_row)

aggregate_user_info()