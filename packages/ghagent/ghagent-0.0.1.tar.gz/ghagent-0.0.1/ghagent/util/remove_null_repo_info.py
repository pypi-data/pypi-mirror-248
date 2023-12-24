import duckdb
from pathlib import Path


DATA_DIR = Path.joinpath(Path.home(), "data/github_archive_analytics")
REPO_INFO_FILE = Path.joinpath(DATA_DIR, "expanded_repo_info.parquet")
UPDATED_INFO_FILE = Path.joinpath(DATA_DIR, "updated_expanded_repo_info.parquet")

# Step 2: Connect to DuckDB
conn = duckdb.connect(database=':memory:', read_only=False)

# Step 3: Load Data from Parquet File
conn.execute(f"CREATE TABLE repo_info AS SELECT * FROM parquet_scan('{REPO_INFO_FILE}')")

# Step 4: Update NULL Values
conn.execute(f"UPDATE repo_info SET description = COALESCE(description, '')")

# Step 5: Write Data Back to Parquet
conn.execute(f"COPY repo_info TO '{UPDATED_INFO_FILE}' (FORMAT 'PARQUET')")

# Step 6: Close the Connection
conn.close()
