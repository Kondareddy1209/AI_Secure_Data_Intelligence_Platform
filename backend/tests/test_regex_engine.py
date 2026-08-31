from app.modules.detection.regex_engine import detect_all, get_all_patterns


def test_detect_api_key_and_password_and_email_and_token():
    r1 = detect_all("sk-EXAMPLE000000000")
    assert any(f["type"] == "api_key" and f["risk"] == "high" for f in r1)

    r2 = detect_all("password=EXAMPLEPASS")
    assert any(f["type"] == "password" and f["risk"] == "critical" for f in r2)

    r3 = detect_all("test@example.com")
    assert any(f["type"] == "email" and f["risk"] == "low" for f in r3)

    r4 = detect_all("bearer eyJhbGciOiJIUzI1NiJ9")
    assert any(f["type"] == "bearer_token" and f["risk"] == "high" for f in r4)

    r5 = detect_all("token=MY_SECRET_TOKEN_VALUE")
    assert any(f["type"] == "token" and f["risk"] == "high" for f in r5)


def test_get_all_patterns():
    patterns = get_all_patterns()
    assert isinstance(patterns, dict)
    assert len(patterns) == 22
    assert "password" in patterns
    assert "api_key" in patterns
    assert "email" in patterns
