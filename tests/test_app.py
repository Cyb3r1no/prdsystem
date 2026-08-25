import json
import os
from pathlib import Path

os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ADMIN_TOKEN", "test-admin-token")

import app as app_module
from questions import all_questions


def valid_answers():
    answers = {}
    for q in all_questions():
        if q["type"] == "checkbox":
            answers[q["id"]] = True
        elif q["type"] == "checkboxes":
            answers[q["id"]] = [q["options"][0]]
        elif q["type"] in ("radio", "select"):
            answers[q["id"]] = q.get("options", ["اختبار"])[0]
        elif q["id"] == "contact_email":
            answers[q["id"]] = "client@example.com"
        else:
            answers[q["id"]] = "إجابة اختبار"
    return answers


def setup_test_db(tmp_path):
    app_module.DB_PATH = Path(tmp_path) / "test.db"
    app_module.init_db()
    app_module.app.config.update(TESTING=True)
    return app_module.app.test_client()


def test_public_pages_submission_and_admin(tmp_path):
    client = setup_test_db(tmp_path)

    home = client.get("/")
    assert home.status_code == 200
    body = home.get_data(as_text=True)
    assert "Project Discovery" in body
    assert "المشكلة" in body

    health = client.get("/health")
    assert health.status_code == 200
    assert health.get_json()["ok"] is True

    bad = client.post("/api/submissions", json={"answers": {}})
    assert bad.status_code == 422

    created = client.post(
        "/api/submissions",
        json={"answers": valid_answers(), "website": "", "meta": {"formVersion": "test"}},
    )
    assert created.status_code == 200
    reference = created.get_json()["reference"]
    assert reference.startswith("DSC-")

    login = client.post("/admin/login", data={"token": "test-admin-token"}, follow_redirects=True)
    assert login.status_code == 200
    dashboard = login.get_data(as_text=True)
    assert reference in dashboard
    assert "Discovery Inbox" in dashboard

    detail = client.get(f"/admin/submissions/{reference}")
    assert detail.status_code == 200
    detail_body = detail.get_data(as_text=True)
    assert "Discovery Readiness" in detail_body
    assert "أسئلة لازم نقفلها" in detail_body

    markdown = client.get(f"/admin/submissions/{reference}/export.md")
    assert markdown.status_code == 200
    md = markdown.get_data(as_text=True)
    assert reference in md
    assert "Executive Snapshot" in md
    assert "ملاحظات الفريق قبل كتابة PRD" in md


def test_payload_is_normalized_and_invalid_choice_rejected(tmp_path):
    client = setup_test_db(tmp_path)
    answers = valid_answers()
    answers["users"] = ["اختيار غير موجود"]
    invalid = client.post("/api/submissions", json={"answers": answers, "website": ""})
    assert invalid.status_code == 422

    answers = valid_answers()
    payload = {"answers": {**answers, "unexpected_field": "should not persist"}, "website": ""}
    created = client.post("/api/submissions", json=payload)
    assert created.status_code == 200
    reference = created.get_json()["reference"]

    with app_module.db_connection() as conn:
        row = conn.execute("SELECT payload FROM submissions WHERE id = ?", (reference,)).fetchone()
    stored = json.loads(row["payload"])
    assert "unexpected_field" not in stored["answers"]
