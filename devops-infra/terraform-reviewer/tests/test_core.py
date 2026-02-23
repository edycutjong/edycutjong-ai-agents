import sys
import os
import pytest

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.parser import TerraformParser
from agent.security import SecurityScanner
from agent.cost import CostEstimator
from agent.rules import RulesChecker
from agent.drift import DriftDetector

TF_CONTENT = """
resource "aws_security_group" "allow_all" {
  name        = "allow_all"
  description = "Allow all inbound traffic"
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_s3_bucket" "b" {
  bucket = "my-bucket"
  acl    = "public-read"
}

resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"
}
"""

TF_STATE = {
  "version": 4,
  "resources": [
    {
      "mode": "managed",
      "type": "aws_s3_bucket",
      "name": "b",
      "provider": "provider.aws",
      "instances": []
    }
  ]
}

def test_security_scan():
    parser = TerraformParser()
    # Need to mock the parsed output structure of hcl2 since we can't easily parse string with hcl2 without ply and temp file potentially if string parsing fails or structure differs.
    # Actually hcl2.loads works on string.
    # But wait, does hcl2 support `loads`? python-hcl2 supports `loads`.

    # We will try to parse.
    try:
        hcl_data = parser.parse_hcl(TF_CONTENT)
    except Exception as e:
        pytest.fail(f"Parsing failed: {e}")

    scanner = SecurityScanner()
    findings = scanner.scan(hcl_data)

    assert len(findings) > 0
    sg_finding = next((f for f in findings if "aws_security_group" in f["resource"]), None)
    assert sg_finding is not None
    assert sg_finding["severity"] == "CRITICAL"

def test_cost_estimation():
    parser = TerraformParser()
    hcl_data = parser.parse_hcl(TF_CONTENT)
    estimator = CostEstimator()
    cost = estimator.estimate(hcl_data)
    assert cost["total_monthly_cost"] > 0
    assert "aws_instance.web" in cost["details"]

def test_drift_detection():
    parser = TerraformParser()
    hcl_data = parser.parse_hcl(TF_CONTENT)
    drift = DriftDetector()
    drift_result = drift.detect(hcl_data, TF_STATE)
    assert "aws_security_group.allow_all" in drift_result["in_code_not_in_state"]
    assert "aws_s3_bucket.b" not in drift_result["in_code_not_in_state"]
