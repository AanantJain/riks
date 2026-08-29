"""OpenCamp — fetch free live contest calendars."""

from __future__ import annotations

from datetime import datetime, timezone

import httpx

CF_API = "https://codeforces.com/api/contest.list"
ATCODER_CONTESTS = "https://atcoder.jp/contests/"


def upcoming_codeforces(limit: int = 8) -> list[dict]:
    try:
        r = httpx.get(CF_API, params={"gym": "false"}, timeout=8.0)
        r.raise_for_status()
        payload = r.json()
        if payload.get("status") != "OK":
            return []
        now = datetime.now(timezone.utc).timestamp()
        rows = []
        for c in payload["result"]:
            start = c.get("startTimeSeconds") or 0
            if c.get("phase") in ("BEFORE", "CODING") and start >= now - 6 * 3600:
                rows.append(
                    {
                        "id": c["id"],
                        "name": c["name"],
                        "phase": c["phase"],
                        "start": datetime.fromtimestamp(start, tz=timezone.utc),
                        "url": f"https://codeforces.com/contests/{c['id']}",
                        "duration_min": int((c.get("durationSeconds") or 0) / 60),
                    }
                )
        rows.sort(key=lambda x: x["start"])
        return rows[:limit]
    except Exception:
        return []
