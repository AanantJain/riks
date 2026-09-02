"""JSON-backed store for students, schedules, evaluations."""

from __future__ import annotations

import json
import os
import uuid
from datetime import date, datetime, timedelta
from pathlib import Path

from riks.algorithms import (
    build_schedule,
    classify_topics,
    create_test_paper,
    evaluate_paper,
    impact_of_skipping,
)
from riks.tracks import bundle_for, question_by_id, set_track_context

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = Path(os.environ.get("DATA_DIR", str(ROOT / "data"))) / "pg.json"

INICET_SUBJECTS = [
    "anatomy", "physiology", "biochem", "pharma", "pathology", "micro",
    "medicine", "surgery", "psm", "obg", "peds", "ortho", "ent_ophth", "forensic",
]


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


class Store:
    def __init__(self) -> None:
        self.path = DATA_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            self.state = json.loads(self.path.read_text())
        else:
            self.state = {"students": {}, "evaluations": {}, "completions": {}, "missed_notes": {}}
        self.ensure_demo_students()
        if not self.path.exists():
            self.save()

    def save(self) -> None:
        self.path.write_text(json.dumps(self.state, indent=2))

    def ensure_demo_students(self) -> None:
        changed = False
        if "nikita" not in self.state.get("students", {}):
            self._seed_nikita()
            changed = True
        if changed:
            self.save()

    def seed_demo(self) -> None:
        self._seed_nikita()

    def _seed_aanant(self) -> None:
        exam = (date.today() + timedelta(days=92)).isoformat()
        student = {
            "id": "aanant",
            "name": "Aanant",
            "track": "cbse",
            "class_level": "10",
            "board": "CBSE",
            "exam_date": exam,
            "target": "distinction",
            "subjects": ["maths", "science", "sst"],
            "coaching": {
                "weekend_institute": True,
                "weekend_institute_name": "VMC",
                "private_maths": True,
                "school_rest": True,
            },
            "strong_subjects": ["science"],
            "weak_subjects": ["maths"],
            "parent_name": "Father",
            "created_at": _now(),
            "demo": True,
        }
        self.state.setdefault("students", {})["aanant"] = student
        self.state.setdefault("evaluations", {})["aanant"] = [
            {
                "id": "seed-eval",
                "kind": "periodic",
                "date": (date.today() - timedelta(days=6)).isoformat(),
                "percent": 54,
                "awarded": 11,
                "total": 20,
                "items": [
                    {"topic_id": "m-quad", "correct": False, "marks": 4, "marks_awarded": 1, "subject_id": "maths"},
                    {"topic_id": "m-trig", "correct": False, "marks": 4, "marks_awarded": 2, "subject_id": "maths"},
                    {"topic_id": "m-ap", "correct": True, "marks": 3, "marks_awarded": 3, "subject_id": "maths"},
                    {"topic_id": "s-life", "correct": True, "marks": 3, "marks_awarded": 3, "subject_id": "science"},
                    {"topic_id": "s-elec", "correct": True, "marks": 3, "marks_awarded": 2, "subject_id": "science"},
                    {"topic_id": "h-nation-in", "correct": False, "marks": 3, "marks_awarded": 0, "subject_id": "sst"},
                ],
            }
        ]
        self.state.setdefault("completions", {})["aanant"] = {}
        self.state.setdefault("missed_notes", {})["aanant"] = []
        yday = (date.today() - timedelta(days=1)).isoformat()
        self.state["completions"]["aanant"][yday] = {"completed": False, "reason": None}
        student["schedule"] = build_schedule(
            student, self.state["evaluations"]["aanant"], completions=self.state["completions"]["aanant"]
        )

    def _seed_nikita(self) -> None:
        exam = (date.today() + timedelta(days=56)).isoformat()
        student = {
            "id": "nikita",
            "name": "Nikita",
            "track": "inicet",
            "class_level": "Intern",
            "board": "INI-CET",
            "exam_date": exam,
            "target": "aiims_band",
            "subjects": INICET_SUBJECTS,
            "coaching": {
                "weekend_institute": True,
                "weekend_institute_name": "Marrow / NEETPGAI mocks",
                "private_maths": False,
                "school_rest": False,
                "hospital_duty": True,
            },
            "strong_subjects": ["anatomy", "physiology"],
            "weak_subjects": ["pharma", "surgery"],
            "parent_name": "Father",
            "created_at": _now(),
            "demo": True,
        }
        self.state.setdefault("students", {})["nikita"] = student
        self.state.setdefault("evaluations", {})["nikita"] = []
        self.state.setdefault("completions", {})["nikita"] = {}
        self.state.setdefault("missed_notes", {})["nikita"] = []
        student["schedule"] = build_schedule(student, [], completions={})

    def create_student(self, payload: dict) -> dict:
        sid = str(uuid.uuid4())[:8]
        track = str(payload.get("track") or "cbse").strip().lower()
        if track not in {"cbse", "inicet"}:
            track = "cbse"
        bundle = bundle_for({"track": track})
        default_target = "aiims_band" if track == "inicet" else "first_division"
        student = {
            "id": sid,
            "name": payload["name"].strip(),
            "track": track,
            "class_level": payload.get("class_level") or ("Intern" if track == "inicet" else "10"),
            "board": payload.get("board") or ("INI-CET" if track == "inicet" else "CBSE"),
            "exam_date": payload["exam_date"],
            "target": payload.get("target") or default_target,
            "subjects": payload.get("subjects") or [s["id"] for s in bundle.SUBJECTS],
            "coaching": {
                "weekend_institute": bool(payload.get("weekend_institute")),
                "weekend_institute_name": payload.get("weekend_institute_name") or "",
                "private_maths": bool(payload.get("private_maths")),
                "school_rest": bool(payload.get("school_rest", track == "cbse")),
                "hospital_duty": bool(payload.get("hospital_duty", track == "inicet")),
            },
            "strong_subjects": payload.get("strong_subjects") or [],
            "weak_subjects": payload.get("weak_subjects") or [],
            "parent_name": payload.get("parent_name") or "Parent",
            "created_at": _now(),
            "demo": False,
        }
        if student["target"] not in bundle.TARGETS:
            student["target"] = default_target
        self.state["students"][sid] = student
        self.state["evaluations"][sid] = []
        self.state["completions"][sid] = {}
        self.state["missed_notes"][sid] = []
        student["schedule"] = build_schedule(student, [], completions={})
        self.save()
        return student

    def reset_progress(self, student_id: str) -> None:
        student = self.get(student_id)
        if not student:
            return
        self.state["evaluations"][student_id] = []
        self.state["completions"][student_id] = {}
        self.state["missed_notes"][student_id] = []
        student["created_at"] = _now()
        student.pop("learner", None)
        student["schedule"] = build_schedule(student, [], completions={})
        self.save()

    def update_profile(self, student_id: str, payload: dict) -> dict:
        student = self.get(student_id)
        if not student:
            raise ValueError("unknown student")
        bundle = bundle_for(student)
        if payload.get("name"):
            student["name"] = str(payload["name"]).strip()
        if payload.get("exam_date"):
            student["exam_date"] = str(payload["exam_date"])
        if payload.get("target") and payload["target"] in bundle.TARGETS:
            student["target"] = payload["target"]
        if payload.get("parent_name"):
            student["parent_name"] = str(payload["parent_name"]).strip()
        coaching = student.setdefault("coaching", {})
        if "weekend_institute" in payload:
            coaching["weekend_institute"] = bool(payload.get("weekend_institute"))
        if payload.get("weekend_institute_name") is not None:
            coaching["weekend_institute_name"] = str(payload.get("weekend_institute_name") or "")
        if student.get("track") == "inicet":
            if "hospital_duty" in payload:
                coaching["hospital_duty"] = bool(payload.get("hospital_duty"))
        else:
            if "private_maths" in payload:
                coaching["private_maths"] = bool(payload.get("private_maths"))
            if "school_rest" in payload:
                coaching["school_rest"] = bool(payload.get("school_rest"))
        if payload.get("strong_subjects") is not None:
            student["strong_subjects"] = list(payload["strong_subjects"])
        if payload.get("weak_subjects") is not None:
            student["weak_subjects"] = list(payload["weak_subjects"])
        if payload.get("reset"):
            self.state["evaluations"][student_id] = []
            self.state["completions"][student_id] = {}
            self.state["missed_notes"][student_id] = []
            student["created_at"] = _now()
            student.pop("learner", None)
        student["schedule"] = build_schedule(
            student,
            self.evaluations(student_id),
            completions=self.state["completions"].get(student_id),
        )
        self.save()
        return student

    def get(self, student_id: str) -> dict | None:
        return self.state["students"].get(student_id)

    def evaluations(self, student_id: str) -> list[dict]:
        return self.state["evaluations"].get(student_id, [])

    def refresh_schedule(self, student_id: str) -> None:
        student = self.get(student_id)
        student["schedule"] = build_schedule(
            student,
            self.evaluations(student_id),
            completions=self.state["completions"].get(student_id),
        )
        self.save()

    def day_plan(self, student_id: str, day: str | None = None) -> dict | None:
        student = self.get(student_id)
        if not student:
            return None
        day = day or date.today().isoformat()
        for d in student.get("schedule", []):
            if d["date"] == day:
                return d
        return None

    def yesterday_plan(self, student_id: str) -> dict | None:
        y = (date.today() - timedelta(days=1)).isoformat()
        plan = self.day_plan(student_id, y)
        if not plan:
            return None
        comp = self.state["completions"].get(student_id, {}).get(y, {})
        if not comp:
            return None
        student = self.get(student_id)
        set_track_context(student)
        classified = classify_topics(
            student,
            self.evaluations(student_id),
            self.state["completions"].get(student_id),
        )
        impact = impact_of_skipping(plan["tasks"], classified["mastery"])
        return {
            **plan,
            "completed": bool(comp.get("completed")),
            "reason": comp.get("reason"),
            "impact": impact,
            "impact_marks": impact["marks_at_risk"],
        }

    def mark_day(self, student_id: str, day: str, completed: bool, reason: str | None = None) -> None:
        self.state["completions"].setdefault(student_id, {})[day] = {
            "completed": completed,
            "reason": reason,
        }
        self.save()

    def add_missed_class(self, student_id: str, when: str, place: str, note: str) -> None:
        self.state["missed_notes"].setdefault(student_id, []).append(
            {"when": when, "place": place, "note": note, "created_at": _now()}
        )
        self.save()

    def missed_classes(self, student_id: str) -> list[dict]:
        return self.state["missed_notes"].get(student_id, [])

    def submit_exam(self, student_id: str, kind: str, question_ids: list[str], answers: dict[str, str]) -> dict:
        student = self.get(student_id)
        set_track_context(student)
        questions = [question_by_id(qid) for qid in question_ids]
        result = evaluate_paper(questions, answers, kind)
        result["id"] = str(uuid.uuid4())[:8]
        result["date"] = date.today().isoformat()
        self.state["evaluations"].setdefault(student_id, []).append(result)
        if kind == "daily":
            all_ok = all(i["correct"] or i["marks_awarded"] > 0 for i in result["items"])
            self.mark_day(student_id, date.today().isoformat(), completed=all_ok or result["percent"] >= 50)
        self.refresh_schedule(student_id)
        return result

    def periodic_paper(self, student_id: str, subject_id: str) -> dict:
        student = self.get(student_id)
        set_track_context(student)
        classified = classify_topics(student, self.evaluations(student_id), self.state["completions"].get(student_id))
        topic_ids = [t["id"] for t in classified["rows"] if t["subject_id"] == subject_id and t.get("unlocked", True)]
        if not topic_ids:
            topic_ids = [t["id"] for t in classified["rows"] if t["subject_id"] == subject_id]
        return create_test_paper(
            topic_ids,
            "periodic",
            classified["mastery"],
            rng_seed=f"{student_id}-{subject_id}-{date.today()}",
            learner=classified.get("learner"),
        )

    def snapshot(self, student_id: str) -> dict:
        student = self.get(student_id)
        set_track_context(student)
        classified = classify_topics(student, self.evaluations(student_id), self.state["completions"].get(student_id))
        want_n = int((classified.get("clock") or {}).get("mode_meta", {}).get("paper") or 6)
        today = self.day_plan(student_id)
        if today and len(today.get("daily_question_ids") or []) != want_n:
            self.refresh_schedule(student_id)
            set_track_context(student)
            classified = classify_topics(
                student, self.evaluations(student_id), self.state["completions"].get(student_id)
            )
            today = self.day_plan(student_id)
        yesterday = self.yesterday_plan(student_id)
        return {
            "student": student,
            "classified": classified,
            "today": today,
            "yesterday": yesterday,
            "evaluations": self.evaluations(student_id),
            "missed": self.missed_classes(student_id),
            "mastery": classified["mastery"],
        }


store = Store()
