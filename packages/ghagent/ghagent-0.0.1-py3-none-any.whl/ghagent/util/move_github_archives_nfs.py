#%%
import shutil
from pathlib import Path
from tqdm import tqdm

GITHUB_ARCHIVE_PATH = Path.joinpath(Path.home(), 'data/gharchive')
GITHUB_ARCHIVE_NFS_DIR = Path.joinpath(Path.home(), 'nfs/datasets/gharchive')

all_files = [file for file in GITHUB_ARCHIVE_PATH.iterdir() if file.suffix == '.gz']

for file in tqdm(all_files):
    shutil.move(file, GITHUB_ARCHIVE_NFS_DIR)
