"""Track registry: CBSE board vs INI-CET medical PG."""

from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass
from typing import Callable

from riks import curriculum as cbse_curriculum
from riks import curriculum_inicet
from riks import questions as cbse_questions
from riks import questions_inicet
from riks import resources as cbse_resources
from riks import resources_inicet

_ctx: ContextVar["TrackBundle | None"] = ContextVar("riks_track", default=None)


@dataclass(frozen=True)
class TrackBundle:
    id: str
    label: str
    SUBJECTS: list
    TOPICS: list
    TARGETS: dict
    TARGET_MASTERY: dict
    QUESTIONS: list
    RESOURCES: list
    PREREQS: dict
    WEEK_PLAN: list
    projected_max: int  # total exam marks (100 per CBSE subject, 200 for INI-CET)
    score_unit: str  # "percent" | "marks"


CBSE = TrackBundle(
    id="cbse",
    label="CBSE Board",
    SUBJECTS=cbse_curriculum.SUBJECTS,
    TOPICS=cbse_curriculum.TOPICS,
    TARGETS=cbse_curriculum.TARGETS,
    TARGET_MASTERY={
        "pass": 45,
        "first_division": 65,
        "distinction": 80,
        "topper": 92,
    },
    QUESTIONS=cbse_questions.QUESTIONS,
    RESOURCES=cbse_resources.RESOURCES,
    PREREQS={
        "m-poly": ["m-real"],
        "m-quad": ["m-poly"],
        "m-linear": ["m-poly"],
        "m-trigapp": ["m-trig"],
        "m-vol": ["m-areas"],
        "s-carbon": ["s-chemrxn", "s-acids"],
        "s-light": ["s-elec"],
        "s-heredity": ["s-repro"],
        "h-nation-in": ["h-nation-eu"],
        "e-money": ["e-dev", "e-sectors"],
    },
    WEEK_PLAN=[],
    projected_max=100,
    score_unit="percent",
)

INICET = TrackBundle(
    id="inicet",
    label="INI-CET (AIIMS PG)",
    SUBJECTS=curriculum_inicet.SUBJECTS,
    TOPICS=curriculum_inicet.TOPICS,
    TARGETS=curriculum_inicet.TARGETS,
    TARGET_MASTERY=curriculum_inicet.TARGET_MASTERY,
    QUESTIONS=questions_inicet.QUESTIONS,
    RESOURCES=resources_inicet.RESOURCES,
    PREREQS=curriculum_inicet.PREREQS,
    WEEK_PLAN=curriculum_inicet.WEEK_PLAN,
    projected_max=200,
    score_unit="marks",
)

TRACKS = {"cbse": CBSE, "inicet": INICET}


def track_id(student: dict | None) -> str:
    if not student:
        return "cbse"
    tid = str(student.get("track") or "cbse").strip().lower()
    return tid if tid in TRACKS else "cbse"


def bundle_for(student: dict | None) -> TrackBundle:
    return TRACKS[track_id(student)]


def set_track_context(student: dict | None) -> None:
    _ctx.set(bundle_for(student))


def current() -> TrackBundle:
    b = _ctx.get()
    return b if b is not None else CBSE


def subject_by_id(subject_id: str, bundle: TrackBundle | None = None) -> dict:
    bundle = bundle or current()
    for s in bundle.SUBJECTS:
        if s["id"] == subject_id:
            return s
    return {"id": subject_id or "", "name": subject_id or "Subject", "color": "#666666"}


def topic_by_id(topic_id: str, bundle: TrackBundle | None = None) -> dict:
    bundle = bundle or current()
    for t in bundle.TOPICS:
        if t["id"] == topic_id:
            return t
    return {"id": topic_id or "", "chapter": topic_id or "Topic", "subject_id": ""}


def topics_for_subject(subject_id: str, bundle: TrackBundle | None = None) -> list:
    bundle = bundle or current()
    return [t for t in bundle.TOPICS if t["subject_id"] == subject_id]


def questions_for_topic(topic_id: str, bundle: TrackBundle | None = None) -> list:
    bundle = bundle or current()
    return [q for q in bundle.QUESTIONS if q["topic_id"] == topic_id]


def question_by_id(question_id: str, bundle: TrackBundle | None = None) -> dict:
    bundle = bundle or current()
    return next(q for q in bundle.QUESTIONS if q["id"] == question_id)


def resources_for_topic(topic_id: str, bundle: TrackBundle | None = None) -> list:
    bundle = bundle or current()
    return [r for r in bundle.RESOURCES if r["topic_id"] == topic_id]


def current_week(student: dict, today=None) -> int:
    """1-based study week in the 8-week INI-CET block."""
    from datetime import date, datetime

    today = today or date.today()
    bundle = bundle_for(student)
    if not bundle.WEEK_PLAN:
        return 1
    exam = datetime.strptime(student["exam_date"][:10], "%Y-%m-%d").date()
    remaining = max(0, (exam - today).days)
    elapsed = max(0, 56 - remaining)
    week = min(8, max(1, elapsed // 7 + 1))
    return week
