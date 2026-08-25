import hmac
import json
import os
import secrets
import sqlite3
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path

from flask import Flask, Response, abort, jsonify, redirect, render_template, request, session, url_for

from questions import READINESS_WEIGHTS, SECTIONS, all_questions, question_map

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
    "slug": os.getenv("PROJECT_SLUG", "voyage"),
    "name": os.getenv("PROJECT_NAME", "VOYAGE"),
    "name_ar": os.getenv("PROJECT_NAME_AR", "ڤوياج للسفر والسياحة"),
    "subtitle": os.getenv("PROJECT_SUBTITLE", "مرحلة اكتشاف المتطلبات قبل بناء الـ PRD"),
}

STATUS_LABELS = {
    "new": "جديد",
    "reviewing": "قيد المراجعة",
    "prd_ready": "جاهز للـ PRD",
    "closed": "مغلق",
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


def normalize_answers(answers):
    qmap = question_map()
    clean = {}
    for qid, question in qmap.items():
        value = answers.get(qid)
        qtype = question.get("type")
        if qtype == "checkboxes":
            clean[qid] = [str(v).strip() for v in value] if isinstance(value, list) else []
        elif qtype == "checkbox":
            clean[qid] = value is True
        else:
            clean[qid] = str(value or "").strip()
    return clean


def validate_payload(payload):
    if not isinstance(payload, dict):
        return ["صيغة البيانات غير صحيحة"]

    answers = payload.get("answers")
    if not isinstance(answers, dict):
        return ["الإجابات غير موجودة"]

    errors = []
    qmap = question_map()

    for qid in required_question_ids():
        question = qmap[qid]
        if not answer_present(question, answers.get(qid)):
            errors.append(f"الحقل مطلوب: {question['label']}")

    for qid, value in answers.items():
        question = qmap.get(qid)
        if not question:
            continue
        qtype = question.get("type")
        if isinstance(value, str) and len(value) > 8000:
            errors.append(f"الإجابة طويلة جداً: {question['label']}")
        if qtype == "checkboxes":
            if not isinstance(value, list) or len(value) > 30:
                errors.append(f"عدد الاختيارات غير صحيح: {question['label']}")
            else:
                allowed = set(question.get("options", []))
                if any(item not in allowed for item in value):
                    errors.append(f"يوجد اختيار غير صحيح في: {question['label']}")
        if qtype in ("radio", "select") and value:
            if value not in question.get("options", []):
                errors.append(f"الاختيار غير صحيح: {question['label']}")
        if qtype == "email" and value and ("@" not in value or len(value) > 254):
            errors.append("البريد الإلكتروني غير صحيح")

    return errors


def generate_reference():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"DSC-{stamp}-{secrets.token_hex(3).upper()}"


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


def discovery_analysis(answers):
    qmap = question_map()
    score = 0
    total = sum(READINESS_WEIGHTS.values()) or 1
    missing = []

    for qid, weight in READINESS_WEIGHTS.items():
        question = qmap.get(qid, {"id": qid, "label": qid})
        if answer_present(question, answers.get(qid)):
            score += weight
        else:
            missing.append(
                {
                    "id": qid,
                    "label": question.get("label", qid),
                    "prompt": question.get("gap_prompt", f"نحتاج توضيح: {question.get('label', qid)}"),
                    "weight": weight,
                }
            )

    percent = round((score / total) * 100)
    missing.sort(key=lambda item: item["weight"], reverse=True)

    if percent >= 85:
        label = "ممتاز — جاهز لجلسة PRD"
        tone = "good"
    elif percent >= 70:
        label = "جيد — يحتاج إقفال نقاط محددة"
        tone = "warn"
    else:
        label = "يحتاج استكمال قبل بناء PRD"
        tone = "risk"

    groups = [
        ("problem", "المشكلة", ["core_problem", "pain_points"]),
        ("workflow", "الوضع الحالي", ["current_process"]),
        ("outcome", "النتيجة", ["desired_outcome", "success_metrics"]),
        ("scope", "نطاق V1", ["must_haves", "users"]),
    ]
    signals = []
    for key, label_text, ids in groups:
        complete = sum(1 for qid in ids if answer_present(qmap[qid], answers.get(qid)))
        signals.append(
            {
                "key": key,
                "label": label_text,
                "complete": complete,
                "total": len(ids),
                "ready": complete == len(ids),
            }
        )

    return {
        "score": percent,
        "label": label,
        "tone": tone,
        "missing": missing,
        "next_questions": [item["prompt"] for item in missing[:5]],
        "signals": signals,
        "answered_count": sum(1 for q in all_questions() if answer_present(q, answers.get(q["id"]))),
        "total_questions": len(all_questions()),
    }


def submission_markdown(row):
    payload = json.loads(row["payload"])
    answers = payload.get("answers", {})
    analysis = discovery_analysis(answers)
    company = answer_to_text(answers.get("company_name")) or "-"

    lines = [
        f"# Discovery Brief — {row['id']}",
        "",
        "> هذا المستند مدخل لمرحلة التحليل وبناء PRD، وليس نطاقاً معتمداً أو عرض سعر.",
        "",
        "## معلومات أساسية",
        "",
        f"- الجهة: {company}",
        f"- المسؤول: {row['contact_name'] or '-'}",
        f"- البريد: {row['contact_email'] or '-'}",
        f"- تاريخ الإرسال: {row['created_at']}",
        f"- جاهزية الاكتشاف: {analysis['score']}% — {analysis['label']}",
        "",
        "## Executive Snapshot",
        "",
        f"### المشكلة الأساسية\n{answer_to_text(answers.get('core_problem')) or '-'}",
        "",
        f"### طريقة العمل الحالية\n{answer_to_text(answers.get('current_process')) or '-'}",
        "",
        f"### النتيجة المطلوبة\n{answer_to_text(answers.get('desired_outcome')) or '-'}",
        "",
        f"### أهم متطلبات النسخة الأولى\n{answer_to_text(answers.get('must_haves')) or '-'}",
        "",
        "## أسئلة يجب إقفالها قبل اعتماد PRD",
        "",
    ]

    if analysis["next_questions"]:
        lines.extend(f"- {question}" for question in analysis["next_questions"])
    else:
        lines.append("- لا توجد فجوات أساسية ظاهرة من النموذج. راجع الافتراضات في جلسة Discovery.")

    lines.extend(["", "## إجابات العميل", ""])
    for section in SECTIONS:
        lines.append(f"### {section['title']}")
        lines.append("")
        for q in section["questions"]:
            value = answers.get(q["id"])
            if value in (None, "", [], False):
                continue
            lines.append(f"**{q['label']}**")
            lines.append("")
            lines.append(answer_to_text(value))
            lines.append("")

    lines.extend(
        [
            "## ملاحظات الفريق قبل كتابة PRD",
            "",
            "- [ ] تأكيد المشكلة والهدف التجاري مع العميل.",
            "- [ ] فصل Must-have عن Nice-to-have.",
            "- [ ] توثيق Out of Scope بوضوح.",
            "- [ ] تأكيد المستخدمين والصلاحيات والتكاملات.",
            "- [ ] تحويل المتطلبات إلى Acceptance Criteria قابلة للاختبار.",
            "- [ ] توثيق الافتراضات والمخاطر والأسئلة المفتوحة.",
            "",
        ]
    )
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
    if request.path.startswith("/admin"):
        response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/")
def index():
    return render_template("index.html", project=PROJECT, sections=SECTIONS)


@app.post("/api/submissions")
def create_submission():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"ok": False, "errors": ["تعذر قراءة البيانات"]}), 400

    if str(data.get("website", "")).strip():
        return jsonify({"ok": True, "reference": "RECEIVED"}), 200

    errors = validate_payload(data)
    if errors:
        return jsonify({"ok": False, "errors": errors[:12]}), 422

    answers = normalize_answers(data["answers"])
    clean_payload = {
        "answers": answers,
        "meta": data.get("meta", {}) if isinstance(data.get("meta"), dict) else {},
    }
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
                answers.get("contact_name", ""),
                answers.get("contact_email", ""),
                "",
                json.dumps(clean_payload, ensure_ascii=False),
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
        rows = conn.execute("SELECT * FROM submissions ORDER BY created_at DESC").fetchall()

    items = []
    for row in rows:
        try:
            payload = json.loads(row["payload"])
            answers = payload.get("answers", {})
        except (TypeError, json.JSONDecodeError):
            answers = {}
        items.append(
            {
                "row": row,
                "company_name": answer_to_text(answers.get("company_name")) or "-",
                "analysis": discovery_analysis(answers),
            }
        )

    return render_template(
        "admin_dashboard.html",
        project=PROJECT,
        items=items,
        status_labels=STATUS_LABELS,
    )


@app.get("/admin/submissions/<submission_id>")
@admin_required
def admin_submission(submission_id):
    with db_connection() as conn:
        row = conn.execute("SELECT * FROM submissions WHERE id = ?", (submission_id,)).fetchone()
    if not row:
        abort(404)
    payload = json.loads(row["payload"])
    answers = payload.get("answers", {})
    return render_template(
        "admin_submission.html",
        project=PROJECT,
        submission=row,
        answers=answers,
        sections=SECTIONS,
        analysis=discovery_analysis(answers),
        answer_to_text=answer_to_text,
        status_labels=STATUS_LABELS,
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
        headers={"Content-Disposition": f'attachment; filename="{submission_id}-discovery-brief.md"'},
    )


@app.errorhandler(413)
def too_large(_):
    return jsonify({"ok": False, "errors": ["حجم الطلب أكبر من الحد المسموح"]}), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")), debug=False)
