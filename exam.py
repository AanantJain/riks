"""Nikita INI-CET desk, mounted on the family RIKS app."""

from __future__ import annotations

from datetime import date, timedelta

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from riks.algorithms import bot_script, parent_briefing
from riks.store import store
from riks.tracks import bundle_for, question_by_id, set_track_context, subject_by_id, topic_by_id

router = APIRouter()
COOKIE = "riks_student"
templates: Jinja2Templates | None = None


def bind(t: Jinja2Templates) -> None:
    global templates
    templates = t


def current_student_id(request: Request) -> str | None:
    return request.cookies.get(COOKIE)


def require_student(request: Request):
    sid = current_student_id(request)
    if not sid or not store.get(sid):
        return None
    return sid


def render(request: Request, name: str, **ctx):
    sid = current_student_id(request)
    student = store.get(sid) if sid else None
    ctx.setdefault("student", student)
    ctx.setdefault("role", request.cookies.get("riks_role") or "student")
    if student:
        set_track_context(student)
        bundle = bundle_for(student)
        ctx.setdefault("track", bundle)
        ctx.setdefault("subjects", bundle.SUBJECTS)
        ctx.setdefault("targets", bundle.TARGETS)
    else:
        from riks.tracks import INICET

        ctx.setdefault("track", INICET)
        ctx.setdefault("subjects", INICET.SUBJECTS)
        ctx.setdefault("targets", INICET.TARGETS)
    ctx.setdefault("subject_by_id", subject_by_id)
    ctx.setdefault("topic_by_id", topic_by_id)
    return templates.TemplateResponse(request, name, ctx)


@router.get("/enter/nikita")
def enter_nikita():
    if not store.get("nikita"):
        return RedirectResponse("/", status_code=303)
    resp = RedirectResponse("/student", status_code=303)
    resp.set_cookie(COOKIE, "nikita", httponly=True)
    resp.set_cookie("riks_role", "student")
    return resp


@router.get("/enter/nikita-parent")
def enter_nikita_parent():
    if not store.get("nikita"):
        return RedirectResponse("/", status_code=303)
    resp = RedirectResponse("/parent", status_code=303)
    resp.set_cookie(COOKIE, "nikita", httponly=True)
    resp.set_cookie("riks_role", "parent")
    return resp


@router.get("/logout")
def logout():
    resp = RedirectResponse("/", status_code=303)
    resp.delete_cookie(COOKIE)
    resp.delete_cookie("riks_role")
    return resp


@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request, track: str = "inicet"):
    track = "inicet"
    default_exam = (date.today() + timedelta(days=56)).isoformat()
    fake = {"track": track}
    set_track_context(fake)
    bundle = bundle_for(fake)
    return render(
        request,
        "register.html",
        default_exam=default_exam,
        register_track=track,
        student=None,
        subjects=bundle.SUBJECTS,
        targets=bundle.TARGETS,
    )


@router.post("/register")
async def register(request: Request):
    form = await request.form()
    student = store.create_student(
        {
            "track": "inicet",
            "name": str(form.get("name") or "").strip() or "Student",
            "exam_date": str(form.get("exam_date") or (date.today() + timedelta(days=56)).isoformat()),
            "target": str(form.get("target") or "aiims_band"),
            "parent_name": str(form.get("parent_name") or "Parent"),
            "weekend_institute": form.get("weekend_institute"),
            "weekend_institute_name": str(form.get("weekend_institute_name") or ""),
            "hospital_duty": form.get("hospital_duty"),
            "strong_subjects": [str(v) for v in form.getlist("strong")],
            "weak_subjects": [str(v) for v in form.getlist("weak")],
        }
    )
    resp = RedirectResponse("/student", status_code=303)
    resp.set_cookie(COOKIE, student["id"], httponly=True)
    resp.set_cookie("riks_role", "student")
    return resp


@router.get("/student", response_class=HTMLResponse)
def student_home(request: Request):
    sid = require_student(request)
    if not sid:
        return RedirectResponse("/enter/nikita", status_code=303)
    snap = store.snapshot(sid)
    return render(request, "student/dashboard.html", snap=snap)


@router.post("/student/profile")
async def student_profile(request: Request):
    sid = require_student(request)
    if not sid:
        return RedirectResponse("/enter/nikita", status_code=303)
    form = await request.form()
    store.update_profile(
        sid,
        {
            "name": str(form.get("name") or "").strip(),
            "exam_date": str(form.get("exam_date") or ""),
            "target": str(form.get("target") or ""),
            "parent_name": str(form.get("parent_name") or ""),
            "weekend_institute": form.get("weekend_institute"),
            "weekend_institute_name": str(form.get("weekend_institute_name") or ""),
            "hospital_duty": form.get("hospital_duty"),
            "strong_subjects": [str(v) for v in form.getlist("strong")],
            "weak_subjects": [str(v) for v in form.getlist("weak")],
            "reset": form.get("reset") == "1",
        },
    )
    return RedirectResponse("/student", status_code=303)


@router.get("/student/today", response_class=HTMLResponse)
def student_today(request: Request):
    sid = require_student(request)
    if not sid:
        return RedirectResponse("/enter/nikita", status_code=303)
    snap = store.snapshot(sid)
    if not snap["today"]:
        store.refresh_schedule(sid)
        snap = store.snapshot(sid)
    messages = bot_script(snap["student"], snap["today"], snap["yesterday"], snap["classified"])
    return render(request, "student/today.html", snap=snap, messages=messages)


@router.post("/student/yesterday-reason")
def yesterday_reason(request: Request, reason: str = Form(...)):
    sid = require_student(request)
    if not sid:
        return RedirectResponse("/enter/nikita", status_code=303)
    y = store.yesterday_plan(sid)
    if y:
        store.mark_day(sid, y["date"], completed=False, reason=reason)
    return RedirectResponse("/student/today", status_code=303)


@router.post("/student/missed-class")
def missed_class(request: Request, place: str = Form(...), note: str = Form("")):
    sid = require_student(request)
    if not sid:
        return RedirectResponse("/enter/nikita", status_code=303)
    store.add_missed_class(sid, date.today().isoformat(), place, note)
    return RedirectResponse("/student/today", status_code=303)


@router.get("/student/schedule", response_class=HTMLResponse)
def student_schedule(request: Request):
    sid = require_student(request)
    if not sid:
        return RedirectResponse("/enter/nikita", status_code=303)
    snap = store.snapshot(sid)
    return render(request, "student/schedule.html", snap=snap)


@router.get("/student/daily-exam", response_class=HTMLResponse)
def daily_exam(request: Request):
    sid = require_student(request)
    if not sid:
        return RedirectResponse("/enter/nikita", status_code=303)
    snap = store.snapshot(sid)
    plan = snap["today"]
    questions = [question_by_id(qid) for qid in plan["daily_question_ids"]] if plan else []
    return render(
        request,
        "student/exam.html",
        snap=snap,
        questions=questions,
        kind="daily",
        title="Daily exam  finish before you sleep",
        action="/student/daily-exam",
    )


@router.post("/student/daily-exam")
async def submit_daily(request: Request):
    sid = require_student(request)
    if not sid:
        return RedirectResponse("/enter/nikita", status_code=303)
    form = await request.form()
    plan = store.day_plan(sid)
    qids = plan["daily_question_ids"]
    answers = {qid: str(form.get(qid, "")) for qid in qids}
    result = store.submit_exam(sid, "daily", qids, answers)
    snap = store.snapshot(sid)
    return render(request, "student/exam_result.html", snap=snap, result=result, kind="daily")


@router.get("/student/periodic-exam", response_class=HTMLResponse)
def periodic_exam(request: Request, subject: str = "anatomy"):
    sid = require_student(request)
    if not sid:
        return RedirectResponse("/enter/nikita", status_code=303)
    snap = store.snapshot(sid)
    paper = store.periodic_paper(sid, subject)
    return render(
        request,
        "student/exam.html",
        snap=snap,
        questions=paper["questions"],
        kind="periodic",
        subject=subject,
        title=f"Periodic evaluation  {subject_by_id(subject)['name']}",
        action=f"/student/periodic-exam?subject={subject}",
    )


@router.post("/student/periodic-exam")
async def submit_periodic(request: Request, subject: str = "anatomy"):
    sid = require_student(request)
    if not sid:
        return RedirectResponse("/enter/nikita", status_code=303)
    form = await request.form()
    paper = store.periodic_paper(sid, subject)
    qids = paper["question_ids"]
    answers = {qid: str(form.get(qid, "")) for qid in qids}
    result = store.submit_exam(sid, "periodic", qids, answers)
    snap = store.snapshot(sid)
    return render(request, "student/exam_result.html", snap=snap, result=result, kind="periodic", subject=subject)


@router.get("/student/week-plan", response_class=HTMLResponse)
def week_plan(request: Request):
    sid = require_student(request)
    if not sid:
        return RedirectResponse("/enter/nikita", status_code=303)
    snap = store.snapshot(sid)
    if not snap["classified"].get("week_plan"):
        return RedirectResponse("/student", status_code=303)
    return render(request, "student/week_plan.html", snap=snap)


@router.get("/student/progress", response_class=HTMLResponse)
def progress(request: Request):
    sid = require_student(request)
    if not sid:
        return RedirectResponse("/enter/nikita", status_code=303)
    snap = store.snapshot(sid)
    return render(request, "student/progress.html", snap=snap)


@router.get("/parent", response_class=HTMLResponse)
def parent_home(request: Request):
    sid = require_student(request) or "nikita"
    if not store.get(sid):
        return RedirectResponse("/", status_code=303)
    snap = store.snapshot(sid)
    brief = parent_briefing(snap["student"], snap["classified"], snap["yesterday"], snap["today"])
    return render(request, "parent/dashboard.html", snap=snap, brief=brief)
