"""Govern the contest journey: target, mastery, schedule, skip impact, daily bot."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from camp.clock import exam_clock, horizon_note, progress_against_clock, tighten_leave_list
from camp.catalog import MODULES, module_by_id
from camp.learner import (
    effective_skill,
    insights,
    is_unlocked,
    skill_to_mastery,
    sync_learner,
    zpd_pick,
)

GOALS = {
    "cf-1200": {"label": "Pupil (1200)", "rating": 1200, "blurb": "Finish Div. 2 A/B reliably."},
    "cf-1400": {"label": "Specialist (1400)", "rating": 1400, "blurb": "Greedy, binary search, first graphs."},
    "cf-1600": {"label": "Expert (1600)", "rating": 1600, "blurb": "DP and shortest paths in contest time."},
    "cf-1900": {"label": "Candidate master (1900)", "rating": 1900, "blurb": "Trees, strings, range queries on the table."},
}

# How much each module matters, and when it is safe to leave.
META = {
    "bootcamp": {"need_for": 800, "ceiling": 1000, "weight": 14, "gain": 80, "color": "#2F5D50"},
    "impl": {"need_for": 800, "ceiling": 1100, "weight": 10, "gain": 70, "color": "#3D6B8A"},
    "math": {"need_for": 1000, "ceiling": 1400, "weight": 10, "gain": 80, "color": "#8A4B2F"},
    "greedy": {"need_for": 1100, "ceiling": 1500, "weight": 14, "gain": 110, "color": "#2F5D50"},
    "search": {"need_for": 1200, "ceiling": 1600, "weight": 12, "gain": 100, "color": "#3D6B8A"},
    "prefix": {"need_for": 1100, "ceiling": 1500, "weight": 8, "gain": 70, "color": "#8A4B2F"},
    "graphs1": {"need_for": 1300, "ceiling": 1700, "weight": 12, "gain": 110, "color": "#2F5D50"},
    "graphs2": {"need_for": 1500, "ceiling": 1900, "weight": 10, "gain": 100, "color": "#3D6B8A"},
    "dp": {"need_for": 1400, "ceiling": 1900, "weight": 14, "gain": 140, "color": "#8A4B2F"},
    "trees-str": {"need_for": 1700, "ceiling": 2100, "weight": 8, "gain": 90, "color": "#2F5D50"},
}


def goal_rating(goal: str) -> int:
    return GOALS.get(goal, GOALS["cf-1400"])["rating"]


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def days_until(when: str, today: date | None = None) -> int:
    today = today or date.today()
    return max(0, (parse_date(when) - today).days)


def module_mastery(module: dict, solved: dict, skipped: dict, weak: list[str], strong: list[str]) -> float:
    ids = [p["id"] for p in module["problems"]]
    if not ids:
        return 40.0
    n_sol = sum(1 for i in ids if i in solved)
    seed = 48.0
    if module["id"] in strong:
        seed = 62.0
    elif module["id"] in weak:
        seed = 32.0
    evidence = 100.0 * n_sol / len(ids)
    w = min(0.85, 0.25 + 0.12 * n_sol)
    return (1 - w) * seed + w * evidence


def classify(state: dict) -> dict:
    learner = sync_learner(state)
    solved = state.get("solved") or {}
    skipped = state.get("skipped") or {}
    target = goal_rating(state.get("goal") or "cf-1400")
    today = date.today()
    rows = []
    for m in MODULES:
        meta = META[m["id"]]
        node = learner["modules"][m["id"]]
        mastery = skill_to_mastery(effective_skill(node, today))
        # Blend in solved fraction so a module with many ticks still shows progress.
        ids = [p["id"] for p in m["problems"]]
        frac = (100.0 * sum(1 for i in ids if i in solved) / len(ids)) if ids else 0
        mastery = round(0.65 * mastery + 0.35 * frac, 1)
        gap = max(0.0, (70 if target >= meta["need_for"] else 40) - mastery) / 100.0
        overdue = 0.0
        last = node.get("last_practice")
        if last:
            from datetime import datetime as _dt

            try:
                last_d = _dt.strptime(last[:10], "%Y-%m-%d").date()
                overdue = max(0.0, (today - last_d).days / max(1.5, float(node.get("stability_days") or 3)))
            except ValueError:
                overdue = 0.0
        lr = float(node.get("learning_rate") or 1.0)
        unlocked = is_unlocked(m["id"], learner)
        prio = (
            meta["weight"]
            * (0.3 + gap)
            * (1.15 if target >= meta["need_for"] else 0.35)
            * (1.15 / lr)
            * (1 + 0.4 * overdue)
        )
        leak = meta["gain"] * (1 - mastery / 100.0) * (1 if target >= meta["need_for"] else 0.2)
        can_leave = (not unlocked) or meta["need_for"] > target + 150 or (mastery >= 55 and meta["ceiling"] < target - 50)
        rows.append(
            {
                **m,
                **meta,
                "mastery": mastery,
                "priority": prio,
                "leak": round(leak, 1),
                "can_leave": can_leave and unlocked,
                "unlocked": unlocked,
                "learning_rate": lr,
                "skill": round(effective_skill(node, today), 0),
            }
        )

    projected = 800 + sum(r["gain"] * (r["mastery"] / 100.0) for r in rows)
    if not solved:
        projected = 800 + sum(r["gain"] * (r["mastery"] / 100.0) * 0.35 for r in rows)
    projected = int(round(min(2400, projected)))
    gap = target - projected
    clock = exam_clock(state.get("contest_date") or "", state.get("started"), event="contest")
    leave = tighten_leave_list(rows, clock, target)
    leave_ids = {r["id"] for r in leave}
    for r in rows:
        r["can_leave"] = r["id"] in leave_ids and r.get("unlocked", True)
    strong = [r for r in rows if r["mastery"] >= 68]
    weak_rows = sorted(
        [r for r in rows if r["unlocked"] and not r["can_leave"]],
        key=lambda r: r["priority"],
        reverse=True,
    )[:5]
    locked = [r for r in rows if not r["unlocked"]]
    progress = progress_against_clock(float(projected), float(target), clock, rows)
    adapted = insights(state, learner)
    adapted.insert(0, horizon_note(clock, progress))
    time_pace = float(clock["mode_meta"]["pace_boost"])
    combined_pace = round(float(learner.get("pace") or 1.0) * time_pace, 3)
    return {
        "rows": rows,
        "strong": strong,
        "weak": weak_rows,
        "can_leave": leave,
        "locked": locked,
        "projected": projected,
        "target": target,
        "gap": gap,
        "goal": GOALS.get(state.get("goal") or "cf-1400", GOALS["cf-1400"]),
        "pace": combined_pace,
        "adapted": adapted,
        "learner": learner,
        "clock": clock,
        "progress": progress,
    }


def impact_of_skipping(tasks: list[dict], classified: dict) -> dict:
    by_id = {r["id"]: r for r in classified["rows"]}
    marks = 0.0
    details = []
    for t in tasks:
        row = by_id.get(t["module_id"])
        if not row:
            continue
        leak = round(row["leak"] * 0.12, 1)
        marks += leak
        details.append(
            {
                "module": row["title"],
                "leak": leak,
                "line": (
                    f"Skipping {t['name']} today leaves ~{leak:.0f} rating points of {row['title']} unsecured "
                    f"(this topic is worth ~{row['gain']} on the way to {classified['target']})."
                ),
            }
        )
    return {"rating_at_risk": round(marks, 1), "details": details}


def build_schedule(state: dict, classified: dict, today: date | None = None, horizon: int = 28) -> list[dict]:
    today = today or date.today()
    contest = state.get("contest_date")
    if contest:
        horizon = min(horizon, max(1, days_until(contest, today) + 1))
    work = [r for r in classified["rows"] if r.get("unlocked") and not r["can_leave"]] or [
        r for r in classified["rows"] if r.get("unlocked")
    ] or classified["rows"]
    work = sorted(work, key=lambda r: r["priority"], reverse=True)
    hours = int(state.get("hours_per_day") or 2)
    minutes = max(60, int(hours * 60 * float(classified.get("pace") or 1.0)))
    start = today - timedelta(days=1)
    learner = classified.get("learner") or sync_learner(state)
    meta = (classified.get("clock") or {}).get("mode_meta") or {"focus": 2, "paper": 6}
    n_focus = int(meta.get("focus") or 2)
    n_pick = max(1, int(meta.get("paper") or 6) // max(1, n_focus))
    days = []
    for i in range(horizon + 1):
        day = start + timedelta(days=i)
        weekend = day.weekday() >= 5
        mins = minutes + (60 if weekend else 0)
        focus = [work[(i + k) % len(work)] for k in range(min(n_focus, len(work)))]
        tasks = []
        for mrow in focus:
            node = learner["modules"][mrow["id"]]
            pick = zpd_pick(mrow, node, state.get("solved") or {}, n=n_pick)
            for p in pick:
                tasks.append(
                    {
                        **p,
                        "module_id": mrow["id"],
                        "module": mrow["title"],
                        "minutes": max(25, mins // max(1, len(focus) * 2)),
                        "reason": (
                            f"{mrow['title']} skill ~{mrow.get('skill', 0):.0f} (your rate {mrow.get('learning_rate', 1):.2f}). "
                            f"Item rating {p.get('rating')} sits near your zone — leak ~{mrow['leak']:.0f} if left cold."
                        ),
                    }
                )
        periodic = None
        if weekend:
            periodic = {"title": "Periodic: sit the round (or a virtual) and upsolve A–C"}
        note = "Contest weekend. Keep the home list short: finish the named problems before the round." if weekend else (
            f"Weekday block: {mins} minutes. Minimum set before sleep — not an extra random sheet."
        )
        days.append(
            {
                "date": day.isoformat(),
                "weekday": day.strftime("%A"),
                "minutes": mins,
                "tasks": tasks[: int(meta.get("paper") or 6)],
                "periodic": periodic,
                "note": note,
            }
        )
    return days


def bot_script(state: dict, classified: dict, today_plan: dict, yesterday: dict | None) -> list[dict]:
    name = (state.get("handle") or "Camper").split()[0]
    remaining = days_until(state["contest_date"]) if state.get("contest_date") else None
    clock = classified.get("clock") or {}
    progress = classified.get("progress") or {}
    gap = classified["gap"]
    if gap > 0:
        gap_text = f"{gap} rating short of target"
    elif gap < 0:
        gap_text = f"{-gap} rating ahead of target"
    else:
        gap_text = "on target"
    msgs = []
    horizon = (
        f"{clock.get('headline', str(remaining) + ' days')} until {clock.get('until', 'the contest')}. "
        f"Mode: {clock.get('mode_meta', {}).get('label', 'Steady')}. "
        if clock
        else (f"{remaining} days to the target contest. " if remaining is not None else "")
    )
    msgs.append(
        {
            "from": "riks",
            "text": (
                f"{name}, {horizon}goal {classified['goal']['label']}. "
                f"Projected ~{classified['projected']} ({gap_text}). "
                f"{progress.get('status_line', 'Here is the minimum set before you sleep.')}"
            ),
        }
    )
    if today_plan:
        lines = [f"• {t['minutes']} min · {t['module']} — {t['name']} ({t['oj']})" for t in today_plan["tasks"]]
        msgs.append({"from": "riks", "text": "Today’s list:\n" + "\n".join(lines)})
        msgs.append(
            {
                "from": "riks",
                "text": (
                    "Sit today’s five-question exam in RIKS (Practice → Daily exam) — we grade MCQs, short answers, and Python. "
                    "Use Codeforces/CSES when you want the live contest interface."
                ),
            }
        )
        if today_plan.get("periodic"):
            msgs.append({"from": "riks", "text": today_plan["periodic"]["title"] + ". Upsolve is the evaluation."})
    if yesterday and not yesterday.get("completed"):
        impact = yesterday.get("impact") or {}
        msgs.append(
            {
                "from": "riks",
                "text": (
                    "Yesterday’s list was not finished. What got in the way — stuck on a topic, "
                    "contest hangover, or too tired to sit? "
                    f"Impact: ~{impact.get('rating_at_risk', yesterday.get('impact_marks', 0))} rating still exposed."
                ),
            }
        )
        for d in impact.get("details", [])[:3]:
            msgs.append({"from": "riks", "text": d["line"]})
    if classified["weak"]:
        w = classified["weak"][0]
        res = (w.get("theory") or [{}])[0]
        msgs.append(
            {
                "from": "riks",
                "text": (
                    f"If you need a second explanation for {w['title']}: {res.get('title', 'USACO Guide')} "
                    f"({res.get('source', '')})."
                ),
            }
        )
    if classified["can_leave"]:
        names = ", ".join(t["title"] for t in classified["can_leave"][:3])
        msgs.append(
            {
                "from": "riks",
                "text": (
                    f"Conscious skip (low marginal impact for this target): {names}. "
                    "Do not grind these unless you raise the goal."
                ),
            }
        )
    if classified.get("adapted"):
        msgs.append({"from": "riks", "text": "Fine-tuned for you:\n• " + "\n• ".join(classified["adapted"])})
    if classified.get("locked"):
        names = ", ".join(t["title"] for t in classified["locked"][:3])
        msgs.append({"from": "riks", "text": f"Not unlocked yet (foundation first): {names}."})
    return msgs


def coach_briefing(state: dict, classified: dict, yesterday: dict | None, today_plan: dict | None) -> dict:
    name = state.get("handle") or "the camper"
    helps = []
    for w in classified["weak"][:3]:
        book = next((t for t in w.get("theory", []) if t.get("source") in {"USACO Guide", "CSES", "CP-Algorithms"}), None)
        if book:
            helps.append(f"Keep {book['title']} open for {w['title']} — leak ~{w['leak']:.0f} rating.")
        else:
            helps.append(f"Sit 25 minutes with {name} on {w['title']} only. Not a random LeetCode dump.")
    helps.append("If sitting time is slipping, protect one block for today’s named problems. RIKS already chose them.")
    helps.append("After a contest, upsolve with the editorial before adding new topics.")
    donts = [
        "Do not scold for a lost rating without reading which topic failed — they may not know where it went wrong.",
        "Do not compare with how you learned to code. This schedule is for this target and this remaining time.",
        "Do not pile extra sheets on a module RIKS marked as safe to leave.",
    ]
    if yesterday and not yesterday.get("completed"):
        donts.append(
            f"Yesterday’s minimum set was unfinished (~{yesterday.get('impact_marks', '?')} rating exposed). Ask why first."
        )
    gap = classified["gap"]
    standing = (
        f"{name} is projected at ~{classified['projected']} against {classified['goal']['label']} "
        f"({gap} short)." if gap > 0 else
        f"{name} is projected at ~{classified['projected']} against {classified['goal']['label']} "
        f"({-gap} ahead)." if gap < 0 else
        f"{name} is on the {classified['goal']['label']} line."
    )
    clock = classified.get("clock") or {}
    progress = classified.get("progress") or {}
    if clock:
        standing += f" {clock.get('headline', '')} until the contest."
    if progress.get("status_line"):
        standing += f" {progress['status_line']}"
    return {"helps": helps[:6], "donts": donts, "standing": standing}
