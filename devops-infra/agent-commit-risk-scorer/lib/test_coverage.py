from typing import List, Dict, Any

def calculate_coverage_gap_score(changed_files: List[str], config: Dict[str, Any]) -> float:
    """
    Check if code changes have corresponding test changes.
    """
    scoring_cfg = config.get("scoring", {})
    max_score = scoring_cfg.get("max_coverage_gap_score", 20.0)
    
    code_files = [f for f in changed_files if not f.startswith("tests/") and not "test_" in f and not "spec." in f]
    test_files = [f for f in changed_files if f.startswith("tests/") or "test_" in f or "spec." in f]
    
    if not code_files:
        return 0.0  # No code touched, no risk
        
    if test_files:
        # If tests are updated, we assume 0 risk for gap. Or partial risk based on ratio.
        ratio = len(test_files) / len(code_files)
        if ratio >= 0.5:
            return 0.0
        else:
            return max_score * (1.0 - (ratio / 0.5))
            
    # Risk is max if code touched but no tests
    return max_score
