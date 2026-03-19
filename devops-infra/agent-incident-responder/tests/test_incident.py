"""Tests for the incident responder agent."""
import pytest

from agent.detector import PatternDetector, Alert
from agent.diagnoser import Diagnoser, DiagnosisResult
from agent.reporter import IncidentReporter


class TestPatternDetector:
    """Tests for PatternDetector."""

    def test_detect_oom(self):
        detector = PatternDetector(min_severity="error")  # pragma: no cover
        alerts = detector.check_line("2024-01-15 ERROR java.lang.OutOfMemoryError: Java heap space")  # pragma: no cover
        assert len(alerts) >= 1  # pragma: no cover
        assert any(a.severity == "critical" for a in alerts)  # pragma: no cover

    def test_detect_connection_refused(self):
        detector = PatternDetector(min_severity="error")  # pragma: no cover
        alerts = detector.check_line("ERROR: Connection refused to database at 10.0.0.1:5432")  # pragma: no cover
        assert len(alerts) >= 1  # pragma: no cover

    def test_detect_timeout(self):
        detector = PatternDetector(min_severity="error")  # pragma: no cover
        alerts = detector.check_line("2024-01-15 ERROR Request timed out after 30000ms")  # pragma: no cover
        assert len(alerts) >= 1  # pragma: no cover

    def test_no_alert_below_severity(self):
        detector = PatternDetector(min_severity="critical")  # pragma: no cover
        alerts = detector.check_line("2024-01-15 WARN Something happened")  # pragma: no cover
        assert len(alerts) == 0  # pragma: no cover

    def test_clean_line_no_alerts(self):
        detector = PatternDetector(min_severity="error")  # pragma: no cover
        alerts = detector.check_line("2024-01-15 INFO Server started on port 8080")  # pragma: no cover
        assert len(alerts) == 0  # pragma: no cover

    def test_check_multiple_lines(self):
        detector = PatternDetector(min_severity="warn")  # pragma: no cover
        lines = [  # pragma: no cover
            "INFO: Server started",
            "WARN: Rate limit approaching",
            "ERROR: Connection timed out",
        ]
        alerts = detector.check_lines(lines)  # pragma: no cover
        assert len(alerts) >= 2  # pragma: no cover

    def test_alert_has_suggestion(self):
        detector = PatternDetector(min_severity="error")  # pragma: no cover
        alerts = detector.check_line("CRITICAL: Disk full, no space left on device")  # pragma: no cover
        assert len(alerts) >= 1  # pragma: no cover
        assert alerts[0].suggestion is not None  # pragma: no cover


class TestDiagnoser:
    """Tests for Diagnoser."""

    def test_diagnose_errors(self):
        diagnoser = Diagnoser()  # pragma: no cover
        lines = [  # pragma: no cover
            "2024-01-15 ERROR ConnectionError: ECONNREFUSED",
            "2024-01-15 ERROR ConnectionError: ECONNREFUSED",
            "2024-01-15 INFO Recovery successful",
        ]
        result = diagnoser.diagnose(lines)  # pragma: no cover
        assert result.issue_count >= 2  # pragma: no cover
        assert result.max_severity in ["error", "critical"]  # pragma: no cover

    def test_diagnose_clean_logs(self):
        diagnoser = Diagnoser()  # pragma: no cover
        lines = ["2024-01-15 INFO All systems operational"]  # pragma: no cover
        result = diagnoser.diagnose(lines)  # pragma: no cover
        assert result.issue_count == 0  # pragma: no cover

    def test_diagnose_oom_pattern(self):
        diagnoser = Diagnoser()  # pragma: no cover
        lines = ["CRITICAL OutOfMemoryError - process killed"]  # pragma: no cover
        result = diagnoser.diagnose(lines)  # pragma: no cover
        assert "Memory exhaustion" in result.patterns  # pragma: no cover

    def test_result_to_dict(self):
        result = DiagnosisResult(issue_count=5, max_severity="error")  # pragma: no cover
        d = result.to_dict()  # pragma: no cover
        assert d["issue_count"] == 5  # pragma: no cover

    def test_result_to_markdown(self):
        result = DiagnosisResult(issue_count=3, max_severity="error", patterns=["Timeout"])  # pragma: no cover
        md = result.to_markdown()  # pragma: no cover
        assert "Incident Diagnosis Report" in md  # pragma: no cover


class TestIncidentReporter:
    """Tests for IncidentReporter."""

    def test_standard_report(self):
        reporter = IncidentReporter(template="standard")  # pragma: no cover
        data = {  # pragma: no cover
            "id": "INC-001",
            "severity": "high",
            "summary": "Database outage",
            "root_cause": "Disk full",
            "duration": "45 minutes",
            "users_affected": "5000",
        }
        report = reporter.generate(data)  # pragma: no cover
        assert "INC-001" in report  # pragma: no cover
        assert "Database outage" in report  # pragma: no cover

    def test_brief_report(self):
        reporter = IncidentReporter(template="brief")  # pragma: no cover
        report = reporter.generate({"id": "INC-002", "summary": "API timeout"})  # pragma: no cover
        assert "INC-002" in report  # pragma: no cover
        assert "Brief" in report  # pragma: no cover

    def test_detailed_report(self):
        reporter = IncidentReporter(template="detailed")  # pragma: no cover
        report = reporter.generate({  # pragma: no cover
            "id": "INC-003",
            "summary": "Memory leak",
            "detection_method": "Prometheus alert",
        })
        assert "Technical Details" in report  # pragma: no cover
        assert "Monitoring" in report  # pragma: no cover
