from main import run, extract_events, classify_severity, generate_summary


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


def test_classify_low():
    events = [{"category": "HTTP_4XX"}]
    assert classify_severity(events) == "LOW"


def test_summary_clean():
    assert "No incidents" in generate_summary([])


def test_summary_with_events():
    events = [{"line": 1, "category": "ERROR", "timestamp": None, "content": "crash"}]
    summary = generate_summary(events)
    assert "Incident Summary" in summary
