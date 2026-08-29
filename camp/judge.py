"""Grade MCQ, short answers, and small Python programs against hidden tests."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

BANNED = re.compile(
    r"\b(subprocess|socket|pathlib|shutil|ctypes|multiprocessing|pty|"
    r"webbrowser|http\.client|urllib|requests|pickle|marshal|"
    r"__import__|eval\s*\(|exec\s*\(|compile\s*\(|open\s*\()\b"
    r"|import\s+os\b|from\s+os\b"
)


def _norm_text(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def _norm_out(value: str) -> str:
    lines = [(ln.rstrip()) for ln in (value or "").replace("\r\n", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def grade_mcq(question: dict, given: str) -> dict:
    ok = (given or "").strip() == str(question["answer"]).strip()
    return {
        "correct": ok,
        "score": 1.0 if ok else 0.0,
        "feedback": "Correct." if ok else f"Expected {question['answer']}. {question.get('explanation', '')}",
        "given": given or "",
    }


def grade_short(question: dict, given: str) -> dict:
    raw = (given or "").strip()
    if not raw:
        return {"correct": False, "score": 0.0, "feedback": "Blank. Attempt even a partial answer.", "given": ""}
    want = _norm_text(str(question["answer"]))
    got = _norm_text(raw)
    if got == want or want in got or got in want:
        return {"correct": True, "score": 1.0, "feedback": "Correct.", "given": raw}
    keys = [_norm_text(k) for k in question.get("keywords") or []]
    hits = sum(1 for k in keys if k and k in got)
    if keys and hits >= max(1, (len(keys) + 1) // 2):
        return {
            "correct": True,
            "score": 0.7,
            "feedback": "Close enough on the key idea. Full answer: " + str(question["answer"]),
            "given": raw,
        }
    return {
        "correct": False,
        "score": 0.0,
        "feedback": f"Expected {question['answer']}. {question.get('explanation', '')}",
        "given": raw,
    }


def _preflight(code: str) -> str | None:
    if not (code or "").strip():
        return "No code submitted."
    if len(code) > 20_000:
        return "Program is too long for this drill."
    if BANNED.search(code):
        return "This drill only allows pure Python (math, collections, itertools, heapq, bisect). Remove file/network/os calls."
    return None


def run_python(code: str, stdin: str, timeout: float = 1.5) -> dict:
    err = _preflight(code)
    if err:
        return {"ok": False, "stdout": "", "stderr": err, "timed_out": False}
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "solve.py"
        path.write_text(code, encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, "-I", "-S", str(path)],
                input=stdin.encode("utf-8"),
                capture_output=True,
                timeout=timeout,
                cwd=tmp,
            )
        except subprocess.TimeoutExpired:
            return {"ok": False, "stdout": "", "stderr": "Time limit (1.5s).", "timed_out": True}
        stdout = proc.stdout.decode("utf-8", errors="replace")
        stderr = proc.stderr.decode("utf-8", errors="replace")
        return {
            "ok": proc.returncode == 0,
            "stdout": stdout,
            "stderr": stderr.strip()[:800],
            "timed_out": False,
        }


def grade_code(question: dict, code: str) -> dict:
    tests = question.get("tests") or []
    passed = 0
    details = []
    last_err = ""
    for i, t in enumerate(tests, 1):
        run = run_python(code, t.get("stdin", ""))
        got = _norm_out(run["stdout"])
        want = _norm_out(t.get("stdout", ""))
        ok = run["ok"] and got == want
        if ok:
            passed += 1
            details.append({"i": i, "ok": True, "hidden": t.get("hidden", False)})
        else:
            last_err = run["stderr"] or (f"Wrong answer. Expected:\n{want}\nGot:\n{got}" if not t.get("hidden") else "Wrong answer on a hidden test.")
            details.append({"i": i, "ok": False, "hidden": t.get("hidden", False), "stderr": last_err})
            # keep going so they see how many passed
    n = max(1, len(tests))
    score = passed / n
    correct = passed == n
    if correct:
        feedback = f"Accepted. {passed}/{n} tests."
    elif passed:
        feedback = f"{passed}/{n} tests passed. {last_err}"
    else:
        feedback = last_err or "No tests passed."
    return {
        "correct": correct,
        "score": round(score, 2),
        "feedback": feedback,
        "given": "(python program)",
        "passed": passed,
        "total_tests": n,
        "details": details,
    }


def grade(question: dict, given: str, code: str | None = None) -> dict:
    kind = question.get("type") or "short"
    if kind == "mcq":
        result = grade_mcq(question, given)
    elif kind == "code":
        result = grade_code(question, code or given)
    else:
        result = grade_short(question, given)
    result["question_id"] = question["id"]
    result["module_id"] = question["module_id"]
    result["title"] = question["title"]
    result["type"] = kind
    return result
