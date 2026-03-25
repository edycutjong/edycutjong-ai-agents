from main import run, analyze_diff, format_report


def test_run():
    assert "PR Risk Scorer" in run("test")


def test_small_diff():
    diff = "+++ b/readme.md\n+hello"
    result = analyze_diff(diff)
    assert result["score"] <= 3


def test_auth_change():
    diff = "diff --git a/auth.py b/auth.py\n+token = get_jwt()"
    result = analyze_diff(diff)
    signals = [s["signal"] for s in result["signals"]]
    assert "AUTH_CHANGES" in signals


def test_hardcoded_secret():
    diff = '+password = "mysupersecretpassword123"'
    result = analyze_diff(diff)
    signals = [s["signal"] for s in result["signals"]]
    assert "HARDCODED_SECRET" in signals


def test_large_diff():
    diff = "\n".join([f"+line {i}" for i in range(600)])
    result = analyze_diff(diff)
    assert result["score"] >= 3


def test_format_low():
    result = {"score": 1, "risk_level": "LOW", "files_changed": 1,
              "lines_added": 5, "lines_removed": 2, "signals": []}
    report = format_report(result)
    assert "LOW" in report


def test_format_signals():
    result = {"score": 8, "risk_level": "HIGH", "files_changed": 3,
              "lines_added": 100, "lines_removed": 50,
              "signals": [{"signal": "AUTH_CHANGES", "weight": 3, "detail": "detected"}]}
    report = format_report(result)
    assert "AUTH_CHANGES" in report
