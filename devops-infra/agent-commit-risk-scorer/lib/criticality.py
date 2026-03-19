from typing import List, Dict, Any

def calculate_criticality_score(changed_files: List[str], config: Dict[str, Any]) -> float:
    """
    Calculate criticality score based on paths.
    Returns a score from 0 to max_criticality_score.
    """
    scoring_cfg = config.get("scoring", {})
    max_score = scoring_cfg.get("max_criticality_score", 30.0)
    
    crit_cfg = config.get("criticality", {}).get("weights", {})
    
    # Defaults
    if not crit_cfg:
        crit_cfg = {
            "migrations/": 3.0,
            "security/": 2.5,
            "config/": 2.0
        }
        
    total_weight = 0.0
    for f in changed_files:
        file_weight = 1.0
        for path_key, weight in crit_cfg.items():
            if path_key in f:
                file_weight = max(file_weight, weight)
        total_weight += file_weight
        
    if not changed_files:
        return 0.0
        
    # Average weight * 10 
    avg_weight = total_weight / len(changed_files)
    
    # Scale: an avg weight of 1.0 is a "normal" risk, maybe 10 points. 
    # An avg weight of 3.0 reaches max score.
    score = (avg_weight / 3.0) * max_score
    
    return min(max_score, score)
