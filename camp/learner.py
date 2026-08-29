"""Progressive contest learner: per-module Elo, personal rate, unlock gates."""

from __future__ import annotations

import math
from datetime import date, datetime

from camp.catalog import MODULES

PREREQS = {
    "impl": ["bootcamp"],
    "math": ["bootcamp"],
    "greedy": ["impl"],
    "search": ["greedy"],
    "prefix": ["impl"],
    "graphs1": ["impl", "greedy"],
    "graphs2": ["graphs1"],
    "dp": ["greedy", "search"],
    "trees-str": ["graphs1", "dp"],
}


def expected_score(skill: float, item_elo: float) -> float:
    return 1.0 / (1.0 + 10 ** ((item_elo - skill) / 400.0))


def skill_to_mastery(skill: float) -> float:
    return round(100.0 * (1.0 / (1.0 + math.exp(-(skill - 1100.0) / 180.0))), 1)


def parse_day(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def seed_skill(state: dict, mid: str) -> float:
    if mid in (state.get("strong_modules") or []):
        return 1180.0
    if mid in (state.get("weak_modules") or []):
        return 900.0
    return 1020.0


def empty_node(skill: float) -> dict:
    return {
        "skill": round(skill, 1),
        "uncertainty": 260.0,
        "learning_rate": 1.0,
        "stability_days": 3.0,
        "attempts": 0,
        "recent": [],
        "residuals": [],
        "last_practice": None,
    }


def init_learner(state: dict) -> dict:
    return {
        "modules": {m["id"]: empty_node(seed_skill(state, m["id"])) for m in MODULES},
        "pace": 1.0,
    }


def effective_skill(node: dict, today: date | None = None) -> float:
    today = today or date.today()
    skill = float(node.get("skill") or 1000)
    last = parse_day(node.get("last_practice"))
    if not last:
        return skill
    stability = max(1.5, float(node.get("stability_days") or 3))
    days = max(0, (today - last).days)
    unc = float(node.get("uncertainty") or 200)
    decay = 24.0 * math.log1p(days / stability) * (0.55 + unc / 500.0)
    return max(600.0, skill - decay)


def apply_attempt(node: dict, actual: float, opp: float, when: str) -> dict:
    skill = float(node["skill"])
    unc = float(node["uncertainty"])
    lr = float(node["learning_rate"])
    exp = expected_score(skill, opp)
    k = 48.0 * lr * _clamp(unc / 220.0, 0.35, 1.55)
    skill = _clamp(skill + k * (actual - exp), 600.0, 2300.0)
    unc = _clamp(unc * 0.91, 70.0, 300.0)
    residuals = (list(node.get("residuals") or []) + [round(actual - exp, 3)])[-12:]
    if len(residuals) >= 4:
        mean_r = sum(residuals) / len(residuals)
        if mean_r > 0.1:
            lr = _clamp(lr * 1.07, 0.45, 1.85)
        elif mean_r < -0.1:
            lr = _clamp(lr * 0.94, 0.45, 1.85)
    recent = (list(node.get("recent") or []) + [1 if actual >= 0.6 else 0])[-8:]
    acc = sum(recent) / len(recent)
    stability = float(node.get("stability_days") or 3)
    stability = _clamp(stability * (1.12 if actual >= 0.6 and acc >= 0.7 else 0.85 if actual < 0.6 else 1.0), 1.5, 21.0)
    node.update(
        {
            "skill": round(skill, 1),
            "uncertainty": round(unc, 1),
            "learning_rate": round(lr, 3),
            "stability_days": round(stability, 2),
            "attempts": int(node.get("attempts") or 0) + 1,
            "recent": recent,
            "residuals": residuals,
            "last_practice": when[:10],
        }
    )
    return node


def module_of_problem(pid: str) -> str | None:
    for m in MODULES:
        if any(p["id"] == pid for p in m["problems"]):
            return m["id"]
    return None


def problem_elo(pid: str) -> float:
    for m in MODULES:
        for p in m["problems"]:
            if p["id"] == pid:
                return float(p.get("rating") or 1200)
    return 1200.0


def sync_learner(state: dict) -> dict:
    """Replay solves/skips in date order so skill is this camper's, not a ladder average."""
    learner = init_learner(state)
    events = []
    for pid, when in (state.get("solved") or {}).items():
        events.append((when, "oj", pid, 1.0))
    for pid, when in (state.get("skipped") or {}).items():
        events.append((when, "oj", pid, 0.25))
    for ev in state.get("drill_log") or []:
        events.append((ev.get("when") or "", "drill", ev.get("qid"), float(ev.get("score") or 0)))
    events.sort(key=lambda e: e[0] or "")
    for when, kind, pid, actual in events:
        if kind == "drill":
            from camp.drills import drill_by_id

            d = drill_by_id(pid)
            if not d:
                continue
            apply_attempt(learner["modules"][d["module_id"]], actual, float(d.get("rating") or 1100), when)
            continue
        mid = module_of_problem(pid)
        if not mid:
            continue
        apply_attempt(learner["modules"][mid], actual, problem_elo(pid), when)
    # Completions tune pace.
    pace = 1.0
    comps = state.get("completions") or {}
    done = sum(1 for r in comps.values() if r.get("completed"))
    missed = sum(1 for r in comps.values() if not r.get("completed"))
    if missed and missed >= done:
        pace *= 0.84
    elif done >= 3 and missed == 0:
        pace *= 1.12
    learner["pace"] = round(_clamp(pace, 0.6, 1.35), 3)
    state["learner"] = learner
    return learner


def is_unlocked(mid: str, learner: dict) -> bool:
    for pre in PREREQS.get(mid, []):
        node = learner["modules"].get(pre)
        if not node:
            return False
        if effective_skill(node) < 1080 and int(node.get("attempts") or 0) < 3:
            return False
        if effective_skill(node) < 1020:
            return False
    return True


def zpd_pick(module: dict, node: dict, solved: dict, n: int = 2) -> list[dict]:
    skill = effective_skill(node)
    recent = node.get("recent") or []
    acc = sum(recent) / len(recent) if recent else 0.5
    target = 0.80 if acc < 0.4 else 0.58 if acc > 0.85 else 0.70
    open_ps = [p for p in module["problems"] if p["id"] not in solved]
    pool = open_ps or list(module["problems"])
    ranked = sorted(
        pool,
        key=lambda p: abs(expected_score(skill, float(p.get("rating") or 1200)) - target),
    )
    return ranked[:n]


def insights(state: dict, learner: dict) -> list[str]:
    lines = []
    pace = float(learner.get("pace") or 1)
    if pace < 0.92:
        lines.append(f"Today’s list is shorter ({int(pace*100)}% load) because recent days slipped or you marked later.")
    elif pace > 1.08:
        lines.append(f"Load is up ({int(pace*100)}%) — you have been converting solves into skill.")
    ranked = []
    for m in MODULES:
        node = learner["modules"][m["id"]]
        if int(node.get("attempts") or 0) >= 2:
            ranked.append((float(node["learning_rate"]), m, node))
    if ranked:
        ranked.sort(key=lambda x: x[0], reverse=True)
        flr, fm, _ = ranked[0]
        slr, sm, sn = ranked[-1]
        if flr >= 1.08:
            lines.append(f"{fm['title']} clicks for you (rate {flr:.2f}) — next problems there are a step harder.")
        if slr <= 0.92 and int(sn.get("attempts") or 0) >= 3:
            lines.append(f"{sm['title']} is slow for you (rate {slr:.2f}) — we stay on easier tasks and do not unlock what sits on top of it.")
    locked = [m["title"] for m in MODULES if not is_unlocked(m["id"], learner)]
    if locked:
        lines.append("Locked until the foundation is yours: " + ", ".join(locked[:3]) + ".")
    lines.append("Each problem is chosen near a ~70% success chance for your current module skill, then the Elo is updated.")
    return lines[:5]
