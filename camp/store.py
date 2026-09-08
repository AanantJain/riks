"""OpenCamp — progress store and daily plan."""

from __future__ import annotations

import json
from datetime import date, datetime, timedelta
import os
from pathlib import Path

from camp.catalog import module_by_id
from camp.govern import bot_script, build_schedule, classify, coach_briefing, impact_of_skipping

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(os.environ.get("DATA_DIR", str(ROOT / "data"))) / "state.json"


def _today() -> str:
    return date.today().isoformat()


def _default_contest() -> str:
    return (date.today() + timedelta(days=21)).isoformat()


class Store:
    def __init__(self) -> None:
        DATA.parent.mkdir(parents=True, exist_ok=True)
        if DATA.exists():
            self.state = json.loads(DATA.read_text())
        else:
            self.state = {}
        self.state.setdefault("handle", "")
        if not str(self.state.get("handle") or "").strip():
            self.state["handle"] = os.environ.get("RIKS_HANDLE", "Aanant")
        self.state.setdefault("goal", "cf-1400")
        self.state.setdefault("solved", {})
        self.state.setdefault("skipped", {})
        self.state.setdefault("notes", {})
        self.state.setdefault("started", _today())
        self.state.setdefault("contest_date", _default_contest())
        self.state.setdefault("hours_per_day", 2)
        self.state.setdefault("strong_modules", [])
        self.state.setdefault("weak_modules", ["graphs1", "dp"])
        self.state.setdefault("completions", {})
        self.state.setdefault("drill_log", [])
        self.state.setdefault("drills_solved", {})
        if "bootcamp" not in (self.state.get("strong_modules") or []) and not self.state.get("handle"):
            # Demo seed so the board is not empty on first paint.
            if not self.state["solved"]:
                self.state["solved"] = {
                    "cf-4a": (date.today() - timedelta(days=5)).isoformat(),
                    "cf-71a": (date.today() - timedelta(days=4)).isoformat(),
                    "cf-231a": (date.today() - timedelta(days=3)).isoformat(),
                }
                self.state["handle"] = self.state.get("handle") or ""
        y = (date.today() - timedelta(days=1)).isoformat()
        self.state["completions"].setdefault(y, {"completed": False, "reason": None})
        self.save()

    def save(self) -> None:
        DATA.write_text(json.dumps(self.state, indent=2))

    def set_profile(self, payload: dict) -> None:
        self.state["handle"] = (payload.get("handle") or "").strip() or self.state.get("handle") or ""
        self.state["goal"] = payload.get("goal") or "cf-1400"
        if payload.get("contest_date"):
            self.state["contest_date"] = payload["contest_date"]
        if payload.get("hours_per_day"):
            self.state["hours_per_day"] = int(payload["hours_per_day"])
        self.state["strong_modules"] = payload.get("strong_modules") or []
        self.state["weak_modules"] = payload.get("weak_modules") or []
        # Rebuild starts the remaining-days clock from today so the board visibly updates.
        self.state["started"] = _today()
        if payload.get("reset"):
            self.state["solved"] = {}
            self.state["skipped"] = {}
            self.state["notes"] = {}
            self.state["completions"] = {}
            self.state["drill_log"] = []
            self.state["drills_solved"] = {}
        self.save()

    def mark(self, pid: str, status: str) -> None:
        if status == "solved":
            self.state["solved"][pid] = _today()
            self.state["skipped"].pop(pid, None)
        elif status == "skipped":
            self.state["skipped"][pid] = _today()
            self.state["solved"].pop(pid, None)
        elif status == "clear":
            self.state["solved"].pop(pid, None)
            self.state["skipped"].pop(pid, None)
        # If today's named set is mostly done, close the day.
        snap = self.snapshot()
        today = snap.get("today") or {}
        ids = [t["id"] for t in today.get("tasks", [])]
        if ids and all(i in self.state["solved"] or i in self.state["skipped"] for i in ids):
            self.state["completions"][_today()] = {"completed": True, "reason": None}
        self.save()

    def record_drills(self, results: list[dict]) -> None:
        when = date.today().isoformat()
        self.state.setdefault("drill_log", [])
        self.state.setdefault("drills_solved", {})
        for r in results:
            self.state["drill_log"].append(
                {
                    "qid": r["question_id"],
                    "when": when,
                    "score": float(r.get("score") or 0),
                    "correct": bool(r.get("correct")),
                    "at": datetime.now().isoformat(timespec="seconds"),
                }
            )
            if r.get("correct") or float(r.get("score") or 0) >= 0.99:
                self.state["drills_solved"][r["question_id"]] = when
        self.save()

    def drill_status(self, qid: str) -> str:
        if qid in (self.state.get("drills_solved") or {}):
            return "solved"
        return "open"

    def mark_day(self, day: str, completed: bool, reason: str | None = None) -> None:
        self.state["completions"][day] = {"completed": completed, "reason": reason}
        self.save()

    def status_of(self, pid: str) -> str:
        if pid in self.state["solved"]:
            return "solved"
        if pid in self.state["skipped"]:
            return "skipped"
        return "open"

    def snapshot(self) -> dict:
        classified = classify(self.state)
        schedule = build_schedule(self.state, classified)
        today = date.today().isoformat()
        today_plan = next((d for d in schedule if d["date"] == today), schedule[1] if len(schedule) > 1 else None)
        yday = (date.today() - timedelta(days=1)).isoformat()
        y_plan = next((d for d in schedule if d["date"] == yday), None)
        y_comp = self.state["completions"].get(yday, {})
        yesterday = None
        if y_plan:
            impact = impact_of_skipping(y_plan["tasks"], classified)
            yesterday = {
                **y_plan,
                "completed": bool(y_comp.get("completed")),
                "reason": y_comp.get("reason"),
                "impact": impact,
                "impact_marks": impact["rating_at_risk"],
            }
        messages = bot_script(self.state, classified, today_plan or {"tasks": []}, yesterday)
        coach = coach_briefing(self.state, classified, yesterday, today_plan)
        return {
            "state": self.state,
            "classified": classified,
            "schedule": schedule,
            "today": today_plan,
            "yesterday": yesterday,
            "messages": messages,
            "coach": coach,
        }

    def module_view(self, mid: str) -> dict:
        from camp.drills import drills_for_module, public_drill

        m = module_by_id(mid)
        problems = []
        for p in m["problems"]:
            problems.append({**p, "status": self.status_of(p["id"]), "note": self.state["notes"].get(p["id"], "")})
        s = sum(1 for p in problems if p["status"] == "solved")
        classified = classify(self.state)
        row = next((r for r in classified["rows"] if r["id"] == mid), None)
        drills = [{**public_drill(d), "status": self.drill_status(d["id"])} for d in drills_for_module(mid)]
        return {**m, "problems": problems, "solved": s, "total": len(problems), "row": row, "drills": drills}


store = Store()
