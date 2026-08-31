import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert "name" in data
    assert "version" in data
    assert "endpoints" in data


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_patterns():
    r = client.get("/patterns")
    assert r.status_code == 200
    data = r.json()
    assert "patterns" in data
    assert "total" in data
    assert data["total"] == 22


def test_analyze_log():
    payload = {
        "input_type": "log",
        "content": "password=EXAMPLEPASS\napi_key=sk-EXAMPLE000000000\nemail=test@example.com",
        "options": {"mask": True, "use_ai": False, "block_high_risk": True},
    }
    r = client.post("/analyze", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "findings" in data
    assert "risk_level" in data
    assert "risk_score" in data
    assert "action" in data
    assert isinstance(data["findings"], list)
    assert data["risk_score"] > 0


def test_analyze_text():
    payload = {
        "input_type": "text",
        "content": "Contact me at john@example.com or call +1-555-123-4567",
        "options": {"mask": True, "use_ai": False, "block_high_risk": False},
    }
    r = client.post("/analyze", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "findings" in data
    assert len(data["findings"]) >= 1


def test_analyze_empty_content():
    payload = {
        "input_type": "text",
        "content": "   ",
    }
    r = client.post("/analyze", json=payload)
    assert r.status_code == 422


def test_analyze_invalid_input_type():
    payload = {
        "input_type": "invalid_type",
        "content": "sample content",
    }
    r = client.post("/analyze", json=payload)
    assert r.status_code == 422
