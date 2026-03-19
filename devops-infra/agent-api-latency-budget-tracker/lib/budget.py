import math
from typing import List, Dict, Any

class BudgetManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def evaluate(self, latencies: List[float], slo_targets: Dict[str, float], total_budget_percent: float) -> Dict[str, Any]:
        """
        Evaluate latencies against SLO targets. Returns a report of budget consumption.
        latencies: list of response times in ms
        slo_targets: e.g. {"p50": 100, "p95": 500, "p99": 1000}
        total_budget_percent: e.g. 1.0 (meaning 1%)
        """
        if not latencies:
            return {"total_requests": 0, "violations": 0, "allowable_violations": 0.0, "budget_consumed_percent": 0.0, "is_exhausted": False}
        
        latencies.sort()
        total_reqs = len(latencies)
        violations = 0
        
        target_ms = None
        if "p99" in slo_targets:
            target_ms = slo_targets["p99"]
        elif "p95" in slo_targets:
            target_ms = slo_targets["p95"]
        elif "p50" in slo_targets:
            target_ms = slo_targets["p50"]
            
        if target_ms is None:
            return {"total_requests": total_reqs, "violations": 0, "allowable_violations": 0.0, "budget_consumed_percent": 0.0, "is_exhausted": False}

        violations = sum(1 for l in latencies if l > target_ms)
        
        allowable_violations = total_reqs * (total_budget_percent / 100.0)
        
        consumed_percent = (violations / allowable_violations * 100.0) if allowable_violations > 0 else 0.0
        
        is_exhausted = consumed_percent >= 100.0

        return {
            "total_requests": total_reqs,
            "violations": violations,
            "allowable_violations": allowable_violations,
            "budget_consumed_percent": consumed_percent,
            "is_exhausted": is_exhausted
        }
