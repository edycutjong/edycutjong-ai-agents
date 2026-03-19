from lib.scorer import calculate_total_risk

def test_calculate_total_risk_no_files():
    result = calculate_total_risk([], "test@example.com", ".", {})
    assert result["score"] == 0.0
    assert result["criticality"] == 0.0
    
def test_calculate_total_risk_with_files(mocker):
    mocker.patch("lib.scorer.calculate_criticality_score", return_value=20.0)
    mocker.patch("lib.scorer.calculate_blast_radius_score", return_value=30.0)
    mocker.patch("lib.scorer.calculate_coverage_gap_score", return_value=10.0)
    mocker.patch("lib.scorer.calculate_history_risk_score", return_value=20.0)
    mocker.patch("lib.scorer.calculate_familiarity_discount", return_value=5.0)
    
    result = calculate_total_risk(["src/main.py"], "test@example.com", ".", {})
    assert result["score"] == 75.0 # 20+30+10+20-5
    
def test_calculate_total_risk_capped(mocker):
    mocker.patch("lib.scorer.calculate_criticality_score", return_value=50.0)
    mocker.patch("lib.scorer.calculate_blast_radius_score", return_value=50.0)
    mocker.patch("lib.scorer.calculate_coverage_gap_score", return_value=20.0)
    mocker.patch("lib.scorer.calculate_history_risk_score", return_value=20.0)
    mocker.patch("lib.scorer.calculate_familiarity_discount", return_value=0.0)
    
    result = calculate_total_risk(["src/main.py"], "test@example.com", ".", {})
    assert result["score"] == 100.0 # Capped at 100
    
def test_calculate_total_risk_floor(mocker):
    mocker.patch("lib.scorer.calculate_criticality_score", return_value=0.0)
    mocker.patch("lib.scorer.calculate_blast_radius_score", return_value=0.0)
    mocker.patch("lib.scorer.calculate_coverage_gap_score", return_value=0.0)
    mocker.patch("lib.scorer.calculate_history_risk_score", return_value=0.0)
    mocker.patch("lib.scorer.calculate_familiarity_discount", return_value=10.0)
    
    result = calculate_total_risk(["src/main.py"], "test@example.com", ".", {})
    assert result["score"] == 0.0 # Floored at 0
