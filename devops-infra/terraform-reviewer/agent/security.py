from typing import List, Dict, Any

class SecurityScanner:
    def scan(self, hcl_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        if not hcl_data or 'resource' not in hcl_data:
            return findings

        resources = hcl_data.get('resource', [])
        for resource_block in resources:
            for resource_type, resource_instances in resource_block.items():
                for name, config in resource_instances.items():
                    if resource_type == 'aws_security_group':
                        findings.extend(self._check_security_group(name, config))
                    elif resource_type == 'aws_s3_bucket':
                        findings.extend(self._check_s3_bucket(name, config))
                    elif resource_type == 'aws_ebs_volume':
                        findings.extend(self._check_ebs_volume(name, config))
                    elif resource_type == 'aws_iam_policy':
                        findings.extend(self._check_iam_policy(name, config))
        return findings

    def _check_security_group(self, name: str, config: Dict) -> List[Dict]:
        issues = []
        ingress_rules = config.get('ingress', [])
        if isinstance(ingress_rules, list):
            for rule in ingress_rules:
                cidr_blocks = rule.get('cidr_blocks', [])
                if '0.0.0.0/0' in cidr_blocks:
                     # Check if port is sensitive (SSH 22, RDP 3389, DBs)
                    from_port = int(rule.get('from_port', 0))
                    to_port = int(rule.get('to_port', 0))
                    if from_port <= 22 <= to_port or from_port == 0:
                        issues.append({
                            "resource": f"aws_security_group.{name}",
                            "severity": "CRITICAL",
                            "message": f"Security Group allows SSH (22) from 0.0.0.0/0"
                        })
                    elif from_port <= 3389 <= to_port:
                        issues.append({
                            "resource": f"aws_security_group.{name}",
                            "severity": "CRITICAL",
                            "message": f"Security Group allows RDP (3389) from 0.0.0.0/0"
                        })
                    else:
                        issues.append({
                            "resource": f"aws_security_group.{name}",
                            "severity": "HIGH",
                            "message": f"Security Group allows ingress from 0.0.0.0/0 on ports {from_port}-{to_port}"
                        })
        return issues

    def _check_s3_bucket(self, name: str, config: Dict) -> List[Dict]:
        issues = []
        # Check for encryption (simplified, newer TF uses aws_s3_bucket_server_side_encryption_configuration)
        # But checks against properties in the resource block for older patterns or inline.
        # This is a basic check.
        if 'server_side_encryption_configuration' not in config:
             issues.append({
                "resource": f"aws_s3_bucket.{name}",
                "severity": "MEDIUM",
                "message": "S3 Bucket may lack server-side encryption configuration."
            })

        acl = config.get('acl', 'private')
        if acl == 'public-read' or acl == 'public-read-write':
            issues.append({
                "resource": f"aws_s3_bucket.{name}",
                "severity": "CRITICAL",
                "message": f"S3 Bucket ACL is set to {acl} (Public Access)."
            })

        return issues

    def _check_ebs_volume(self, name: str, config: Dict) -> List[Dict]:
        issues = []
        encrypted = config.get('encrypted', False)
        if not encrypted:
            issues.append({
                "resource": f"aws_ebs_volume.{name}",
                "severity": "HIGH",
                "message": "EBS Volume is not encrypted."
            })
        return issues

    def _check_iam_policy(self, name: str, config: Dict) -> List[Dict]:
        issues = []
        # Parsing policy JSON is complex as it's often a string (heredoc).
        # We'll just flag if we see "Action": "*" in a simple string search if it's not a complex object.
        policy = config.get('policy')
        if isinstance(policy, str):
            if '"Action": "*"' in policy or "'Action': '*'" in policy:
                issues.append({
                    "resource": f"aws_iam_policy.{name}",
                    "severity": "CRITICAL",
                    "message": "IAM Policy allows full administrative privileges ('*')."
                })
        return issues
