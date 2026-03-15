"""Tests for the incident responder agent."""
import pytest

from agent.detector import PatternDetector, Alert
from agent.diagnoser import Diagnoser, DiagnosisResult
from agent.reporter import IncidentReporter


class TestPatternDetector:
    """Tests for PatternDetector."""

    def test_detect_oom(self):
        detector = PatternDetector(min_severity="error")
        alerts = detector.check_line("2024-01-15 ERROR java.lang.OutOfMemoryError: Java heap space")
        assert len(alerts) >= 1
        assert any(a.severity == "critical" for a in alerts)

    def test_detect_connection_refused(self):
        detector = PatternDetector(min_severity="error")
        alerts = detector.check_line("ERROR: Connection refused to database at 10.0.0.1:5432")
        assert len(alerts) >= 1

    def test_detect_timeout(self):
        detector = PatternDetector(min_severity="error")
        alerts = detector.check_line("2024-01-15 ERROR Request timed out after 30000ms")
        assert len(alerts) >= 1

    def test_no_alert_below_severity(self):
        detector = PatternDetector(min_severity="critical")
        alerts = detector.check_line("2024-01-15 WARN Something happened")
        assert len(alerts) == 0

    def test_clean_line_no_alerts(self):
        detector = PatternDetector(min_severity="error")
        alerts = detector.check_line("2024-01-15 INFO Server started on port 8080")
        assert len(alerts) == 0

    def test_check_multiple_lines(self):
        detector = PatternDetector(min_severity="warn")
        lines = [
            "INFO: Server started",
            "WARN: Rate limit approaching",
            "ERROR: Connection timed out",
        ]
        alerts = detector.check_lines(lines)
        assert len(alerts) >= 2

    def test_alert_has_suggestion(self):
        detector = PatternDetector(min_severity="error")
        alerts = detector.check_line("CRITICAL: Disk full, no space left on device")
        assert len(alerts) >= 1
        assert alerts[0].suggestion is not None


class TestDiagnoser:
    """Tests for Diagnoser."""

    def test_diagnose_errors(self):
        diagnoser = Diagnoser()
        lines = [
            "2024-01-15 ERROR ConnectionError: ECONNREFUSED",
            "2024-01-15 ERROR ConnectionError: ECONNREFUSED",
            "2024-01-15 INFO Recovery successful",
        ]
        result = diagnoser.diagnose(lines)
        assert result.issue_count >= 2
        assert result.max_severity in ["error", "critical"]

    def test_diagnose_clean_logs(self):
        diagnoser = Diagnoser()
        lines = ["2024-01-15 INFO All systems operational"]
        result = diagnoser.diagnose(lines)
        assert result.issue_count == 0

    def test_diagnose_oom_pattern(self):
        diagnoser = Diagnoser()
        lines = ["CRITICAL OutOfMemoryError - process killed"]
        result = diagnoser.diagnose(lines)
        assert "Memory exhaustion" in result.patterns

    def test_result_to_dict(self):
        result = DiagnosisResult(issue_count=5, max_severity="error")
        d = result.to_dict()
        assert d["issue_count"] == 5

    def test_result_to_markdown(self):
        result = DiagnosisResult(issue_count=3, max_severity="error", patterns=["Timeout"])
        md = result.to_markdown()
        assert "Incident Diagnosis Report" in md


class TestIncidentReporter:
    """Tests for IncidentReporter."""

    def test_standard_report(self):
        reporter = IncidentReporter(template="standard")
        data = {
            "id": "INC-001",
            "severity": "high",
            "summary": "Database outage",
            "root_cause": "Disk full",
            "duration": "45 minutes",
            "users_affected": "5000",
        }
        report = reporter.generate(data)
        assert "INC-001" in report
        assert "Database outage" in report

    def test_brief_report(self):
        reporter = IncidentReporter(template="brief")
        report = reporter.generate({"id": "INC-002", "summary": "API timeout"})
        assert "INC-002" in report
        assert "Brief" in report

    def test_detailed_report(self):
        reporter = IncidentReporter(template="detailed")
        report = reporter.generate({
            "id": "INC-003",
            "summary": "Memory leak",
            "detection_method": "Prometheus alert",
        })
        assert "Technical Details" in report
        assert "Monitoring" in report
