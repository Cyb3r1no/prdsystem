import os

os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ADMIN_TOKEN", "test-admin-token")

from app import app
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


def test_public_pages_and_submission():
    app.config.update(TESTING=True)
    client = app.test_client()

    home = client.get("/")
    assert home.status_code == 200
    assert "VOYAGE" in home.get_data(as_text=True)

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
    assert reference.startswith("VOY-")

    login = client.post("/admin/login", data={"token": "test-admin-token"}, follow_redirects=True)
    assert login.status_code == 200
    assert reference in login.get_data(as_text=True)

    detail = client.get(f"/admin/submissions/{reference}")
    assert detail.status_code == 200

    markdown = client.get(f"/admin/submissions/{reference}/export.md")
    assert markdown.status_code == 200
    assert reference in markdown.get_data(as_text=True)
