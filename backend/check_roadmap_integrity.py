"""CI guard against the "wrong course plays wrong video" class of bug.

A single (non-playlist) YouTube video ID appearing under two courses whose
competency areas don't overlap almost certainly means one course's video list
was copy-pasted from another as a placeholder and never swapped out — e.g. a
Banking course silently playing a GIS lecture. Playlist IDs are exempt: a
generic resource (like an NPTEL Python playlist) is legitimately reused
across departments. Run as part of CI's backend import check.
"""
import sys

import roadmap_data as rd


def find_cross_topic_collisions() -> list[str]:
    by_video: dict[str, list[tuple[str, frozenset]]] = {}
    for c in rd.ROADMAP_COURSES:
        areas = frozenset(c["areas"])
        for m in c["modules"]:
            for v in m["videos"]:
                if v.get("playlist"):
                    continue
                by_video.setdefault(v["yt"], []).append((c["key"], areas))

    problems = []
    for yt, uses in by_video.items():
        keys = {k for k, _ in uses}
        if len(keys) < 2:
            continue
        all_areas = [a for _, a in uses]
        if not any(all_areas[0] & other for other in all_areas[1:]):
            problems.append(f"video {yt} reused across unrelated courses {sorted(keys)} "
                             f"with no shared competency area")
    return problems


if __name__ == "__main__":
    issues = find_cross_topic_collisions()
    if issues:
        print("Roadmap integrity check FAILED:")
        for i in issues:
            print(" -", i)
        sys.exit(1)
    print(f"Roadmap integrity check OK — {len(rd.ROADMAP_COURSES)} courses, no cross-topic video reuse")
