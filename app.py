"""OpenCamp — RIKS for contests: govern the journey to rating success."""

from __future__ import annotations

import hmac
import os
from http.cookies import SimpleCookie
from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, Form, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from camp.catalog import MODULES, SHELVES
from camp.contests import upcoming_codeforces
from camp.drills import DRILLS, drill_by_id, drills_for_module, pick_drills, public_drill
from camp.govern import GOALS
from camp.judge import grade
from camp.store import store
from exam import bind as bind_exam
from exam import router as exam_router

from starlette.datastructures import Headers
from starlette.types import ASGIApp, Receive, Scope, Send

ROOT = Path(__file__).resolve().parent
app = FastAPI(title="RIKS Contest")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
templates = Jinja2Templates(directory=str(ROOT / "templates"))
templates.env.globals.update(goals=GOALS, modules=MODULES, today=lambda: __import__("datetime").date.today().isoformat())
bind_exam(templates)
app.include_router(exam_router)

FAMILY_PASSWORD = os.environ.get("RIKS_PASSWORD", "").strip()
FAMILY_COOKIE = hmac.new(b"riks-contest", FAMILY_PASSWORD.encode(), "sha256").hexdigest()[:32] if FAMILY_PASSWORD else ""
PUBLIC_PATHS = {"/", "/unlock", "/healthz"}


def safe_next(value: str | None) -> str:
    raw = (value or "/").strip()
    if raw.startswith("/") and not raw.startswith("//") and "://" not in raw and not raw.startswith("/unlock"):
        return raw
    return "/"


class FamilyGateMiddleware:
    """ASGI gate that does not consume the request body (so POST forms still work)."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or not FAMILY_PASSWORD:
            await self.app(scope, receive, send)
            return
        path = scope.get("path", "")
        if path.startswith("/static") or path in PUBLIC_PATHS:
            await self.app(scope, receive, send)
            return
        cookie = ""
        raw = Headers(scope=scope).get("cookie") or ""
        parsed = SimpleCookie()
        try:
            parsed.load(raw)
        except Exception:
            parsed = SimpleCookie()
        if "riks_family" in parsed:
            cookie = parsed["riks_family"].value
        if cookie == FAMILY_COOKIE:
            await self.app(scope, receive, send)
            return
        qs = scope.get("query_string") or b""
        if isinstance(qs, bytes):
            qs = qs.decode("latin-1")
        dest = path + (f"?{qs}" if qs else "")
        response = RedirectResponse(f"/unlock?next={quote(safe_next(dest), safe='/')}", status_code=303)
        await response(scope, receive, send)


app.add_middleware(FamilyGateMiddleware)


@app.get("/healthz")
def healthz():
    return {"ok": True}


def render(request: Request, name: str, **ctx):
    ctx["snap"] = store.snapshot()
    return templates.TemplateResponse(request, name, ctx)


@app.get("/unlock", response_class=HTMLResponse)
def unlock_form(request: Request, wrong: int = 0, next_path: str = Query("/", alias="next")):
    return templates.TemplateResponse(
        request,
        "unlock.html",
        {"wrong": bool(wrong), "next_path": safe_next(next_path)},
    )


@app.post("/unlock")
def unlock_submit(password: str = Form(""), next_path: str = Form("/", alias="next")):
    dest = safe_next(next_path)
    if FAMILY_PASSWORD and password == FAMILY_PASSWORD:
        resp = RedirectResponse(dest, status_code=303)
        resp.set_cookie(
            "riks_family",
            FAMILY_COOKIE,
            httponly=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 120,
            path="/",
        )
        return resp
    return RedirectResponse(f"/unlock?wrong=1&next={quote(dest, safe='/')}", status_code=303)


@app.get("/", response_class=HTMLResponse)
def choose(request: Request):
    return templates.TemplateResponse(request, "choose.html", {})


@app.get("/overview", response_class=HTMLResponse)
def overview(request: Request):
    return templates.TemplateResponse(request, "overview.html", {})


@app.get("/camp", response_class=HTMLResponse)
def home(request: Request):
    return render(request, "home.html", rebuilt=request.query_params.get("rebuilt") == "1")


@app.get("/board", response_class=HTMLResponse)
def board_alias(request: Request):
    return RedirectResponse("/camp", status_code=303)


@app.get("/today", response_class=HTMLResponse)
def today(request: Request):
    return render(request, "today.html")


@app.post("/yesterday-reason")
def yesterday_reason(reason: str = Form(...)):
    y = store.snapshot()["yesterday"]
    if y:
        store.mark_day(y["date"], completed=False, reason=reason)
    return RedirectResponse("/today", status_code=303)


@app.get("/schedule", response_class=HTMLResponse)
def schedule(request: Request):
    return render(request, "schedule.html")


@app.get("/path", response_class=HTMLResponse)
def path(request: Request):
    return render(request, "path.html")


@app.get("/module/{mid}", response_class=HTMLResponse)
def module(request: Request, mid: str):
    view = store.module_view(mid)
    return render(request, "module.html", mod=view, drills=view.get("drills") or [])


@app.post("/mark/{pid}")
def mark(pid: str, status: str = Form(...), next: str = Form("/camp")):
    store.mark(pid, status)
    return RedirectResponse(next, status_code=303)


@app.get("/resources", response_class=HTMLResponse)
def resources(request: Request):
    return render(request, "resources.html", shelves=SHELVES)


@app.get("/contests", response_class=HTMLResponse)
def contests(request: Request):
    return render(request, "contests.html", rounds=upcoming_codeforces())


@app.get("/coach", response_class=HTMLResponse)
def coach(request: Request):
    return render(request, "coach.html")


def _paper_for_today():
    snap = store.snapshot()
    mids = []
    if snap.get("today"):
        mids = list(dict.fromkeys(t.get("module_id") for t in snap["today"]["tasks"] if t.get("module_id")))
    if not mids:
        mids = [r["id"] for r in (snap["classified"].get("weak") or [])[:2]] or ["bootcamp"]
    qs = pick_drills(mids, store.state.get("drills_solved") or {}, snap["classified"].get("learner"), n=5)
    return [public_drill(q) for q in qs], [q["id"] for q in qs]


@app.get("/practice", response_class=HTMLResponse)
def practice_hub(request: Request, module: str | None = None):
    mid = module if module in {m["id"] for m in MODULES} else None
    rows = drills_for_module(mid) if mid else list(DRILLS)
    listed = []
    for d in rows:
        listed.append({**public_drill(d), "status": store.drill_status(d["id"])})
    return render(
        request,
        "practice.html",
        listed=listed,
        filter_module=mid,
        solved_n=len(store.state.get("drills_solved") or {}),
        total_n=len(DRILLS),
    )


@app.get("/practice/daily", response_class=HTMLResponse)
def practice_daily(request: Request):
    questions, qids = _paper_for_today()
    return render(
        request,
        "try_paper.html",
        questions=questions,
        qids=qids,
        title="Daily exam — try here, we grade it",
        action="/practice/daily",
    )


@app.post("/practice/daily")
async def practice_daily_submit(request: Request):
    form = await request.form()
    qids = [s for s in str(form.get("qids") or "").split(",") if s]
    results = []
    for qid in qids:
        q = drill_by_id(qid)
        if not q:
            continue
        given = str(form.get(qid) or "")
        code = str(form.get(qid + "_code") or "")
        results.append(grade(q, given, code=code))
    store.record_drills(results)
    awarded = sum(r["score"] for r in results)
    total = max(1, len(results))
    percent = round(100 * awarded / total, 1)
    snap = store.snapshot()
    return templates.TemplateResponse(
        request,
        "try_result.html",
        {
            "snap": snap,
            "results": results,
            "percent": percent,
            "awarded": round(awarded, 1),
            "total": total,
            "kind": "daily",
        },
    )


@app.get("/practice/{qid}", response_class=HTMLResponse)
def practice_one(request: Request, qid: str):
    q = drill_by_id(qid)
    if not q:
        return RedirectResponse("/practice", status_code=303)
    return render(request, "try.html", q=public_drill(q), status=store.drill_status(qid))


@app.post("/practice/{qid}")
async def practice_one_submit(request: Request, qid: str):
    q = drill_by_id(qid)
    if not q:
        return RedirectResponse("/practice", status_code=303)
    form = await request.form()
    given = str(form.get("answer") or "")
    code = str(form.get("code") or "")
    result = grade(q, given, code=code)
    store.record_drills([result])
    snap = store.snapshot()
    return templates.TemplateResponse(
        request,
        "try_result.html",
        {
            "snap": snap,
            "results": [result],
            "percent": round(100 * result["score"], 1),
            "awarded": result["score"],
            "total": 1,
            "kind": "single",
            "next_id": qid,
            "q": public_drill(q),
        },
    )


@app.get("/profile")
def profile_get():
    return RedirectResponse("/camp#plan", status_code=303)


@app.post("/profile")
async def profile(request: Request):
    form = await request.form()
    store.set_profile(
        {
            "handle": str(form.get("handle") or ""),
            "goal": str(form.get("goal") or "cf-1400"),
            "contest_date": str(form.get("contest_date") or ""),
            "hours_per_day": str(form.get("hours_per_day") or "2"),
            "strong_modules": [str(v) for v in form.getlist("strong")],
            "weak_modules": [str(v) for v in form.getlist("weak")],
            "reset": form.get("reset") == "1",
        }
    )
    return RedirectResponse("/camp?rebuilt=1", status_code=303)
