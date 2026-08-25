import hashlib
import hmac
import json
import os
import secrets
import sqlite3
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path

from flask import Flask, Response, abort, jsonify, redirect, render_template, request, session, url_for

from questions import SECTIONS, all_questions, question_map

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "prdsystem.db"

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("SECRET_KEY", secrets.token_hex(32)),
    MAX_CONTENT_LENGTH=1024 * 1024,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("COOKIE_SECURE", "0") == "1",
)

PROJECT = {
    "slug": "voyage",
    "name": "VOYAGE",
    "name_ar": "ڤوياج للسفر والسياحة",
    "subtitle": "مرحلة اكتشاف المتطلبات وبناء تصور المشروع",
}


def db_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS submissions (
                id TEXT PRIMARY KEY,
                project_slug TEXT NOT NULL,
                contact_name TEXT,
                contact_email TEXT,
                contact_phone TEXT,
                status TEXT NOT NULL DEFAULT 'new',
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_submissions_created_at ON submissions(created_at DESC)")
        conn.commit()


init_db()


def required_question_ids():
    return {q["id"] for q in all_questions() if q.get("required")}


def answer_present(question, value):
    qtype = question.get("type")
    if qtype == "checkbox":
        return value is True
    if qtype == "checkboxes":
        return isinstance(value, list) and len(value) > 0
    return isinstance(value, str) and bool(value.strip())


def validate_payload(payload):
    if not isinstance(payload, dict):
        return ["صيغة البيانات غير صحيحة"]

    answers = payload.get("answers")
    if not isinstance(answers, dict):
        return ["الإجابات غير موجودة"]

    errors = []
    qmap = question_map()
    for qid in required_question_ids():
        q = qmap[qid]
        if not answer_present(q, answers.get(qid)):
            errors.append(f"الحقل مطلوب: {q['label']}")

    for qid, value in answers.items():
        if qid not in qmap:
            continue
        if isinstance(value, str) and len(value) > 8000:
            errors.append(f"الإجابة طويلة جداً: {qmap[qid]['label']}")
        if isinstance(value, list) and len(value) > 30:
            errors.append(f"عدد الاختيارات غير صحيح: {qmap[qid]['label']}")

    return errors


def generate_reference():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"VOY-{stamp}-{secrets.token_hex(3).upper()}"


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def safe_admin_token():
    return os.getenv("ADMIN_TOKEN", "")


def answer_to_text(value):
    if isinstance(value, list):
        return "، ".join(str(v) for v in value)
    if isinstance(value, bool):
        return "نعم" if value else "لا"
    return str(value or "")


def submission_markdown(row):
    payload = json.loads(row["payload"])
    answers = payload.get("answers", {})
    lines = [
        f"# VOYAGE Discovery — {row['id']}",
        "",
        f"- الحالة: {row['status']}",
        f"- تاريخ الإرسال: {row['created_at']}",
        f"- المسؤول: {row['contact_name'] or '-'}",
        f"- البريد: {row['contact_email'] or '-'}",
        f"- الجوال: {row['contact_phone'] or '-'}",
        "",
        "> هذه المادة خام لمرحلة Discovery وتحتاج تحليل قبل تحويلها إلى PRD.",
        "",
    ]

    for section in SECTIONS:
        lines.append(f"## {section['title']}")
        lines.append("")
        for q in section["questions"]:
            value = answers.get(q["id"])
            if value in (None, "", [], False):
                continue
            lines.append(f"### {q['label']}")
            lines.append(answer_to_text(value))
            lines.append("")
    return "\n".join(lines)


@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; img-src 'self' data:; style-src 'self'; "
        "script-src 'self'; connect-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'"
    )
    return response


@app.get("/")
def index():
    return render_template("index.html", project=PROJECT, sections=SECTIONS)


@app.post("/api/submissions")
def create_submission():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"ok": False, "errors": ["تعذر قراءة البيانات"]}), 400

    # Honeypot field. Bots often fill hidden fields.
    if str(data.get("website", "")).strip():
        return jsonify({"ok": True, "reference": "RECEIVED"}), 200

    errors = validate_payload(data)
    if errors:
        return jsonify({"ok": False, "errors": errors[:12]}), 422

    answers = data["answers"]
    reference = generate_reference()
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    with db_connection() as conn:
        conn.execute(
            """
            INSERT INTO submissions
            (id, project_slug, contact_name, contact_email, contact_phone, status, payload, created_at)
            VALUES (?, ?, ?, ?, ?, 'new', ?, ?)
            """,
            (
                reference,
                PROJECT["slug"],
                str(answers.get("contact_name", "")).strip(),
                str(answers.get("contact_email", "")).strip(),
                str(answers.get("contact_phone", "")).strip(),
                json.dumps(data, ensure_ascii=False),
                created_at,
            ),
        )
        conn.commit()

    return jsonify({"ok": True, "reference": reference})


@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "prdsystem", "project": PROJECT["slug"]})


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        supplied = request.form.get("token", "")
        configured = safe_admin_token()
        if not configured:
            error = "ADMIN_TOKEN غير مضبوط على السيرفر."
        elif hmac.compare_digest(supplied, configured):
            session.clear()
            session["is_admin"] = True
            return redirect(request.args.get("next") or url_for("admin_dashboard"))
        else:
            error = "رمز الدخول غير صحيح."
    return render_template("admin_login.html", project=PROJECT, error=error)


@app.post("/admin/logout")
@admin_required
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


@app.get("/admin")
@admin_required
def admin_dashboard():
    with db_connection() as conn:
        rows = conn.execute(
            "SELECT id, contact_name, contact_email, contact_phone, status, created_at FROM submissions ORDER BY created_at DESC"
        ).fetchall()
    return render_template("admin_dashboard.html", project=PROJECT, submissions=rows)


@app.get("/admin/submissions/<submission_id>")
@admin_required
def admin_submission(submission_id):
    with db_connection() as conn:
        row = conn.execute("SELECT * FROM submissions WHERE id = ?", (submission_id,)).fetchone()
    if not row:
        abort(404)
    payload = json.loads(row["payload"])
    return render_template(
        "admin_submission.html",
        project=PROJECT,
        submission=row,
        answers=payload.get("answers", {}),
        sections=SECTIONS,
        answer_to_text=answer_to_text,
    )


@app.get("/admin/submissions/<submission_id>/export.json")
@admin_required
def export_json(submission_id):
    with db_connection() as conn:
        row = conn.execute("SELECT * FROM submissions WHERE id = ?", (submission_id,)).fetchone()
    if not row:
        abort(404)
    return Response(
        row["payload"],
        mimetype="application/json; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{submission_id}.json"'},
    )


@app.get("/admin/submissions/<submission_id>/export.md")
@admin_required
def export_markdown(submission_id):
    with db_connection() as conn:
        row = conn.execute("SELECT * FROM submissions WHERE id = ?", (submission_id,)).fetchone()
    if not row:
        abort(404)
    content = submission_markdown(row)
    return Response(
        content,
        mimetype="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{submission_id}.md"'},
    )


@app.errorhandler(413)
def too_large(_):
    return jsonify({"ok": False, "errors": ["حجم الطلب أكبر من الحد المسموح"]}), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")), debug=False)
