from lib.history import calculate_history_risk_score, calculate_familiarity_discount

def test_calculate_history_risk_score(mocker):
    config = {
        "scoring": {
            "max_history_risk_score": 20.0
        }
    }
    
    files = ["src/auth.py", "src/main.py"]
    score = calculate_history_risk_score(files, "test@example.com", ".", config)
    # Default is penalty 0.5 * max_score (20) = 10.0
    assert score == 10.0

def test_calculate_history_risk_score_no_files():
    score = calculate_history_risk_score([], "test@example.com", ".", {})
    assert score == 0.0

def test_calculate_history_risk_score_subprocess_error(mocker):
    files = ["src/main.py"]
    score = calculate_history_risk_score(files, "test@example.com", ".", {})
    assert score == 10.0

def test_calculate_familiarity_discount(mocker):
    config = {
        "scoring": {
            "familiarity_discount_max": 20.0
        }
    }
    
    discount = calculate_familiarity_discount("test@example.com", ".", config)
    # Default factor 0.5 * 20 = 10.0
    assert discount == 10.0

def test_calculate_familiarity_discount_empty_email():
    discount = calculate_familiarity_discount("", ".", {})
    assert discount == 0.0

def test_calculate_familiarity_discount_subprocess_error(mocker):
    discount = calculate_familiarity_discount("test@example.com", ".", {})
    # default factor 0.5 * 20 = 10.0
    assert discount == 10.0
