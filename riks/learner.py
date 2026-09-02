"""Progressive individual learner: Elo skill, uncertainty, personal rate, spacing."""

from __future__ import annotations

import math
from datetime import date, datetime

from riks.tracks import current, question_by_id


def _today() -> date:
    return date.today()


def parse_day(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def expected_score(skill: float, item_elo: float) -> float:
    return 1.0 / (1.0 + 10 ** ((item_elo - skill) / 400.0))


def item_elo(question: dict) -> float:
    """Map tagged difficulty + PYQ likelihood onto an Elo-like scale."""
    return (
        820
        + int(question.get("difficulty") or 2) * 170
        + (1.0 - float(question.get("probability") or 0.7)) * 90
        + float(question.get("marks") or 2) * 12
    )


def skill_to_mastery(skill: float) -> float:
    """800 → ~28, 1000 → 50, 1200 → 72, 1400 → 88."""
    return round(100.0 * sigmoid((skill - 1000.0) / 160.0), 1)


def seed_skill(student: dict, topic: dict) -> float:
    strong = set(student.get("strong_subjects") or [])
    weak = set(student.get("weak_subjects") or [])
    if topic["subject_id"] in strong:
        base = 1120.0
    elif topic["subject_id"] in weak:
        base = 880.0
    else:
        base = 1000.0
    if topic.get("ncert_priority") == "optional":
        base += 40
    return base


def empty_node(skill: float) -> dict:
    return {
        "skill": round(skill, 1),
        "uncertainty": 280.0,
        "learning_rate": 1.0,
        "stability_days": 2.5,
        "attempts": 0,
        "recent": [],
        "last_practice": None,
        "residuals": [],
    }


def init_learner(student: dict) -> dict:
    topics = {t["id"]: empty_node(seed_skill(student, t)) for t in current().TOPICS}
    return {
        "topics": topics,
        "pace": 1.0,
        "days_complete": 0,
        "days_missed": 0,
        "mean_accuracy": None,
    }


def effective_skill(node: dict, today: date | None = None) -> float:
    """Skill decays if this student has not revisited the topic within their own stability."""
    today = today or _today()
    skill = float(node.get("skill") or 1000)
    last = parse_day(node.get("last_practice"))
    if not last:
        return skill
    stability = max(1.2, float(node.get("stability_days") or 2.5))
    days = max(0, (today - last).days)
    # Individual forgetting: unstable skills decay faster.
    unc = float(node.get("uncertainty") or 200)
    decay = 28.0 * math.log1p(days / stability) * (0.6 + unc / 500.0)
    return max(500.0, skill - decay)


def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def apply_attempt(node: dict, actual: float, opp: float, when: str) -> dict:
    """One Elo step, then fine-tune this student's learning rate and spacing."""
    skill = float(node["skill"])
    unc = float(node["uncertainty"])
    lr = float(node["learning_rate"])
    exp = expected_score(skill, opp)
    # High uncertainty → bigger steps; many attempts → fine-tune (smaller K).
    k = 52.0 * lr * _clamp(unc / 220.0, 0.35, 1.6)
    delta = k * (actual - exp)
    skill = _clamp(skill + delta, 500.0, 2100.0)
    unc = _clamp(unc * 0.90, 70.0, 320.0)

    residuals = list(node.get("residuals") or [])
    residuals.append(round(actual - exp, 3))
    residuals = residuals[-12:]
    # Consistently beating expectation → this topic clicks for them; raise rate.
    if len(residuals) >= 4:
        mean_r = sum(residuals) / len(residuals)
        if mean_r > 0.12:
            lr = _clamp(lr * 1.06, 0.45, 1.85)
        elif mean_r < -0.12:
            lr = _clamp(lr * 0.94, 0.45, 1.85)

    recent = list(node.get("recent") or [])
    recent.append(1 if actual >= 0.6 else 0)
    recent = recent[-8:]
    acc = sum(recent) / len(recent)
    stability = float(node.get("stability_days") or 2.5)
    if actual >= 0.6:
        stability = _clamp(stability * (1.15 if acc >= 0.75 else 1.05), 1.5, 18.0)
    else:
        stability = _clamp(stability * 0.82, 1.5, 18.0)

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


def sync_learner(student: dict, evaluations: list[dict]) -> dict:
    """Replay this student's papers so the model is always theirs, not a class average."""
    learner = init_learner(student)
    # Stable order: date then kind (periodic after daily on the same day).
    ordered = sorted(evaluations or [], key=lambda e: (e.get("date") or "", e.get("kind") or ""))
    for ev in ordered:
        when = ev.get("date") or _today().isoformat()
        for item in ev.get("items") or []:
            tid = item.get("topic_id")
            if tid not in learner["topics"]:
                continue
            marks = float(item.get("marks") or 0) or 1.0
            actual = _clamp(float(item.get("marks_awarded") or 0) / marks, 0.0, 1.0)
            qid = item.get("question_id")
            if qid:
                try:
                    opp = item_elo(question_by_id(qid))
                except StopIteration:
                    opp = 1000 + (0 if item.get("correct") else 80)
            else:
                opp = 1080.0
            apply_attempt(learner["topics"][tid], actual, opp, when)
    learner["mean_accuracy"] = _global_accuracy(learner)
    student["learner"] = learner
    return learner


def _global_accuracy(learner: dict) -> float | None:
    bits = []
    for node in learner["topics"].values():
        bits.extend(node.get("recent") or [])
    if not bits:
        return None
    return round(sum(bits) / len(bits), 3)


def tune_pace(learner: dict, completions: dict | None) -> float:
    """Daily load is personal: shrink after misses, grow after a clean streak."""
    pace = 1.0
    missed = 0
    done = 0
    if completions:
        for row in completions.values():
            if row.get("completed"):
                done += 1
            else:
                missed += 1
        if missed and missed >= done:
            pace *= 0.82
        elif done >= 3 and missed == 0:
            pace *= 1.12
    acc = learner.get("mean_accuracy")
    if acc is not None and acc < 0.4:
        pace *= 0.9  # struggling: shorter list, easier items — not more volume
    if acc is not None and acc > 0.8 and done >= 2:
        pace *= 1.08
    learner["pace"] = round(_clamp(pace, 0.6, 1.35), 3)
    learner["days_complete"] = done
    learner["days_missed"] = missed
    return learner["pace"]


def is_unlocked(topic_id: str, learner: dict, today: date | None = None) -> bool:
    for pre in current().PREREQS.get(topic_id, []):
        node = learner["topics"].get(pre)
        if not node:
            return False
        skill = effective_skill(node, today)
        attempts = int(node.get("attempts") or 0)
        if skill < 1040 and attempts < 2:
            return False
        if skill < 1000:
            return False
    return True


def zpd_target(node: dict) -> float:
    """Zone of proximal development: ~70% success, shifted if this student is stuck or flying."""
    recent = node.get("recent") or []
    if len(recent) >= 3:
        acc = sum(recent) / len(recent)
        if acc < 0.4:
            return 0.80  # easier until they can stand
        if acc > 0.85:
            return 0.58  # step up
    return 0.70


def topic_urgency(topic: dict, node: dict, target_mastery: float, today: date | None = None) -> float:
    today = today or _today()
    skill = effective_skill(node, today)
    mastery = skill_to_mastery(skill)
    gap = max(0.0, target_mastery - mastery) / 100.0
    leak = topic["marks_weight"] * (1 - mastery / 100.0)
    last = parse_day(node.get("last_practice"))
    stability = float(node.get("stability_days") or 2.5)
    overdue = 0.0
    if last:
        overdue = max(0.0, (today - last).days / stability)
    elif int(node.get("attempts") or 0) == 0:
        overdue = 0.6
    # Slow personal learning rate → more time on this topic, not less.
    lr = float(node.get("learning_rate") or 1.0)
    stuck = 1.0
    recent = node.get("recent") or []
    if len(recent) >= 3 and sum(recent) / len(recent) < 0.4:
        stuck = 1.35
    conf = 1.0 + float(node.get("uncertainty") or 200) / 400.0
    return leak * topic["probability"] * (0.3 + gap) * (1 + 0.55 * overdue) * (1.15 / lr) * stuck * conf


def insights(student: dict, learner: dict) -> list[str]:
    """Human lines that show the course is *theirs*."""
    lines = []
    pace = float(learner.get("pace") or 1.0)
    if pace < 0.92:
        lines.append(f"Today’s block is shortened ({int(pace*100)}% load) because recent days were missed or scores were low — fewer, better-fit questions.")
    elif pace > 1.08:
        lines.append(f"Load is raised ({int(pace*100)}%) — you have been finishing the list and converting practice into skill.")
    ranked = []
    for t in current().TOPICS:
        node = learner["topics"][t["id"]]
        if int(node.get("attempts") or 0) >= 2:
            ranked.append((float(node["learning_rate"]), t, node))
    if ranked:
        ranked.sort(key=lambda x: x[0], reverse=True)
        fast_lr, fast_t, _ = ranked[0]
        slow_lr, slow_t, slow_n = ranked[-1]
        if fast_lr >= 1.08:
            lines.append(f"{fast_t['chapter']} clicks for you (personal rate {fast_lr:.2f}) — we step difficulty there instead of repeating easy items.")
        if slow_lr <= 0.92 and int(slow_n.get("attempts") or 0) >= 3:
            lines.append(f"{slow_t['chapter']} is slow for you specifically (rate {slow_lr:.2f}) — more time, easier items, no unlock of what sits on top of it yet.")
    locked = [t["chapter"] for t in current().TOPICS if not is_unlocked(t["id"], learner)]
    if locked:
        lines.append("Held back until the foundation is yours: " + ", ".join(locked[:3]) + ".")
    acc = learner.get("mean_accuracy")
    if acc is not None:
        lines.append(f"Questions are aimed at ~{int(100* (0.70 if 0.4 <= acc <= 0.85 else (0.80 if acc < 0.4 else 0.58)))}% success for your current skill — not the class average.")
    return lines[:5]
