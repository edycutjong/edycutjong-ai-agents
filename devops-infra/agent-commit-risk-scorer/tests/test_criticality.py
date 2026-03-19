from lib.criticality import calculate_criticality_score

def test_criticality_score_basic():
    config = {
        "scoring": {
            "max_criticality_score": 30.0
        },
        "criticality": {
            "weights": {
                "src/auth/": 10.0,
                "tests/": 0.0,
                ".py": 2.0
            }
        }
    }
    
    files = ["src/auth/login.py", "tests/test_login.py", "README.md"]
    score = calculate_criticality_score(files, config)
    # src/auth/login.py matches src/auth/ (10) and .py (2), max is 10
    # tests/test_login.py matches tests/ (0) and .py (2), max is 2
    # README.md matches nothing, defaults to 1.0
    # Avg = 13 / 3 = 4.333
    # 4.333 / 3.0 * 30.0 = 43.333 -> capped at 30.0
    assert abs(score - 30.0) < 0.1
    
def test_criticality_score_empty_config():
    files = ["src/main.py"]
    score = calculate_criticality_score(files, {})
    # default config weights -> "migrations/": 3.0, etc.
    # main.py matches nothing -> weight is 1.0. 
    # score = 1.0 / 3.0 * 30.0 = 10.0
    assert abs(score - 10.0) < 0.1
    
def test_criticality_score_invalid_regex():
    config = {
        "scoring": {
            "max_criticality_score": 30.0
        },
        "criticality": {
            "weights": {
                "main": 10.0
            }
        }
    }
    files = ["src/main.py"]
    score = calculate_criticality_score(files, config)
    # "main" matches "src/main.py" -> weight 10.0
    # 10.0 / 3.0 * 30.0 = 100.0 capped -> 30.0
    assert abs(score - 30.0) < 0.1 

def test_criticality_score_no_files():
    score = calculate_criticality_score([], {})
    assert score == 0.0
