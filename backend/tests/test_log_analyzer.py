from app.modules.detection.log_analyzer import analyze_log, analyze_log_chunked

SAMPLE_LOG = """2026-03-10 10:00:01 INFO User login
email=admin@company.com
password=TEST_ONLY
api_key=sk-EXAMPLE000000000
ERROR stack trace: NullPointerException at service.java:45"""


def test_log_findings():
    result = analyze_log(SAMPLE_LOG)
    assert "findings" in result
    types = [f["type"] for f in result["findings"]]
    assert "email" in types
    assert "password" in types
    assert "api_key" in types
    risks = {f["type"]: f["risk"] for f in result["findings"]}
    assert risks.get("email") == "low"
    assert risks.get("password") == "critical"
    assert risks.get("api_key") == "high"


def test_log_chunked():
    result = analyze_log_chunked(SAMPLE_LOG, chunk_size=2)
    assert "findings" in result
    assert result["chunked"] is True
    assert result["total_lines"] > 0
