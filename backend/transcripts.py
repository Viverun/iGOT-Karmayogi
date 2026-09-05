"""YouTube transcript fetching + caching for transcript-grounded module quizzes."""
from db import get_db


def _fetch_video(video_id: str) -> str | None:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        try:
            t = api.fetch(video_id, languages=["en"])
        except Exception:
            t = api.fetch(video_id)  # any available language / auto-generated
        return " ".join(s.text.replace("\n", " ") for s in t)
    except Exception:
        return None


def get_transcript(video_id: str, max_chars: int = 24000) -> str:
    """Cached transcript text for one video (head of the transcript)."""
    conn = get_db()
    row = conn.execute("SELECT text FROM transcripts WHERE video_id=?", (video_id,)).fetchone()
    conn.close()
    if row:
        return row["text"][:max_chars]
    text = _fetch_video(video_id)
    if not text:
        return ""
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO transcripts (video_id, text, chars) VALUES (?,?,?)",
                 (video_id, text, len(text)))
    conn.commit()
    conn.close()
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
