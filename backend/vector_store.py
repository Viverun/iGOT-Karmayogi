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
    key, base = get_openai_auth()
    resp = httpx.post(
        f"{base}/embeddings",
        headers={"Authorization": f"Bearer {key}", "content-type": "application/json"},
        json={"model": EMBED_MODEL, "input": texts},
        timeout=60,
    )
    resp.raise_for_status()
    return [d["embedding"] for d in resp.json()["data"]]


def embed(texts: list) -> list:
    if isinstance(texts, str):
        texts = [texts]
    return _embed_azure(texts)


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
