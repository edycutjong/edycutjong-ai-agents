import pytest
import os
from unittest.mock import patch, MagicMock
from agent.core import A11yFixer
from agent.utils import calculate_luminance, generate_audit_report

def test_a11y_fixer_missing_api_key():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="OPENAI_API_KEY environment variable is required."):
            A11yFixer(api_key=None)

def test_analyze_element_json_parsing():
    fixer = A11yFixer(api_key="test-key")
    
    mock_response = MagicMock()
    mock_response.content = """Here is the answer:
{"issues": ["test issue"], "recommendations": ["test rec"], "fixed_html": "<div>fixed</div>"}
"""
    
    with patch('langchain_core.runnables.RunnableSequence.invoke', return_value=mock_response):
        result = fixer.analyze_element("<div>error</div>", "test context")
        assert result["issues"] == ["test issue"]
        assert result["fixed_html"] == "<div>fixed</div>"

def test_analyze_element_invalid_json():
    fixer = A11yFixer(api_key="test-key")
    
    mock_response = MagicMock()
    mock_response.content = """Here is the answer:
{ "issues": invalid_json_here }
"""
    
    with patch('langchain_core.runnables.RunnableSequence.invoke', return_value=mock_response):
        result = fixer.analyze_element("<div>error</div>", "test context")
        assert result["issues"] == []
        assert result["fixed_html"] == "<div>error</div>"

def test_scan_html_implicit_label():
    fixer = A11yFixer(api_key="test-key")
    html_content = """
    <form>
        <label>
            Username
            <input type="text" name="user">
        </label>
    </form>
    """
    result = fixer.scan_html(html_content)
    issues = result["issues"]
    # The input is implicitly labeled, so there shouldn't be an issue about missing label.
    assert not any(i["type"] == "Missing Form Label" for i in issues)

def test_calculate_luminance_3_char_hex():
    lum_3 = calculate_luminance("#FFF")
    lum_6 = calculate_luminance("#FFFFFF")
    assert lum_3 == lum_6
    assert 0.99 < lum_3 <= 1.0

def test_generate_audit_report_empty(tmp_path):
    report_path = tmp_path / "report_empty.html"
    res = generate_audit_report([], filename=str(report_path))
    assert res == str(report_path)
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "No issues found" in content

def test_generate_audit_report_with_issues(tmp_path):
    report_path = tmp_path / "report_issues.html"
    issues = [
        {
            "type": "Missing Alt",
            "description": "desc",
            "element": "<img>",
            "recommendation": "add alt"
        }
    ]
    res = generate_audit_report(issues, filename=str(report_path))
    assert res == str(report_path)
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Missing Alt" in content
    assert "add alt" in content
