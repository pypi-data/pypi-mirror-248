#%%
import ast
import csv
import sys
from pathlib import Path
from tqdm import tqdm

csv.field_size_limit(sys.maxsize)

DATA_DIR = Path.joinpath(Path.home(), "data/github_archive_analytics")
REPO_INFO_DIR = Path.joinpath(DATA_DIR, "repo_info")
REPO_INFO_FILE = Path.joinpath(DATA_DIR, "aggregated_repo_info.csv")

key_attributes = ["id", "name", "full_name", "private", "description", "fork", "created_at", "updated_at", "pushed_at", "size", "stargazers_count", "watchers_count", "language", "has_issues", "has_projects", "has_downloads", "has_wiki", "has_pages", "has_discussions", "forks_count", "mirror_url", "archived", "disabled", "open_issues_count", "license", "allow_forking", "is_template", "web_commit_signoff_required", "topics", "visibility", "forks", "open_issues", "watchers", "default_branch", "temp_clone_token", "network_count", "subscribers_count"]
additional_attributes = ["owner_login", "owner_id", "permission_admin", "permission_maintain", "permission_push", "permission_triage", "permission_pull"]

def aggregate_repo_info(prefix=""):
    unique_ids = set()
    files = list(REPO_INFO_DIR.iterdir())
    if prefix:
        files = [file for file in files if file.name.startswith(prefix)]
    with open(REPO_INFO_FILE, "w+") as f:
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
                    if obj["id"] in unique_ids:
                        continue
                    unique_ids.add(obj["id"])
                    new_row = [obj[key] for key in key_attributes]
                    new_row.extend([
                        obj["owner"]["login"],
                        obj["owner"]["id"],
                        obj["permissions"]["admin"],
                        obj["permissions"]["maintain"],
                        obj["permissions"]["push"],
                        obj["permissions"]["triage"],
                        obj["permissions"]["pull"]
                    ])
                    writer.writerow(new_row)

# aggregate_repo_info("2023-09-25-14-59-30")
aggregate_repo_info()
