import pytest
from unittest.mock import patch
from main import run, extract_events, classify_severity, generate_summary, main


def test_run():
    assert "Incident Summarizer" in run("test")


def test_extract_error():
    events = extract_events("2024-01-15T10:30:00 ERROR: connection failed")
    assert len(events) == 1
    assert events[0]["category"] == "ERROR"
    assert events[0]["timestamp"] == "2024-01-15T10:30:00"


def test_extract_timeout():
    events = extract_events("Request timed out after 30s")
    assert any(e["category"] == "TIMEOUT" for e in events)


def test_extract_oom():
    events = extract_events("MemoryError: out of memory")
    assert any(e["category"] == "OOM" for e in events)


def test_no_events():
    events = extract_events("all good\nnothing here")
    assert len(events) == 0


def test_classify_critical():
    events = [{"category": "OOM"}]
    assert classify_severity(events) == "CRITICAL"


def test_classify_high_timeout():
    events = [{"category": "TIMEOUT"}]
    assert classify_severity(events) == "HIGH"


def test_classify_high_errors():
    events = [{"category": "ERROR"}] * 11
    assert classify_severity(events) == "HIGH"


def test_classify_medium():
    events = [{"category": "ERROR"}] * 5
    assert classify_severity(events) == "MEDIUM"


def test_classify_low():
    events = [{"category": "HTTP_4XX"}]
    assert classify_severity(events) == "LOW"


def test_summary_clean():
    assert "No incidents" in generate_summary([])


def test_summary_with_events():
    events = [{"line": 1, "category": "ERROR", "timestamp": None, "content": "crash"}]
    summary = generate_summary(events)
    assert "Incident Summary" in summary


def test_summary_more_than_5_events():
    events = [{"line": i, "category": "ERROR", "timestamp": "2024-01-01T00:00:00", "content": f"crash {i}"} for i in range(10)]
    summary = generate_summary(events)
    assert "... and 5 more" in summary


@patch("sys.argv", ["main.py"])
def test_main_no_args(capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out


@patch("sys.argv", ["main.py", "non_existent.log"])
def test_main_bad_file(capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "not found" in captured.out


def test_main_success(capsys, tmp_path):
    p = tmp_path / "app.log"
    p.write_text("ERROR: failed")
    with patch("sys.argv", ["main.py", str(p)]):
        main()
    captured = capsys.readouterr()
    assert "Incident Summary" in captured.out
