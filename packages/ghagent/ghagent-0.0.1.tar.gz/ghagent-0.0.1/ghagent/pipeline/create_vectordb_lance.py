#%%
import duckdb
import lancedb
import shutil
import pyarrow as pa
from sentence_transformers import SentenceTransformer

from pathlib import Path
from tqdm import tqdm

REPO_DB_DIR = Path.joinpath(Path.home(), "data/github_archive_analytics/vectordb/repo_info")
REPO_FILE = Path.joinpath(Path.home(), "data/github_archive_analytics/updated_expanded_repo_info.parquet")
BATCH_SIZE = 128
MICRO_BATCH_SIZE = 128 # used for GPU processing
# DEVICE = None
DEVICE = "cuda"

MODEL_NAME="all-MiniLM-L6-v2"
MODEL = SentenceTransformer(MODEL_NAME)
EMBEDDING_SIZE = 384

db = lancedb.connect(REPO_DB_DIR)
con = duckdb.connect()

schema = pa.schema([
    pa.field("id", pa.int64()),
    pa.field("description", pa.utf8()),
    pa.field("name", pa.utf8()),
    pa.field("full_name", pa.utf8()),
    pa.field("description_embedding", pa.list_(pa.float32(), EMBEDDING_SIZE)),
    pa.field("name_embedding", pa.list_(pa.float32(), EMBEDDING_SIZE))
])

repo_count = con.execute(f"select count(*) from '{REPO_FILE}';").fetchone()[0]

def make_batches():
    query = con.execute(f"""select id, name, full_name, description from '{REPO_FILE}';""")
    for batch in tqdm(query.fetch_record_batch(BATCH_SIZE), total=(repo_count // BATCH_SIZE)):
        description_embeddings = MODEL.encode(batch["description"].to_pylist(), batch_size=MICRO_BATCH_SIZE, device=DEVICE)
        description_embeddings = [embedding.tolist() for embedding in description_embeddings]
        name_embeddings = MODEL.encode(batch["name"].to_pylist(), batch_size=MICRO_BATCH_SIZE, device=DEVICE)
        name_embeddings = [embedding.tolist() for embedding in name_embeddings]
        yield pa.RecordBatch.from_arrays(
            [
                pa.array(batch["id"], pa.int64()),
                pa.array(batch["description"]),
                pa.array(batch["name"]),
                pa.array(batch["full_name"]),
                pa.array(description_embeddings, pa.list_(pa.float32(), EMBEDDING_SIZE)),
                pa.array(name_embeddings, pa.list_(pa.float32(), EMBEDDING_SIZE))
            ],
            ["id", "description", "name", "full_name", "description_embedding", "name_embedding"],
        )

shutil.rmtree(REPO_DB_DIR)
db.create_table("repo_info", make_batches(), schema=schema)
con.close()

# %%
