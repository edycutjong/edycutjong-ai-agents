import pytest
from agent.converter import ParsedRequest, parse_collection, convert_request

def test_parsed_request_to_dict():
    req = ParsedRequest(name="Test", method="POST", url="http://test.com", body="data", body_type="raw")
    d = req.to_dict()
    assert d["name"] == "Test"
    assert d["method"] == "POST"
    assert d["url"] == "http://test.com"
    assert d["body"] == "data"
    assert d["body_type"] == "raw"

def test_parse_collection_body_types():
    coll = {
        "item": [
            {
                "request": {
                    "method": "POST",
                    "url": "http://test.com/urlencoded",
                    "body": {
                        "mode": "urlencoded",
                        "urlencoded": [
                            {"key": "a", "value": "1"},
                            {"key": "b", "value": "2", "disabled": True}
                        ]
                    }
                }
            },
            {
                "request": {
                    "method": "POST",
                    "url": "http://test.com/formdata",
                    "body": {
                        "mode": "formdata",
                        "formdata": [
                            {"key": "user", "value": "test"}
                        ]
                    }
                }
            }
        ]
    }
    reqs = parse_collection(coll)
    assert len(reqs) == 2
    assert reqs[0].body_type == "urlencoded"
    assert reqs[0].body == "a=1"
    assert reqs[1].body_type == "formdata"
    assert '"user": "test"' in reqs[1].body

def test_to_python_urlencoded():
    req = ParsedRequest(method="POST", url="http://test", body="a=1", body_type="urlencoded")
    code = convert_request(req, "python")
    assert 'data = "a=1"' in code

def test_to_javascript_extra():
    # Only auth token, no headers
    req = ParsedRequest(method="GET", url="http://test", auth_token="abc", body="bodydata")
    code = convert_request(req, "javascript")
    assert "Bearer abc" in code
    assert "bodydata" in code

def test_to_go_extra():
    req = ParsedRequest(method="POST", url="http://test", body="bodydata", auth_token="abc", headers={"X-Test": "yes"})
    code = convert_request(req, "go")
    assert '"strings"' in code
    assert "strings.NewReader" in code
    assert "X-Test" in code
    assert "Bearer abc" in code
