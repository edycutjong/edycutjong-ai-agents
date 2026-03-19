from typing import List, Dict, Any
from .criticality import calculate_criticality_score
from .blast_radius import calculate_blast_radius_score
from .test_coverage import calculate_coverage_gap_score
from .history import calculate_history_risk_score, calculate_familiarity_discount

def calculate_total_risk(changed_files: List[str], author_email: str, repo_path: str, config: Dict[str, Any]) -> Dict[str, Any]:
    if not changed_files:
        return {
            "score": 0.0,
            "criticality": 0.0,
            "blast_radius": 0.0,
            "coverage_gap": 0.0,
            "history_risk": 0.0,
            "familiarity_discount": 0.0
        }
        
    crit = calculate_criticality_score(changed_files, config)
    blast = calculate_blast_radius_score(changed_files, repo_path, config)
    cov = calculate_coverage_gap_score(changed_files, config)
    hist = calculate_history_risk_score(changed_files, author_email, repo_path, config)
    
    discount = calculate_familiarity_discount(author_email, repo_path, config)
    
    total = crit + blast + cov + hist - discount
    
    # Cap between 0 and 100
    total = max(0.0, min(100.0, total))
    
    return {
        "score": total,
        "criticality": crit,
        "blast_radius": blast,
        "coverage_gap": cov,
        "history_risk": hist,
        "familiarity_discount": discount
    }
