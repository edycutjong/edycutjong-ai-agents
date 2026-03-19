from lib.blast_radius import calculate_blast_radius_score

def test_blast_radius_score_basic(mocker):
    config = {
        "scoring": {
            "max_blast_radius_score": 30.0,
            "max_blast_radius_files": 10.0
        }
    }
    
    files = ["src/main.py", "README.md", "src/auth.py", "src/utils.py"]
    
    score = calculate_blast_radius_score(files, ".", config)
    # 4 files -> 8 impact -> min(8, 10.0) = 8
    # 8 / 10.0 * 30.0 = 24.0
    assert abs(score - 24.0) < 0.1

def test_blast_radius_score_empty_config(mocker):
    files = ["src/main.py"]
    score = calculate_blast_radius_score(files, ".", {})
    # default max_files = 10.0, max_score = 30.0
    # 1 file -> 2 impact -> 2 / 10.0 * 30.0 = 6.0
    assert abs(score - 6.0) < 0.1
    
def test_blast_radius_score_high_volume(mocker):
    files = [f"file_{i}.py" for i in range(15)]
    config = {
        "scoring": {
            "max_blast_radius_score": 30.0,
            "max_blast_radius_files": 10.0
        }
    }
    score = calculate_blast_radius_score(files, ".", config)
    # 15 files -> 30 impact -> min(30, 10) = 10
    # 10 / 10.0 * 30.0 = 30.0
    assert abs(score - 30.0) < 0.1

def test_blast_radius_score_no_files():
    assert calculate_blast_radius_score([], ".", {}) == 0.0

def test_blast_radius_score_short_names(mocker):
    # Tests the case where no basenames are > 3 chars
    files = ["a.py", "b.py"]
    mocker.patch("os.path.dirname", return_value=".")
    
    config = {
        "scoring": {
            "max_blast_radius_score": 30.0,
            "max_blast_radius_files": 10.0
        }
    }
    score = calculate_blast_radius_score(files, ".", config)
    # 2 files / 10.0 * 30.0 = 6.0
    assert abs(score - 6.0) < 0.1
