"""SLA monitor — track service level agreements and compliance."""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class SLADefinition:
    name: str
    metric: str  # uptime, response_time, resolution_time, error_rate
    target: float  # target value
    unit: str = "%"  # %, ms, hours
    warning_threshold: float = 0  # threshold before breach
    def to_dict(self) -> dict:
        return self.__dict__.copy()

@dataclass
class SLAMeasurement:
    sla_name: str
    value: float
    timestamp: str = ""
    def __post_init__(self):
        if not self.timestamp: self.timestamp = datetime.now().isoformat()
    def to_dict(self) -> dict:
        return self.__dict__.copy()

@dataclass
class SLAStatus:
    sla: SLADefinition
    current_value: float = 0
    is_compliant: bool = True
    is_warning: bool = False
    margin: float = 0  # how far above/below target
    measurements: list[SLAMeasurement] = field(default_factory=list)
    def to_dict(self) -> dict:
        return {"name": self.sla.name, "metric": self.sla.metric, "target": self.sla.target, "current": self.current_value,
                "unit": self.sla.unit, "compliant": self.is_compliant, "warning": self.is_warning, "margin": round(self.margin, 2)}

def check_compliance(sla: SLADefinition, value: float) -> SLAStatus:
    """Check if a value meets an SLA target."""
    status = SLAStatus(sla=sla, current_value=value)
    if sla.metric in ("uptime",):
        status.is_compliant = value >= sla.target
        status.margin = value - sla.target
        status.is_warning = not status.is_compliant or (sla.warning_threshold > 0 and value <= sla.target + sla.warning_threshold)
    elif sla.metric in ("response_time", "resolution_time"):
        status.is_compliant = value <= sla.target
        status.margin = sla.target - value
        status.is_warning = not status.is_compliant or (sla.warning_threshold > 0 and value >= sla.target - sla.warning_threshold)
    elif sla.metric == "error_rate":
        status.is_compliant = value <= sla.target
        status.margin = sla.target - value
        status.is_warning = not status.is_compliant or (sla.warning_threshold > 0 and value >= sla.target - sla.warning_threshold)
    return status

def calculate_uptime(total_minutes: float, downtime_minutes: float) -> float:
    """Calculate uptime percentage."""
    if total_minutes <= 0: return 0
    return round((total_minutes - downtime_minutes) / total_minutes * 100, 4)

def calculate_compliance_rate(statuses: list[SLAStatus]) -> float:
    """Calculate overall compliance rate."""
    if not statuses: return 0
    compliant = sum(1 for s in statuses if s.is_compliant)
    return round(compliant / len(statuses) * 100, 1)

def get_breach_report(statuses: list[SLAStatus]) -> list[dict]:
    """Get list of SLA breaches."""
    return [s.to_dict() for s in statuses if not s.is_compliant]

def format_sla_dashboard(statuses: list[SLAStatus]) -> str:
    compliance = calculate_compliance_rate(statuses)
    lines = ["# SLA Dashboard", f"**Overall Compliance:** {compliance}% | **SLAs:** {len(statuses)}", ""]
    for s in statuses:
        if s.is_compliant:
            emoji = "✅" if not s.is_warning else "🟡"
        else:
            emoji = "🔴"
        lines.append(f"## {emoji} {s.sla.name}")
        lines.append(f"**Target:** {s.sla.target}{s.sla.unit} | **Current:** {s.current_value}{s.sla.unit} | **Margin:** {s.margin:+.2f}{s.sla.unit}")
        lines.append("")
    breaches = [s for s in statuses if not s.is_compliant]
    if breaches:
        lines.append("## 🚨 Breaches")
        for b in breaches:
            lines.append(f"- **{b.sla.name}**: {b.current_value}{b.sla.unit} vs target {b.sla.target}{b.sla.unit}")
    return "\n".join(lines)
