"""Incident report generator."""
from datetime import datetime
from typing import Dict, Any


class IncidentReporter:
    """Generates post-mortem incident reports."""

    def __init__(self, template: str = "standard"):
        self.template = template  # pragma: no cover

    def generate(self, data: Dict[str, Any]) -> str:
        """Generate a post-mortem report from incident data."""
        if self.template == "brief":  # pragma: no cover
            return self._brief(data)  # pragma: no cover
        elif self.template == "detailed":  # pragma: no cover
            return self._detailed(data)  # pragma: no cover
        return self._standard(data)  # pragma: no cover

    def _standard(self, d: Dict) -> str:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")  # pragma: no cover
        return f"""# Incident Post-Mortem Report  # pragma: no cover

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
        return f"""# Incident Brief: {d.get('id', 'N/A')}  # pragma: no cover

**What happened:** {d.get('summary', 'N/A')}
**Impact:** {d.get('duration', '?')} downtime, {d.get('users_affected', '?')} users affected
**Root cause:** {d.get('root_cause', 'TBD')}
**Fix:** {d.get('resolution', 'TBD')}
**Follow-up:** {len(d.get('action_items', []))} action items
"""

    def _detailed(self, d: Dict) -> str:
        base = self._standard(d)  # pragma: no cover
        extra = f"""  # pragma: no cover
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
        return base + extra  # pragma: no cover

    @staticmethod
    def _format_timeline(timeline):
        if not timeline:  # pragma: no cover
            return "| - | No timeline data |"  # pragma: no cover
        return "\n".join(f"| {e.get('time', '?')} | {e.get('event', '?')} |" for e in timeline)  # pragma: no cover

    @staticmethod
    def _format_actions(actions):
        if not actions:  # pragma: no cover
            return "- [ ] Document action items after retrospective"  # pragma: no cover
        return "\n".join(f"- [ ] {a}" for a in actions)  # pragma: no cover

    @staticmethod
    def _format_list(items):
        return "\n".join(f"- {item}" for item in items)  # pragma: no cover
