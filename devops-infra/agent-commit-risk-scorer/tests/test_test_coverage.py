from lib.test_coverage import calculate_coverage_gap_score

def test_coverage_gap_score_basic():
    config = {
        "scoring": {
            "max_coverage_gap_score": 20.0
        }
    }
    
    files = ["src/auth.py", "tests/test_auth.py", "src/main.py"]
    score = calculate_coverage_gap_score(files, config)
    # 2 code files, 1 test file
    # ratio = 1 / 2 = 0.5
    # since ratio >= 0.5: return 0.0
    assert score == 0.0

def test_coverage_gap_score_no_tests():
    files = ["src/auth.py", "src/main.py"]
    config = {"scoring": {"max_coverage_gap_score": 20.0}}
    score = calculate_coverage_gap_score(files, config)
    # 2 code files, 0 test files -> returns max_score
    assert score == 20.0

def test_coverage_gap_score_empty_config():
    files = ["src/main.py"]
    # Default max gap penalty is 20.0
    score = calculate_coverage_gap_score(files, {})
    assert score == 20.0
    
def test_coverage_gap_score_only_tests():
    files = ["tests/test_auth.py"]
    score = calculate_coverage_gap_score(files, {})
    assert score == 0.0
    
def test_coverage_gap_score_partial_tests():
    files = ["src/auth.py", "src/main.py", "src/utils.py", "src/helper.py", "tests/test_auth.py"]
    # 4 code files, 1 test file. ratio = 0.25
    # score = 20.0 * (1.0 - (0.25 / 0.5)) = 20.0 * 0.5 = 10.0
    score = calculate_coverage_gap_score(files, {})
    assert score == 10.0
