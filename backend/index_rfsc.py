"""Patient resumable indexer for the large freeCodeCamp transcript."""
import sqlite3, time
import vector_store
from materials import chunk_text

DB = "igot.db"
c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
text = c.execute("SELECT text FROM transcripts WHERE video_id='rfscVS0vtbw'").fetchone()[0]
chunks = [x for x in chunk_text(text) if len(x.strip()) > 80]
print("total chunks:", len(chunks), flush=True)

# resume: find how many chunks already uploaded by querying Pinecone ids
import vector_store as vs
idx = vs.get_index()
already = 0
try:
    res = idx.fetch(ids=[f"vidrfscVS0vtbw_c{i}" for i in range(len(chunks))], namespace="transcripts")
    already = len([v for v in res["vectors"].values() if v])
except Exception as e:
    print("resume check failed:", e)
print("already uploaded:", already, flush=True)

BATCH = 8
i = already
while i < len(chunks):
    batch = chunks[i:i + BATCH]
    for attempt in range(20):
        try:
            embeddings = vs.embed(batch)
            vectors = [{"id": f"vidrfscVS0vtbw_c{i + j}", "values": emb,
                        "metadata": {"video_id": "rfscVS0vtbw", "chunk_no": i + j, "text": t[:4000]}}
                       for j, (t, emb) in enumerate(zip(batch, embeddings))]
            vs.upsert_chunks("transcripts", vectors)
            break
        except Exception as e:
            wait = 45
            print(f"batch {i} attempt {attempt + 1} failed: {str(e)[:80]} — waiting {wait}s", flush=True)
            time.sleep(wait)
    else:
        print("giving up at batch", i, flush=True); break
    print(f"uploaded chunks {i}-{i + len(batch) - 1}", flush=True)
    i += len(batch)
    time.sleep(45)  # stay under the per-minute quota

if i >= len(chunks):
    c.execute("UPDATE transcripts SET indexed=1 WHERE video_id='rfscVS0vtbw'")
    c.commit()
    print("ALL INDEXED", flush=True)
