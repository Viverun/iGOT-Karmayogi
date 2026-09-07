"""YouTube transcript fetching + caching for transcript-grounded module quizzes.

Set TRANSCRIPT_PROXY (e.g. http://user:pass@host:port) in the environment to
route YouTube requests through a proxy — needed on cloud hosts whose IPs are
blocked by YouTube. Transcripts are indexed into Pinecone on first fetch, so
the proxy is only needed once per video."""
import os

from db import get_db


def _proxy_config():
    """Optional egress proxy for YouTube (cloud IPs are often blocked).
    Set TRANSCRIPT_PROXY in the environment, e.g. http://user:pass@host:port."""
    proxy_url = os.environ.get("TRANSCRIPT_PROXY")
    if not proxy_url:
        return None
    from youtube_transcript_api.proxies import GenericProxyConfig
    return GenericProxyConfig(http_url=proxy_url, https_url=proxy_url)


def _fetch_via_supadata(video_id: str) -> str | None:
    """Transcript-API service (works from any cloud host; SUPADATA_API_KEY env)."""
    key = os.environ.get("SUPADATA_API_KEY")
    if not key:
        return None
    try:
        import httpx
        r = httpx.get("https://api.supadata.ai/v1/youtube/transcript",
                      params={"videoId": video_id},
                      headers={"x-api-key": key}, timeout=60)
        if r.status_code != 200:
            print(f"supadata {video_id}: HTTP {r.status_code}")
            return None
        d = r.json()
        content = d.get("content")
        if isinstance(content, list):  # timestamped chunks -> plain text
            content = " ".join(c.get("text", "") if isinstance(c, dict) else str(c) for c in content)
        return (content or "").strip() or None
    except Exception as e:
        print(f"supadata {video_id} failed:", e)
        return None


def _yt_api():
    """Transcript API client with a hard 45s HTTP timeout (proxies can hang)."""
    import requests
    from youtube_transcript_api import YouTubeTranscriptApi

    class _TimeoutSession(requests.Session):
        def request(self, *a, **kw):
            kw.setdefault("timeout", 45)
            return super().request(*a, **kw)

    return YouTubeTranscriptApi(proxy_config=_proxy_config(), http_client=_TimeoutSession())


def _fetch_video(video_id: str) -> str | None:
    # 1. direct fetch (works locally / with TRANSCRIPT_PROXY)
    try:
        api = _yt_api()
        try:
            t = api.fetch(video_id, languages=["en"])
        except Exception:
            t = api.fetch(video_id)  # any available language / auto-generated
        return " ".join(s.text.replace("\n", " ") for s in t)
    except Exception:
        pass
    # 2. transcript API service (works from Render/cloud)
    return _fetch_via_supadata(video_id)


def _index_to_vector_db(video_id: str, text: str) -> bool:
    """One-time: embed + index a transcript into the vector DB so quiz
    generation everywhere retrieves from Pinecone instead of re-fetching."""
    try:
        import vector_store
        from materials import chunk_text
        chunks = [c for c in chunk_text(text) if len(c.strip()) > 80]
        if chunks:
            n = vector_store.index_transcript(video_id, chunks)
            print(f"transcript {video_id} indexed into Pinecone ({n} chunks)")
            return True
    except Exception as e:
        print(f"transcript {video_id} vector indexing skipped:", e)
    return False


def get_transcript(video_id: str, max_chars: int = 24000) -> str:
    """Cached transcript text for one video (head of the transcript).
    Newly fetched AND previously-cached-but-unindexed transcripts get
    indexed into the vector DB exactly once, at fetch/access time."""
    conn = get_db()
    row = conn.execute("SELECT text, indexed FROM transcripts WHERE video_id=?", (video_id,)).fetchone()
    conn.close()
    if row:
        if not row["indexed"]:
            if _index_to_vector_db(video_id, row["text"]):
                conn = get_db()
                conn.execute("UPDATE transcripts SET indexed=1 WHERE video_id=?", (video_id,))
                conn.commit(); conn.close()
        return row["text"][:max_chars]
    text = _fetch_video(video_id)
    if not text:
        return ""
    conn = get_db()
    conn.execute("INSERT INTO transcripts (video_id, text, chars, indexed) VALUES (?,?,?,?) "
                 "ON CONFLICT (video_id) DO UPDATE SET text=excluded.text, chars=excluded.chars, "
                 "indexed=excluded.indexed, fetched_at=NOW()::text",
                 (video_id, text, len(text), 0))
    conn.commit()
    conn.close()
    if _index_to_vector_db(video_id, text):
        conn = get_db()
        conn.execute("UPDATE transcripts SET indexed=1 WHERE video_id=?", (video_id,))
        conn.commit(); conn.close()
    return text[:max_chars]


def module_context(videos: list, per_video: int = 16000, total: int = 55000) -> tuple[str, list]:
    """Transcript context for a module's videos. Returns (context_text, fetched_ids)."""
    parts, fetched, used = [], [], 0
    for v in videos:
        if v.get("playlist"):
            continue
        text = get_transcript(v["yt"], max_chars=per_video)
        if not text:
            continue
        fetched.append(v["yt"])
        budget = max(2000, total - used)
        parts.append(f"[Video: {v['title']}]\n{text[:budget]}")
        used += min(len(text), budget)
        if used >= total:
            break
    return "\n\n---\n\n".join(parts), fetched
