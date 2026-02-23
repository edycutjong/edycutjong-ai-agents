"""Timesheet analyzer — track hours, analyze productivity, detect anomalies."""
from __future__ import annotations
import json, os, re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict

@dataclass
class TimeEntry:
    date: str
    project: str
    hours: float
    description: str = ""
    tags: list[str] = field(default_factory=list)
    def to_dict(self) -> dict:
        return {"date": self.date, "project": self.project, "hours": self.hours, "description": self.description, "tags": self.tags}

@dataclass
class TimesheetReport:
    entries: list[TimeEntry] = field(default_factory=list)
    total_hours: float = 0
    project_hours: dict = field(default_factory=dict)
    daily_hours: dict = field(default_factory=dict)
    avg_daily: float = 0
    anomalies: list[str] = field(default_factory=list)
    utilization: float = 0  # percentage of 8h days
    def to_dict(self) -> dict:
        return {"total_hours": self.total_hours, "project_hours": self.project_hours, "daily_hours": self.daily_hours,
                "avg_daily": round(self.avg_daily, 2), "utilization": round(self.utilization, 1), "anomalies": self.anomalies, "entries": len(self.entries)}

def parse_csv_timesheet(csv_text: str) -> list[TimeEntry]:
    """Parse CSV timesheet data."""
    entries = []
    lines = csv_text.strip().split("\n")
    if not lines: return entries
    header = [h.strip().lower() for h in lines[0].split(",")]
    for line in lines[1:]:
        if not line.strip(): continue
        values = [v.strip() for v in line.split(",")]
        row = dict(zip(header, values))
        try:
            entry = TimeEntry(
                date=row.get("date", ""),
                project=row.get("project", row.get("task", "")),
                hours=float(row.get("hours", row.get("duration", 0))),
                description=row.get("description", row.get("notes", "")),
            )
            if row.get("tags"): entry.tags = [t.strip() for t in row["tags"].split(";")]
            entries.append(entry)
        except (ValueError, KeyError):
            continue
    return entries

def analyze_timesheet(entries: list[TimeEntry], daily_target: float = 8.0) -> TimesheetReport:
    """Analyze timesheet entries."""
    report = TimesheetReport(entries=entries)
    project_hours = defaultdict(float)
    daily_hours = defaultdict(float)

    for e in entries:
        report.total_hours += e.hours
        project_hours[e.project] += e.hours
        daily_hours[e.date] += e.hours

    report.project_hours = dict(sorted(project_hours.items(), key=lambda x: -x[1]))
    report.daily_hours = dict(daily_hours)

    if daily_hours:
        report.avg_daily = report.total_hours / len(daily_hours)
        total_target = len(daily_hours) * daily_target
        report.utilization = (report.total_hours / total_target * 100) if total_target > 0 else 0

    # Anomaly detection
    for date, hours in daily_hours.items():
        if hours > 12: report.anomalies.append(f"⚠️ {date}: {hours}h logged — unusually high")
        elif hours < 2 and hours > 0: report.anomalies.append(f"ℹ️ {date}: only {hours}h — possible missing entries")

    if report.avg_daily > 10:
        report.anomalies.append(f"⚠️ Average {report.avg_daily:.1f}h/day — risk of burnout")

    return report

def get_project_breakdown(entries: list[TimeEntry]) -> dict:
    """Get percentage breakdown by project."""
    total = sum(e.hours for e in entries)
    if total == 0: return {}
    project_hours = defaultdict(float)
    for e in entries: project_hours[e.project] += e.hours
    return {p: round(h / total * 100, 1) for p, h in sorted(project_hours.items(), key=lambda x: -x[1])}

def format_report_markdown(report: TimesheetReport) -> str:
    lines = [
        "# Timesheet Report",
        f"**Total Hours:** {report.total_hours:.1f}h | **Avg Daily:** {report.avg_daily:.1f}h | **Utilization:** {report.utilization:.0f}%",
        f"**Days:** {len(report.daily_hours)} | **Projects:** {len(report.project_hours)}",
        "",
    ]
    if report.project_hours:
        lines.append("## Project Breakdown")
        total = report.total_hours or 1
        for p, h in report.project_hours.items():
            pct = h / total * 100
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            lines.append(f"- **{p}:** {h:.1f}h ({pct:.0f}%) [{bar}]")
        lines.append("")
    if report.anomalies:
        lines.append("## Anomalies")
        for a in report.anomalies: lines.append(f"- {a}")
    return "\n".join(lines)
