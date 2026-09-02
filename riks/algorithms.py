"""Personalised scheduler, question selector, and test-paper creator."""

from __future__ import annotations

import random
from collections import defaultdict
from datetime import date, datetime, timedelta

from riks.clock import exam_clock, horizon_note, progress_against_clock, tighten_leave_list
from riks.tracks import (
    current,
    current_week,
    questions_for_topic,
    resources_for_topic,
    set_track_context,
    subject_by_id,
    topic_by_id,
)
from riks.learner import (
    effective_skill,
    expected_score,
    insights,
    is_unlocked,
    item_elo,
    skill_to_mastery,
    sync_learner,
    topic_urgency,
    tune_pace,
    zpd_target,
)


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def days_until(exam_date: str, today: date | None = None) -> int:
    today = today or date.today()
    return max(0, (parse_date(exam_date) - today).days)


def topic_attempts(evaluations: list[dict]) -> dict[str, dict]:
    """Per-topic marks scored vs available across all evaluations."""
    stats: dict[str, dict] = defaultdict(lambda: {"correct": 0, "total": 0, "marks": 0, "marks_max": 0})
    for ev in evaluations:
        for item in ev.get("items", []):
            tid = item["topic_id"]
            stats[tid]["correct"] += int(item.get("correct", 0))
            stats[tid]["total"] += 1
            stats[tid]["marks"] += float(item.get("marks_awarded", 0))
            stats[tid]["marks_max"] += float(item.get("marks", 0))
    return stats


def mastery_map(student: dict, evaluations: list[dict]) -> dict[str, float]:
    """0–100 mastery from this student's skill model (forgetting included).

    Unattempted topics stay at 0 — profile seeds still steer the schedule,
    but the board does not pretend papers have already been taken.
    """
    learner = sync_learner(student, evaluations)
    today = date.today()
    out = {}
    for topic in current().TOPICS:
        node = learner["topics"][topic["id"]]
        if int(node.get("attempts") or 0) == 0:
            out[topic["id"]] = 0.0
        else:
            out[topic["id"]] = skill_to_mastery(effective_skill(node, today))
    return out


def topic_priority(topic: dict, mastery: float, target_key: str) -> float:
    gap = max(0.0, TARGET_MASTERY[target_key] - mastery) / 100.0
    # High-yield, likely-to-appear, unfinished topics rise to the top.
    return topic["marks_weight"] * topic["probability"] * (0.25 + gap)


def classify_topics(student: dict, evaluations: list[dict], completions: dict | None = None) -> dict:
    set_track_context(student)
    bundle = current()
    TARGETS = bundle.TARGETS
    TARGET_MASTERY = bundle.TARGET_MASTERY
    TOPICS = bundle.TOPICS
    learner = sync_learner(student, evaluations)
    tune_pace(learner, completions)
    mastery = mastery_map(student, evaluations)
    target_key = student.get("target", "first_division")
    if target_key not in TARGETS:
        target_key = next(iter(TARGETS))
    today = date.today()
    rows = []
    for topic in TOPICS:
        node = learner["topics"][topic["id"]]
        m = mastery[topic["id"]]
        prio = topic_urgency(topic, node, TARGET_MASTERY[target_key], today)
        expected_marks = topic["marks_weight"] * (m / 100.0)
        leak = topic["marks_weight"] - expected_marks
        rows.append(
            {
                **topic,
                "mastery": round(m, 1),
                "priority": prio,
                "expected_marks": expected_marks,
                "leak": leak,
                "skill": round(effective_skill(node, today), 0),
                "learning_rate": node.get("learning_rate"),
                "unlocked": is_unlocked(topic["id"], learner, today),
                "attempts": node.get("attempts") or 0,
            }
        )

    by_subject: dict[str, list] = defaultdict(list)
    for row in rows:
        by_subject[row["subject_id"]].append(row)

    strong, weak, can_leave = [], [], []
    for sid, items in by_subject.items():
        ranked = sorted(items, key=lambda r: r["mastery"], reverse=True)
        strong.extend([r for r in ranked if r["mastery"] >= 68][:3])
        weak.extend(sorted([r for r in items if r["unlocked"]], key=lambda r: r["priority"], reverse=True)[:3])
        # Conscious skip: low weight, decent mastery, low remaining leak.
        for r in items:
            if r["ncert_priority"] == "optional" and r["mastery"] >= 40:
                can_leave.append(r)
            elif r["leak"] < 1.2 and r["mastery"] >= 58 and r["probability"] < 0.72:
                can_leave.append(r)

    # unique can_leave
    seen = set()
    unique_leave = []
    for r in sorted(can_leave, key=lambda x: x["leak"]):
        if r["id"] not in seen:
            seen.add(r["id"])
            unique_leave.append(r)

    projected = {}
    for sid in by_subject:
        items = by_subject[sid]
        theory = sum(i["expected_marks"] for i in items)
        subj = subject_by_id(sid)
        max_m = subj.get("theory_marks", 80) + subj.get("internal_marks", 20)
        if bundle.id == "inicet":
            internal = 0.0
            total = theory
            percent = round(100 * theory / max(max_m, 1), 1)
        else:
            internal = 20 * (sum(i["mastery"] for i in items) / (100 * len(items)))
            total = theory + internal
            percent = round(100 * total / 100.0, 1)
        projected[sid] = {
            "theory": round(theory, 1),
            "internal": round(internal, 1),
            "total": round(total, 1),
            "percent": percent,
            "max_marks": max_m,
        }

    if bundle.id == "inicet":
        total_expected = sum(sum(i["expected_marks"] for i in items) for items in by_subject.values())
        overall = round(100 * total_expected / bundle.projected_max, 1)
    else:
        overall = sum(v["percent"] for v in projected.values()) / max(1, len(projected))
    locked = [r for r in rows if not r["unlocked"]]
    clock = exam_clock(
        student.get("exam_date"),
        student.get("created_at"),
        event="INI-CET" if bundle.id == "inicet" else "exam",
    )
    unique_leave = tighten_leave_list(rows, clock)
    gap = round(TARGETS[target_key]["percent"] - overall, 1)
    progress = progress_against_clock(overall, TARGETS[target_key]["percent"], clock, rows)
    adapted = insights(student, learner)
    adapted.insert(0, horizon_note(clock, progress))
    # Time pressure also scales personal pace (sprint: slightly longer sitting on fewer topics).
    time_pace = float(clock["mode_meta"]["pace_boost"])
    combined_pace = round(float(learner.get("pace") or 1.0) * time_pace, 3)
    return {
        "mastery": mastery,
        "rows": rows,
        "strong": strong,
        "weak": weak,
        "can_leave": unique_leave[:8],
        "locked": locked[:6],
        "projected": projected,
        "overall_percent": round(overall, 1),
        "target_percent": TARGETS[target_key]["percent"],
        "gap": gap,
        "pace": combined_pace,
        "adapted": adapted,
        "learner": learner,
        "clock": clock,
        "progress": progress,
        "track": bundle.id,
        "study_week": current_week(student) if bundle.WEEK_PLAN else None,
        "week_plan": bundle.WEEK_PLAN,
    }


def select_questions(
    topic_ids: list[str],
    count: int,
    prefer_harder: bool = False,
    used: set[str] | None = None,
    learner: dict | None = None,
) -> list[dict]:
    used = used or set()
    QUESTIONS = current().QUESTIONS
    pool = [q for q in QUESTIONS if q["topic_id"] in topic_ids and q["id"] not in used]
    if not pool:
        pool = [q for q in QUESTIONS if q["topic_id"] in topic_ids]
    if not pool:
        pool = list(QUESTIONS)

    def score(q: dict) -> float:
        if learner:
            node = learner["topics"].get(q["topic_id"])
            if node:
                skill = effective_skill(node)
                p_hat = expected_score(skill, item_elo(q))
                target = zpd_target(node)
                return -abs(p_hat - target) * 4.0 + q["probability"] * 0.35 + random.random() * 0.08
        diff = q["difficulty"]
        if prefer_harder:
            return q["probability"] * (0.4 + 0.3 * diff) + random.random() * 0.15
        return q["probability"] * (1.4 - 0.15 * abs(diff - 2)) + random.random() * 0.2

    ranked = sorted(pool, key=score, reverse=True)
    picked = ranked[:count]
    if len(picked) < count:
        extra = [q for q in QUESTIONS if q["id"] not in {p["id"] for p in picked}]
        picked.extend(extra[: count - len(picked)])
    return picked[:count]


def create_test_paper(
    topic_ids: list[str],
    kind: str,
    mastery: dict[str, float] | None = None,
    rng_seed: str | None = None,
    learner: dict | None = None,
    paper_size: int | None = None,
) -> dict:
    """Daily paper sits in this student's ZPD. Periodic is a slightly harder check."""
    rnd = random.Random(rng_seed)
    mastery = mastery or {}
    if kind == "daily":
        n = paper_size or 6
        questions = select_questions(topic_ids, n, learner=learner)
    else:
        questions = select_questions(topic_ids, 8, prefer_harder=True, learner=learner)
        covered = {q["topic_id"] for q in questions}
        for tid in topic_ids:
            if tid not in covered:
                extras = questions_for_topic(tid)
                if extras:
                    questions.append(rnd.choice(extras))
        questions = questions[:8]

    total = sum(q["marks"] for q in questions)
    return {
        "kind": kind,
        "question_ids": [q["id"] for q in questions],
        "questions": questions,
        "total_marks": total,
    }


def _weekday_minutes(student: dict, day: date) -> int:
    coaching = student.get("coaching", {})
    if student.get("track") == "inicet":
        if day.weekday() >= 5:
            return 120 if coaching.get("weekend_institute") else 240
        return 90 if coaching.get("hospital_duty") else 150
    if day.weekday() >= 5:
        if coaching.get("weekend_institute"):
            return 90
        return 180
    return 150


def build_schedule(student: dict, evaluations: list[dict], today: date | None = None, completions: dict | None = None) -> list[dict]:
    set_track_context(student)
    bundle = current()
    today = today or date.today()
    remaining = days_until(student["exam_date"], today)
    if remaining == 0:
        remaining = 1
    horizon = min(remaining, 56 if bundle.WEEK_PLAN else 42)
    start = today - timedelta(days=1)
    classified = classify_topics(student, evaluations, completions)
    learner = classified["learner"]
    mastery = classified["mastery"]
    pace = float(classified.get("pace") or 1.0)
    mode = classified.get("clock", {}).get("mode_meta") or {"focus": 2, "paper": 6}

    ranked = sorted(
        [r for r in classified["rows"] if r["unlocked"]],
        key=lambda r: r["priority"],
        reverse=True,
    )
    if bundle.WEEK_PLAN:
        week = current_week(student, today)

        def week_boost(r):
            tw = r.get("study_week") or 8
            if tw == week:
                return r["priority"] * 2.2
            if tw == week + 1:
                return r["priority"] * 1.4
            if tw < week:
                return r["priority"] * 0.85
            return r["priority"] * 0.65

        ranked = sorted(ranked, key=week_boost, reverse=True)

    leave_ids = {t["id"] for t in classified["can_leave"]}
    work = [r for r in ranked if r["id"] not in leave_ids] or ranked or classified["rows"]
    n_focus = int(mode.get("focus") or 2)

    days = []
    subject_cycle = [s["id"] for s in bundle.SUBJECTS]
    q_cursor = 0
    weight_label = "INI-CET weight" if bundle.id == "inicet" else "Board weight"
    for i in range(horizon + 1):
        day = start + timedelta(days=i)
        minutes = int(_weekday_minutes(student, day) * pace)
        minutes = max(45, minutes)
        focus = [work[(i + k) % len(work)] for k in range(min(n_focus, len(work)))]
        # Personal review: a topic this student is due to forget.
        review = None
        for r in ranked:
            if r["id"] in {f["id"] for f in focus}:
                continue
            node = learner["topics"][r["id"]]
            last = node.get("last_practice")
            if last and (day - date.fromisoformat(last[:10])).days >= float(node.get("stability_days") or 3):
                review = r
                break
        topics_today = focus + ([review] if review else [])
        paper = create_test_paper(
            [t["id"] for t in topics_today],
            "daily",
            mastery,
            rng_seed=f"{student['id']}-{day.isoformat()}-{q_cursor}",
            learner=learner,
            paper_size=int(mode.get("paper") or 6),
        )
        q_cursor += 1

        tasks = []
        mins_left = minutes
        for t in topics_today:
            slice_m = max(25, mins_left // max(1, len(topics_today)))
            leak = round(t["marks_weight"] * (1 - mastery[t["id"]] / 100.0), 1)
            tasks.append(
                {
                    "topic_id": t["id"],
                    "chapter": t["chapter"],
                    "subject_id": t["subject_id"],
                    "minutes": slice_m,
                    "reason": (
                        f"{weight_label} ~{t['marks_weight']} Qs, recall chance "
                        f"{int(t['probability'] * 100)}%. Mastery {mastery[t['id']]:.0f}%. "
                        f"Leaving this cold leaks ~{leak} marks."
                    ),
                    "resources": resources_for_topic(t["id"])[:2],
                }
            )
        periodic = None
        week_block = None
        if bundle.WEEK_PLAN:
            week_num = min(8, max(1, current_week(student, day)))
            week_block = next((w for w in bundle.WEEK_PLAN if w["week"] == week_num), None)
        if i > 0 and i % 7 == 6:
            if week_block:
                sid = week_block["subjects"][0]
                periodic = {
                    "subject_id": sid,
                    "subject_name": subject_by_id(sid)["name"],
                    "title": f"Week {week_block['week']} mock — {week_block['mock']}",
                }
            else:
                sid = subject_cycle[(i // 7) % len(subject_cycle)]
                periodic = {
                    "subject_id": sid,
                    "subject_name": subject_by_id(sid)["name"],
                    "title": f"Periodic evaluation — {subject_by_id(sid)['name']}",
                }

        day_note = _day_note(student, day, minutes, week_block)
        days.append(
            {
                "date": day.isoformat(),
                "weekday": day.strftime("%A"),
                "minutes": minutes,
                "tasks": tasks,
                "daily_question_ids": paper["question_ids"],
                "daily_total_marks": paper["total_marks"],
                "periodic": periodic,
                "note": day_note,
                "study_week": week_block["week"] if week_block else None,
                "week_title": week_block["title"] if week_block else None,
            }
        )
    return days


def _day_note(student: dict, day: date, minutes: int, week_block: dict | None = None) -> str:
    coaching = student.get("coaching", {})
    track = student.get("track", "cbse")
    if week_block:
        base = f"Week {week_block['week']}: {week_block['title']}. {week_block['focus']}"
    else:
        base = ""
    if track == "inicet":
        if day.weekday() >= 5 and coaching.get("weekend_institute"):
            return (base + " Weekend test-series day — RIKS keeps home drill to high-yield MCQs only.").strip()
        if coaching.get("hospital_duty"):
            return (base + f" Post-duty block: {minutes} minutes minimum. Clinical subjects first.").strip()
        return (base + f" Study block: {minutes} minutes. Finish MCQs before sleep (+1/−⅓ marking).").strip()
    if day.weekday() >= 5 and coaching.get("weekend_institute"):
        return "Weekend institute day. RIKS keeps the home list short: only the questions you must finish before sleep."
    if coaching.get("private_maths") and day.weekday() in (1, 3):
        return "Private maths coaching day. Use the tutor for today's weak algebra/trig item; RIKS will still check the drill."
    return f"School day. Minimum focused block: {minutes} minutes. Finish the question set before you sleep."


def impact_of_skipping(tasks: list[dict], mastery: dict[str, float]) -> dict:
    marks = 0.0
    details = []
    for t in tasks:
        topic = topic_by_id(t["topic_id"])
        m = mastery.get(t["topic_id"], 45)
        leak = topic["marks_weight"] * (1 - m / 100.0) * 0.15  # one skipped day ≈ 15% of remaining leak
        marks += leak
        details.append(
            {
                "topic": topic["chapter"],
                "subject": subject_by_id(topic["subject_id"])["name"],
                "leak": round(leak, 2),
                "line": (
                    f"Skipping {topic['chapter']} today leaves ~{leak:.1f} board marks "
                    f"still unsecured (topic is worth {topic['marks_weight']} marks, "
                    f"{int(topic['probability']*100)}% likely)."
                ),
            }
        )
    return {"marks_at_risk": round(marks, 1), "details": details}


def grade_answer(question: dict, given: str) -> dict:
    given_n = (given or "").strip()
    if not given_n:
        return {"correct": False, "marks_awarded": 0, "feedback": "Blank. Attempt even a partial step next time."}

    if question["type"] == "mcq":
        ok = given_n == question["answer"]
        return {
            "correct": ok,
            "marks_awarded": question["marks"] if ok else 0,
            "feedback": "Correct." if ok else f"Correct option: {question['answer']}. {question['explanation']}",
        }

    answer_l = question["answer"].lower()
    given_l = given_n.lower()
    keys = [k.lower() for k in question.get("keywords", [])]
    hits = sum(1 for k in keys if k in given_l)
    if given_l in answer_l or answer_l in given_l:
        score = question["marks"]
        ok = True
    elif keys and hits >= max(1, len(keys) // 2):
        score = round(question["marks"] * min(1.0, 0.5 + 0.5 * hits / max(1, len(keys))), 1)
        ok = score >= 0.6 * question["marks"]
    else:
        score = 0
        ok = False
    return {
        "correct": ok,
        "marks_awarded": score,
        "feedback": question["explanation"] if not ok else "Good — matches the expected idea.",
    }


def evaluate_paper(questions: list[dict], answers: dict[str, str], kind: str) -> dict:
    items = []
    awarded = 0.0
    total = 0
    for q in questions:
        result = grade_answer(q, answers.get(q["id"], ""))
        total += q["marks"]
        awarded += result["marks_awarded"]
        items.append(
            {
                "question_id": q["id"],
                "topic_id": q["topic_id"],
                "subject_id": q["subject_id"],
                "marks": q["marks"],
                "correct": result["correct"],
                "marks_awarded": result["marks_awarded"],
                "feedback": result["feedback"],
                "given": answers.get(q["id"], ""),
                "expected": q["answer"],
            }
        )
    percent = round(100 * awarded / total, 1) if total else 0
    return {
        "kind": kind,
        "awarded": round(awarded, 1),
        "total": total,
        "percent": percent,
        "items": items,
    }


def parent_briefing(student: dict, classified: dict, yesterday: dict | None, today_plan: dict | None) -> dict:
    """What a parent should actually do — not generic gyan."""
    set_track_context(student)
    is_pg = student.get("track") == "inicet"
    helps = []
    donts = []
    weak = classified["weak"][:4]
    for w in weak:
        res = resources_for_topic(w["id"])
        tutor = next((r for r in res if r["kind"] == "tuition"), None)
        book = next((r for r in res if r["kind"] == "book"), None)
        if tutor:
            helps.append(f"Book / use the tutor specifically for {w['chapter']} — not a general pep talk.")
        elif is_pg:
            helps.append(f"Ask {student['name']} to redo {w['chapter']} MCQs on NEETPGAI or Reflex PG — pharmacology/surgery gaps show up fast in mocks.")
        if book:
            helps.append(f"Keep {book['title']} on the desk for {w['chapter']}.")
        else:
            helps.append(f"Sit with {student['name']} for 20 minutes on {w['chapter']} — the leak is ~{w['leak']:.1f} marks.")

    helps.append("If study time is slipping, ask for a longer single sitting today — RIKS already named the minimum question set.")
    if is_pg:
        helps.append("Weekend = test-series day. Protect one uninterrupted 200-Q mock in Week 8; negative marking punishes guessing.")
    else:
        helps.append("If a school or VMC day was missed, open Today in RIKS: it lists the chapter that would have been covered and the catch-up drill.")

    donts.append("Do not scold for a low periodic score without reading which topic failed — they may not know where it went wrong.")
    donts.append("Do not compare with how you studied. The schedule is built for this exam, this remaining time, and this target.")
    donts.append("Do not pile extra random worksheets on a topic RIKS marked as 'safe to leave'.")

    if yesterday and not yesterday.get("completed"):
        donts.append(
            f"Yesterday's list was not finished. Ask why — tired, coaching overrun, or stuck — then look at the impact "
            f"({yesterday.get('impact_marks', '?')} marks at risk), not at character."
        )

    gap = classified["gap"]
    if gap > 0:
        standing_gap = f"{gap} points short"
    elif gap < 0:
        standing_gap = f"{-gap} points ahead"
    else:
        standing_gap = "on target"
    return {
        "helps": _unique(helps)[:6],
        "donts": donts,
        "today_summary": today_plan["tasks"] if today_plan else [],
        "standing": (
            f"{student['name']} is projected at {classified['overall_percent']}% "
            f"against a {classified['target_percent']}% target ({standing_gap}). "
            f"{(classified.get('clock') or {}).get('headline', '')} until the exam"
            f"{' — ' + classified['progress']['status_line'] if classified.get('progress') else ''}"
        ),
    }


def _unique(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for i in items:
        if i not in seen:
            seen.add(i)
            out.append(i)
    return out


def bot_script(student: dict, today_plan: dict, yesterday: dict | None, classified: dict) -> list[dict]:
    """Daily coach: what to do, what was missed, impact, resources."""
    set_track_context(student)
    TARGETS = current().TARGETS
    name = student["name"].split()[0]
    remaining = days_until(student["exam_date"])
    clock = classified.get("clock") or {}
    progress = classified.get("progress") or {}
    gap = classified["gap"]
    if gap > 0:
        gap_text = f"{gap} points short of target"
    elif gap < 0:
        gap_text = f"{-gap} points ahead of target"
    else:
        gap_text = "on target"
    msgs = []
    msgs.append(
        {
            "from": "riks",
            "text": (
                f"{name}, {clock.get('headline', str(remaining) + ' days')} until {clock.get('until', 'the exam')}. "
                f"Mode: {clock.get('mode_meta', {}).get('label', 'Steady')}. "
                f"Target: {TARGETS[student['target']]['label']}. "
                f"Projected overall {classified['overall_percent']}% ({gap_text}). "
                f"{progress.get('status_line', 'Here is the minimum set before you sleep.')}"
            ),
        }
    )
    if today_plan.get("week_title"):
        msgs.append(
            {
                "from": "riks",
                "text": f"8-week block — Week {today_plan.get('study_week')}: {today_plan['week_title']}",
            }
        )
    lines = []
    for t in today_plan["tasks"]:
        lines.append(f"• {t['minutes']} min · {subject_by_id(t['subject_id'])['name']} — {t['chapter']}")
    msgs.append({"from": "riks", "text": "Today's list:\n" + "\n".join(lines)})
    msgs.append(
        {
            "from": "riks",
            "text": (
                f"Daily exam: {len(today_plan['daily_question_ids'])} questions "
                f"({today_plan['daily_total_marks']} marks). These are the items most likely to matter "
                f"from the topics above — tagged from recalls, standard texts, and INI-CET-style mocks."
                if student.get("track") == "inicet"
                else f"from the topics above — tagged from PYQs, NCERT, and model papers."
            ),
        }
    )
    if yesterday and not yesterday.get("completed"):
        impact = yesterday.get("impact") or {}
        msgs.append(
            {
                "from": "riks",
                "text": (
                    "Yesterday's list was not finished. What got in the way — coaching ran long, "
                    "energy, or a topic you could not start? "
                    f"Impact of leaving it: ~{impact.get('marks_at_risk', yesterday.get('impact_marks', 0))} board marks still exposed."
                ),
                "prompt": True,
            }
        )
        for d in impact.get("details", [])[:3]:
            msgs.append({"from": "riks", "text": d["line"]})
    weak = classified["weak"][:2]
    if weak:
        bits = []
        for w in weak:
            res = resources_for_topic(w["id"])
            if res:
                bits.append(f"{w['chapter']}: {res[0]['title']} ({res[0]['kind']}, {res[0]['rating']}★). {res[0]['note']}")
        if bits:
            msgs.append({"from": "riks", "text": "If you need a second explanation:\n" + "\n".join(bits)})
    if today_plan.get("periodic"):
        p = today_plan["periodic"]
        msgs.append(
            {
                "from": "riks",
                "text": f"Periodic evaluation today: {p['title']}. This rewrites the coming week's schedule.",
            }
        )
    if classified["can_leave"]:
        names = ", ".join(t["chapter"] for t in classified["can_leave"][:3])
        msgs.append(
            {
                "from": "riks",
                "text": (
                    f"Conscious skip (low marginal impact if time is tight): {names}. "
                    "You can leave these unless you are chasing the topper band."
                ),
            }
        )
    if classified.get("adapted"):
        msgs.append({"from": "riks", "text": "Fine-tuned for you:\n• " + "\n• ".join(classified["adapted"])})
    if classified.get("locked"):
        names = ", ".join(t["chapter"] for t in classified["locked"][:3])
        msgs.append(
            {
                "from": "riks",
                "text": f"Not unlocked yet (foundation first): {names}.",
            }
        )
    return msgs
