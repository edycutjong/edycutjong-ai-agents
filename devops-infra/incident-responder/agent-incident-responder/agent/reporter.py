"""Incident report generator."""
from datetime import datetime
from typing import Dict, Any


class IncidentReporter:
    """Generates post-mortem incident reports."""

    def __init__(self, template: str = "standard"):
        self.template = template

    def generate(self, data: Dict[str, Any]) -> str:
        """Generate a post-mortem report from incident data."""
        if self.template == "brief":
            return self._brief(data)
        elif self.template == "detailed":
            return self._detailed(data)
        return self._standard(data)

    def _standard(self, d: Dict) -> str:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        return f"""# Incident Post-Mortem Report

**Generated:** {now}
**Incident ID:** {d.get('id', 'N/A')}
**Severity:** {d.get('severity', 'Unknown')}
**Status:** {d.get('status', 'Resolved')}

## Summary
{d.get('summary', 'No summary provided.')}

## Timeline
| Time | Event |
|------|-------|
{self._format_timeline(d.get('timeline', []))}

## Impact
- **Duration:** {d.get('duration', 'Unknown')}
- **Users affected:** {d.get('users_affected', 'Unknown')}
- **Services affected:** {', '.join(d.get('services', ['Unknown']))}

## Root Cause
{d.get('root_cause', 'Under investigation.')}

## Resolution
{d.get('resolution', 'Pending documentation.')}

## Action Items
{self._format_actions(d.get('action_items', []))}

## Lessons Learned
{self._format_list(d.get('lessons', ['To be discussed in retrospective.']))}
"""

    def _brief(self, d: Dict) -> str:
        return f"""# Incident Brief: {d.get('id', 'N/A')}

**What happened:** {d.get('summary', 'N/A')}
**Impact:** {d.get('duration', '?')} downtime, {d.get('users_affected', '?')} users affected
**Root cause:** {d.get('root_cause', 'TBD')}
**Fix:** {d.get('resolution', 'TBD')}
**Follow-up:** {len(d.get('action_items', []))} action items
"""

    def _detailed(self, d: Dict) -> str:
        base = self._standard(d)
        extra = f"""
## Technical Details
{d.get('technical_details', 'No additional technical details.')}

## Monitoring & Detection
- **How detected:** {d.get('detection_method', 'Manual')}
- **Time to detect:** {d.get('time_to_detect', 'Unknown')}
- **Time to resolve:** {d.get('time_to_resolve', 'Unknown')}

## Communication
{d.get('communication_log', 'No communication log available.')}

## Prevention
{self._format_list(d.get('prevention_measures', ['Review and update monitoring alerts.']))}
"""
        return base + extra

    @staticmethod
    def _format_timeline(timeline):
        if not timeline:
            return "| - | No timeline data |"
        return "\n".join(f"| {e.get('time', '?')} | {e.get('event', '?')} |" for e in timeline)

    @staticmethod
    def _format_actions(actions):
        if not actions:
            return "- [ ] Document action items after retrospective"
        return "\n".join(f"- [ ] {a}" for a in actions)

    @staticmethod
    def _format_list(items):
        return "\n".join(f"- {item}" for item in items)
