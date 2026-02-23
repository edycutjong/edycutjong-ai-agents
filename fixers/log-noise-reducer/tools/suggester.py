from typing import List, Tuple, Dict, Any, Optional

class Suggester:
    def __init__(self, log_counts: List[Tuple[str, int]], code_findings: List[Dict[str, Any]], total_logs: int):
        self.log_counts = log_counts
        self.code_findings = code_findings
        self.total_logs = total_logs

    def generate_suggestions(self) -> List[Dict[str, Any]]:
        suggestions = []

        for pattern, count in self.log_counts:
            # Calculate percentage
            percentage = (count / self.total_logs) * 100 if self.total_logs > 0 else 0

            # Find matching code
            match = self._find_match(pattern)

            suggestion = {
                "pattern": pattern,
                "count": count,
                "percentage": round(percentage, 2),
                "source": match if match else None,
                "action": "Investigate",
                "severity": "Low"
            }

            if match:
                log_type = match['type']
                if log_type == 'print':
                    suggestion['action'] = "Remove print statement"
                    suggestion['severity'] = "High"
                elif 'info' in log_type and percentage > 5:
                    suggestion['action'] = "Change to Debug"
                    suggestion['severity'] = "Medium"
                elif 'debug' in log_type and percentage > 10:
                    suggestion['action'] = "Remove or Sample"
                    suggestion['severity'] = "High"
                elif percentage > 20:
                     suggestion['action'] = "Implement Sampling"
                     suggestion['severity'] = "Critical"
            else:
                if percentage > 10:
                    suggestion['action'] = "Locate source manually (High Volume)"
                    suggestion['severity'] = "High"

            suggestions.append(suggestion)

        return suggestions

    def _find_match(self, pattern: str) -> Optional[Dict[str, Any]]:
        best_match = None
        best_score = 0

        pattern_lower = pattern.lower()

        for finding in self.code_findings:
            template = finding['message_template']
            if template in ["dynamic", "dynamic-expression", "f-string"]:
                continue

            # Remove <VAR> from template to get static parts
            # "Processing item <VAR>" -> "Processing item"
            static_parts = template.replace("<VAR>", "").strip()

            if not static_parts:
                continue

            # Check if static parts are in pattern
            # Using lower case for robust matching
            if static_parts.lower() in pattern_lower:
                score = len(static_parts)
                if score > best_score:
                    best_score = score
                    best_match = finding

        # Threshold for match
        if best_score > 4:
            return best_match
        return None
