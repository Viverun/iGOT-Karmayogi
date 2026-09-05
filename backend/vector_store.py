"""Vector store layer: Pinecone + Azure OpenAI embeddings (text-embedding-3-small).

Namespaces:
  - "materials"   : chunks of uploaded training material (per-material metadata)
  - "courses"     : course catalogue entries for semantic search

Used for personalized MCQ generation: a user's weakest competency areas are
embedded as a query and the most relevant material chunks are retrieved as
grounding context for the LLM.
"""
import os

import env_config  # noqa: F401  (loads .env)
import httpx
from llm import get_openai_auth

EMBED_MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")
DIM = 1536
INDEX_NAME = os.environ.get("PINECONE_INDEX", "setu-stat")

_client = None
_index = None


def _embed_azure(texts: list) -> list:
    """Embeds in batches — Azure caps the total input per request (~8k tokens)."""
    key, base = get_openai_auth()
    out = []
    BATCH = 16  # ~16 x 1200-char chunks stays well under the token cap
    for i in range(0, len(texts), BATCH):
        batch = texts[i:i + BATCH]
        resp = httpx.post(
            f"{base}/embeddings",
            headers={"Authorization": f"Bearer {key}", "content-type": "application/json"},
            json={"model": EMBED_MODEL, "input": batch},
            timeout=60,
        )
        resp.raise_for_status()
        out.extend(d["embedding"] for d in resp.json()["data"])
    return out


def embed(texts: list) -> list:
    """Embed with retry/backoff for Azure rate limits (429)."""
    import time
    if isinstance(texts, str):
        texts = [texts]
    texts = [t for t in texts if t and t.strip()]  # guard empty inputs
    if not texts:
        return []
    last = None
    for attempt in range(6):
        try:
            return _embed_azure(texts)
        except httpx.HTTPStatusError as e:
            last = e
            if e.response.status_code in (429, 500, 503):
                wait = min(60, 3 * (2 ** attempt))
                print(f"embed rate-limited, retrying in {wait}s (attempt {attempt + 1})")
                time.sleep(wait)
            else:
                raise
    raise last


def get_index():
    global _client, _index
    if _index is not None:
        return _index
    from pinecone import Pinecone, ServerlessSpec
    _client = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    if INDEX_NAME not in _client.list_indexes().names():
        _client.create_index(name=INDEX_NAME, dimension=DIM, metric="cosine",
                             spec=ServerlessSpec(cloud="aws", region="us-east-1"))
    _index = _client.Index(INDEX_NAME)
    return _index


def upsert_chunks(namespace: str, vectors: list):
    """vectors: [{id, values, metadata}]"""
    idx = get_index()
    for i in range(0, len(vectors), 100):
        idx.upsert(vectors=vectors[i:i + 100], namespace=namespace)


def index_material(material_id: int, chunks: list):
    """Embed and store material chunks in the 'materials' namespace."""
    embeddings = embed(chunks)
    vectors = [{
        "id": f"mat{material_id}_c{i}",
        "values": emb,
        "metadata": {"material_id": material_id, "chunk_no": i, "text": c[:4000]},
    } for i, (c, emb) in enumerate(zip(chunks, embeddings))]
    upsert_chunks("materials", vectors)
    return len(vectors)


def query_similar_chunks(query_text: str, top_k: int = 6, material_id: int | None = None) -> list:
    """Retrieve the most relevant material chunks for a query (e.g. weak areas)."""
    qvec = embed([query_text])[0]
    idx = get_index()
    flt = {"material_id": {"$eq": material_id}} if material_id else None
    res = idx.query(vector=qvec, top_k=top_k, namespace="materials",
                    filter=flt, include_metadata=True)
    return [{"score": m["score"], "text": m["metadata"]["text"],
             "material_id": m["metadata"]["material_id"]}
            for m in res["matches"]]


def index_courses(courses: list):
    """Embed the course catalogue for semantic search / recommendations."""
    texts = [f"{c['name']}. {c['description']} Provider: {c['provider']}. "
             f"Competencies: {', '.join(c['competencyAreas'])}. Level: {c['level']}."
             for c in courses]
    embeddings = embed(texts)
    vectors = [{
        "id": c["identifier"],
        "values": emb,
        "metadata": {"name": c["name"], "provider": c["provider"],
                     "level": c["level"], "competencyAreas": c["competencyAreas"]},
    } for c, emb in zip(courses, embeddings)]
    upsert_chunks("courses", vectors)
    return len(vectors)


def search_courses(query_text: str, top_k: int = 5) -> list:
    qvec = embed([query_text])[0]
    idx = get_index()
    res = idx.query(vector=qvec, top_k=top_k, namespace="courses", include_metadata=True)
    return [{"id": m["id"], "score": m["score"], **m["metadata"]} for m in res["matches"]]


def index_transcript(video_id: str, chunks: list):
    """Embed and store one lecture's transcript chunks in the 'transcripts' namespace."""
    embeddings = embed(chunks)
    vectors = [{
        "id": f"vid{video_id}_c{i}",
        "values": emb,
        "metadata": {"video_id": video_id, "chunk_no": i, "text": c[:4000]},
    } for i, (c, emb) in enumerate(zip(chunks, embeddings))]
    upsert_chunks("transcripts", vectors)
    return len(vectors)


def query_transcripts(query_text: str, video_ids: list | None = None, top_k: int = 10) -> list:
    """Retrieve transcript chunks, optionally restricted to specific lecture videos."""
    qvec = embed([query_text])[0]
    idx = get_index()
    flt = {"video_id": {"$in": video_ids}} if video_ids else None
    res = idx.query(vector=qvec, top_k=top_k, namespace="transcripts",
                    filter=flt, include_metadata=True)
    return [{"score": m["score"], "video_id": m["metadata"]["video_id"],
             "text": m["metadata"]["text"]} for m in res["matches"]]
