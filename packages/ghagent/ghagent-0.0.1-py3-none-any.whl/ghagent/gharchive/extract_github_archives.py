import os
import gzip
import shutil
import concurrent.futures

from pathlib import Path

INPUT_DIR = Path.joinpath(Path.home(), "data/gharchive")
OUTPUT_DIR = Path.joinpath(Path.home(), "nfs/datasets/github-archives/extracted")

def extract_gz_file(file_path, output_folder):
    """Function to extract a .gz file."""
    # Check if the file has a .gz extension
    if not file_path.endswith('.gz'):
        print(f"Not a .gz file: {file_path}")
        return

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Determine the output file name
    output_file_path = os.path.join(output_folder, os.path.basename(file_path)[:-3])

    # Extract the .gz file
    with gzip.open(file_path, 'rb') as f_in:
        with open(output_file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"Extracted {file_path} to {output_file_path}")

def main():
    # Get a list of all .gz files in the directory
    gz_files = [os.path.join(INPUT_DIR, file) for file in os.listdir(INPUT_DIR) if file.endswith('.gz')]

    # Use ThreadPoolExecutor to concurrently extract .gz files
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(extract_gz_file, gz_files, [OUTPUT_DIR] * len(gz_files))

if __name__ == "__main__":
    main()
