"""Tests for Competitive Analysis Agent."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.analyzer import (
    Competitor, run_analysis, build_feature_matrix, find_market_gaps,
    find_unique_advantages, score_competitor, generate_recommendations,
    format_report_markdown,
)

YOUR = Competitor(name="MyApp", features=["Auth", "API", "Dashboard", "Mobile"], target_market="SMB", differentiators=["AI-powered"])
COMP_A = Competitor(name="CompA", features=["Auth", "API", "Billing", "Reporting"], pricing="$49/mo")
COMP_B = Competitor(name="CompB", features=["Auth", "API", "Billing", "Dashboard", "Webhooks"], pricing="$99/mo")
COMP_C = Competitor(name="CompC", features=["Auth", "Billing", "Reporting"])

# --- Feature Matrix ---
def test_feature_matrix():
    matrix = build_feature_matrix(YOUR, [COMP_A, COMP_B])
    assert "Auth" in matrix
    assert matrix["Auth"]["your_product"] is True
    assert matrix["Auth"]["CompA"] is True

def test_feature_matrix_missing():
    matrix = build_feature_matrix(YOUR, [COMP_A])
    assert matrix["Dashboard"]["CompA"] is False

# --- Market Gaps ---
def test_market_gaps():
    gaps = find_market_gaps(YOUR, [COMP_A, COMP_B, COMP_C])
    gap_text = " ".join(gaps).lower()
    assert "billing" in gap_text  # 3/3 competitors have it

def test_no_gaps_when_all_features():
    comp = Competitor(name="Weak", features=[])
    gaps = find_market_gaps(YOUR, [comp])
    assert len(gaps) == 0

# --- Unique Advantages ---
def test_unique_advantages():
    unique = find_unique_advantages(YOUR, [COMP_A, COMP_B])
    assert "Mobile" in unique

def test_no_unique_when_all_shared():
    same = Competitor(name="Same", features=["Auth", "API", "Dashboard", "Mobile"])
    unique = find_unique_advantages(YOUR, [same])
    assert len(unique) == 0

# --- Scoring ---
def test_score_competitor():
    scores = score_competitor(COMP_A)
    assert "overall" in scores
    assert 0 <= scores["overall"] <= 100

def test_score_feature_breadth():
    scores = score_competitor(Competitor(name="Rich", features=list(range(10))))
    assert scores["feature_breadth"] == 100

# --- Recommendations ---
def test_recommendations():
    recs = generate_recommendations(YOUR, [COMP_A, COMP_B, COMP_C])
    assert len(recs) >= 1

def test_recs_no_differentiators():
    no_diff = Competitor(name="Plain", features=["Auth"])
    recs = generate_recommendations(no_diff, [COMP_A])
    assert any("differentiator" in r.lower() for r in recs)

def test_recs_no_target():
    no_target = Competitor(name="Vague", features=["Auth"])
    recs = generate_recommendations(no_target, [COMP_A])
    assert any("target" in r.lower() for r in recs)

# --- Full Analysis ---
def test_run_analysis():
    report = run_analysis(YOUR, [COMP_A, COMP_B])
    assert report.your_product.name == "MyApp"
    assert len(report.feature_matrix) > 0

def test_report_to_dict():
    report = run_analysis(YOUR, [COMP_A])
    d = report.to_dict()
    assert "your_product" in d
    assert "competitors" in d

# --- Formatting ---
def test_format_markdown():
    report = run_analysis(YOUR, [COMP_A, COMP_B])
    md = format_report_markdown(report)
    assert "Competitive Analysis" in md
    assert "MyApp" in md
    assert "✅" in md

# --- Serialization ---
def test_competitor_roundtrip():
    d = YOUR.to_dict()
    restored = Competitor.from_dict(d)
    assert restored.name == "MyApp"

def test_empty_competitors():
    report = run_analysis(YOUR, [])
    assert len(report.feature_matrix) > 0
