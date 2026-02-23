"""Tests for OKR Tracker."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.tracker import Objective, KeyResult, OKRStore, get_summary, format_okrs_markdown

def test_kr_progress():
    kr = KeyResult(title="Revenue", target=100, current=75)
    assert kr.progress == 75.0

def test_kr_status_completed():
    kr = KeyResult(title="T", target=10, current=10)
    assert kr.status == "completed"

def test_kr_status_on_track():
    kr = KeyResult(title="T", target=100, current=80)
    assert kr.status == "on-track"

def test_kr_status_at_risk():
    kr = KeyResult(title="T", target=100, current=40)
    assert kr.status == "at-risk"

def test_kr_status_behind():
    kr = KeyResult(title="T", target=100, current=10)
    assert kr.status == "behind"

def test_kr_progress_capped():
    kr = KeyResult(title="T", target=50, current=100)
    assert kr.progress == 100

def test_obj_progress():
    o = Objective(title="Growth", key_results=[KeyResult(title="A", target=100, current=50), KeyResult(title="B", target=100, current=100)])
    assert o.progress == 75.0

def test_obj_no_krs():
    o = Objective(title="Empty")
    assert o.progress == 0

def test_obj_status():
    o = Objective(title="Growth", key_results=[KeyResult(title="A", target=100, current=80)])
    assert o.status == "on-track"

def test_obj_to_dict():
    o = Objective(title="Test", key_results=[KeyResult(title="KR1", target=10, current=5)])
    d = o.to_dict()
    assert d["title"] == "Test"
    assert len(d["key_results"]) == 1

def test_kr_to_dict():
    kr = KeyResult(title="KR", target=50, current=25)
    d = kr.to_dict()
    assert d["progress"] == 50.0

def test_store_add_get(tmp_path):
    s = OKRStore(filepath=str(tmp_path / "okrs.json"))
    o = Objective(title="Ship v2", key_results=[KeyResult(title="KR1", target=100, current=0)])
    s.add_objective(o)
    data = s.get_all()
    assert len(data) == 1
    assert data[0]["title"] == "Ship v2"

def test_store_update(tmp_path):
    s = OKRStore(filepath=str(tmp_path / "okrs.json"))
    kr = KeyResult(title="KR", target=100, current=0)
    o = Objective(id="obj1", title="Test", key_results=[kr])
    s.add_objective(o)
    ok = s.update_key_result("obj1", kr.id, 50)
    assert ok
    data = s.get_all()
    assert data[0]["key_results"][0]["current"] == 50

def test_store_update_not_found(tmp_path):
    s = OKRStore(filepath=str(tmp_path / "okrs.json"))
    assert not s.update_key_result("x", "y", 10)

def test_summary():
    objs = [{"status": "on-track", "progress": 70}, {"status": "behind", "progress": 20}]
    s = get_summary(objs)
    assert s["total"] == 2
    assert s["avg_progress"] == 45.0

def test_summary_empty():
    assert get_summary([])["total"] == 0

def test_format_markdown():
    objs = [Objective(title="Ship v2", key_results=[KeyResult(title="Revenue", target=100, current=75)]).to_dict()]
    md = format_okrs_markdown(objs)
    assert "OKR Dashboard" in md
    assert "Ship v2" in md
