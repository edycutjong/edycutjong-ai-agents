from typing import List, Dict, Any

def calculate_history_risk_score(changed_files: List[str], author_email: str, repo_path: str, config: Dict[str, Any]) -> float:
    """
    Bug correlation and familiarity. 
    """
    scoring_cfg = config.get("scoring", {})
    max_score = scoring_cfg.get("max_history_risk_score", 20.0)
    
    if not changed_files:
        return 0.0
        
    bug_prone_penalty = 0.5 # Default middle risk
    
    return max_score * bug_prone_penalty

def calculate_familiarity_discount(author_email: str, repo_path: str, config: Dict[str, Any]) -> float:
    scoring_cfg = config.get("scoring", {})
    max_discount = scoring_cfg.get("familiarity_discount_max", 20.0)
    
    if not author_email:
        return 0.0
        
    # Assume known author gets 50% of the max discount for simple implementation
    return max_discount * 0.5
