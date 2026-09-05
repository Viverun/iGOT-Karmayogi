"""One-time backfill: fetch all roadmap lecture transcripts (residential IP)
and index them into the Pinecone 'transcripts' namespace."""
import json
import roadmap_data
import transcripts as ts
import vector_store

done, failed = [], []
for c in roadmap_data.ROADMAP_COURSES:
    for m in c["modules"]:
        for v in m["videos"]:
            if v.get("playlist"):
                continue
            text = ts.get_transcript(v["yt"], max_chars=10**9)
            if text:
                done.append((c["key"], v["yt"], len(text)))
            else:
                failed.append((c["key"], v["yt"], v["title"]))

print(f"indexed/cached: {len(done)} | no transcript available: {len(failed)}")
for f in failed:
    print("  no transcript:", f[0], f[1], f[2][:60])
