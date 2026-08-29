"""Time-to-contest clock and whether progress is keeping up with that clock."""

from __future__ import annotations

from datetime import date, datetime

MODES = {
    "build": {
        "label": "Build",
        "blurb": "Enough runway. Keep foundations unlocking; do not skip high-yield modules yet.",
        "paper": 6,
        "focus": 3,
        "leave_leak": 0.8,
        "pace_boost": 1.0,
        "drop_low_p": 0.45,
    },
    "steady": {
        "label": "Steady",
        "blurb": "Normal pace. High-yield first; modules well above this rating can wait.",
        "paper": 6,
        "focus": 2,
        "leave_leak": 1.2,
        "pace_boost": 1.0,
        "drop_low_p": 0.55,
    },
    "tighten": {
        "label": "Tighten",
        "blurb": "Under three weeks. Drop modules above this rating; only leaky, likely topics stay.",
        "paper": 5,
        "focus": 2,
        "leave_leak": 1.8,
        "pace_boost": 1.08,
        "drop_low_p": 0.70,
    },
    "sprint": {
        "label": "Sprint",
        "blurb": "Contest week. Only must-do modules for this rating. No new unlocks.",
        "paper": 4,
        "focus": 2,
        "leave_leak": 2.4,
        "pace_boost": 1.12,
        "drop_low_p": 0.80,
    },
}


def _as_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def exam_clock(
    exam_date: str,
    started_at: str | None = None,
    today: date | None = None,
    event: str = "contest",
) -> dict:
    today = today or date.today()
    exam = _as_date(exam_date) or today
    start = _as_date(started_at)
    if start is None or start >= exam:
        start = today if exam == today else min(today, exam)
        if start >= exam:
            start = exam
    remaining = max(0, (exam - today).days)
    elapsed = max(0, (today - start).days)
    span = max(1, (exam - start).days)
    left_pct = round(100.0 * remaining / span, 1)
    used_pct = round(100.0 - left_pct, 1)
    weeks, days = divmod(remaining, 7)
    if remaining <= 7:
        mode = "sprint"
    elif remaining <= 21:
        mode = "tighten"
    elif remaining <= 60:
        mode = "steady"
    else:
        mode = "build"
    noun = "Contest" if event == "contest" else "Exam"
    return {
        "exam_date": exam.isoformat(),
        "remaining_days": remaining,
        "remaining_hours": remaining * 24,
        "weeks": weeks,
        "week_days": days,
        "elapsed_days": elapsed,
        "span_days": span,
        "time_left_pct": left_pct,
        "time_used_pct": used_pct,
        "mode": mode,
        "mode_meta": MODES[mode],
        "event": event,
        "headline": (
            f"{noun} today"
            if remaining == 0
            else f"{remaining} day{'s' if remaining != 1 else ''} · {weeks}w {days}d"
        ),
        "until": exam.strftime("%d %b %Y"),
    }


def progress_against_clock(overall: float, target: float, clock: dict, rows: list[dict]) -> dict:
    remaining = max(1, clock["remaining_days"])
    gap = round(target - overall, 1)
    need_per_day = round(max(0.0, gap) / remaining, 2)
    unit = "rating" if target > 200 else "points"
    must = [r for r in rows if r.get("need_for", 0) <= target] or rows
    must_mastery = sum(r["mastery"] for r in must) / max(1, len(must))
    work_left = max(0.0, 1.0 - (must_mastery / 70.0))
    time_left = clock["time_left_pct"] / 100.0
    lag = round(work_left - time_left, 2)
    elapsed = int(clock.get("elapsed_days") or 0)
    if gap <= 0:
        status, status_line = "ahead", "You are already at or above the target. Protect it with light review."
    elif elapsed <= 2 and clock["remaining_days"] > 7:
        status, status_line = "on_track", (
            f"Clock is running: {clock['remaining_days']} days left to close {gap} {unit} "
            f"(~{need_per_day} per day). Must-do mastery is {must_mastery:.0f}% — finish today’s named set."
        )
    elif lag > 0.12:
        status, status_line = "behind", (
            f"Behind the clock: {clock['time_used_pct']:.0f}% of the days are gone, "
            f"but must-do modules sit at {must_mastery:.0f}% mastery. "
            f"You still need about {need_per_day} {unit} per day."
        )
    elif lag < -0.12:
        status, status_line = "ahead", (
            f"Ahead of the clock: {clock['time_left_pct']:.0f}% of the time remains "
            f"and must-do mastery is {must_mastery:.0f}%. Keep the daily minimum; do not add random sheets."
        )
    else:
        status, status_line = "on_track", (
            f"On track for the time left. Close {gap} {unit} in {clock['remaining_days']} days "
            f"(~{need_per_day} per day) by finishing today’s named set."
        )
    return {
        "status": status,
        "status_line": status_line,
        "need_per_day": need_per_day,
        "must_mastery": round(must_mastery, 1),
        "work_left_pct": round(100 * work_left, 1),
        "gap": gap,
        "progress_pct": round(100.0 * overall / max(1.0, target), 1),
        "unit": unit,
    }


def tighten_leave_list(rows: list[dict], clock: dict, target: int) -> list[dict]:
    """As the contest nears, more modules become a conscious skip."""
    mode = clock["mode"]
    leave = [r for r in rows if r.get("can_leave")]
    extra = 100 if mode == "tighten" else (50 if mode == "sprint" else 150)
    for r in rows:
        if r["need_for"] > target + extra:
            leave.append(r)
        elif mode == "sprint" and r["weight"] <= 8 and r["mastery"] >= 45:
            leave.append(r)
        elif mode == "sprint" and not r.get("unlocked", True):
            leave.append(r)
    seen = set()
    out = []
    for r in sorted(leave, key=lambda x: x["leak"]):
        if r["id"] not in seen:
            seen.add(r["id"])
            out.append(r)
    return out[:10]


def horizon_note(clock: dict, progress: dict) -> str:
    m = clock["mode_meta"]
    return f"{clock['headline']} to {clock['until']} — {m['label']}: {m['blurb']} {progress['status_line']}"
