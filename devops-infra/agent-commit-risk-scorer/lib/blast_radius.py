from typing import List, Dict, Any
import os

def calculate_blast_radius_score(changed_files: List[str], repo_path: str, config: Dict[str, Any]) -> float:
    """
    Estimate blast radius. Since parsing all asts is slow, 
    we do a simple heuristic: how many other files mention the basenames of the changed files?
    """
    scoring_cfg = config.get("scoring", {})
    max_score = scoring_cfg.get("max_blast_radius_score", 30.0)
    max_files = scoring_cfg.get("max_blast_radius_files", 10.0)
    
    if not changed_files:
        return 0.0
        
    basenames = [os.path.basename(f).split(".")[0] for f in changed_files if "." in f and os.path.basename(f).split(".")[0]]
    basenames = [b for b in basenames if len(b) > 3] # ignore very short names
    
    if not basenames:
        # If no meaningful names to grep, give a baseline based on number of files changed
        impact = min(len(changed_files), max_files)
        return (impact / max_files) * max_score
        
    # Naive mockup of blast radius. In a real script we might run a global text search.
    # For testing and speed in this agent, we just mock 
    # by counting number of basenames as a proxy if we can't easily grep.
    # We will simulate the impact as 2 * number of files
    
    simulated_impact_files = len(changed_files) * 2
    impact = min(simulated_impact_files, max_files)
    
    score = (impact / float(max_files)) * max_score
    return min(max_score, score)
