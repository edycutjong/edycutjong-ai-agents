import re
from typing import Dict, Any, List

class RulesChecker:
    def __init__(self):
        self.snake_case_pattern = re.compile(r'^[a-z0-9_]+$')
        self.secret_pattern = re.compile(r'(?i)(password|secret|key|token|auth)')
        self.aws_key_pattern = re.compile(r'AKIA[0-9A-Z]{16}')

    def check_naming(self, hcl_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        if not hcl_data or 'resource' not in hcl_data:
            return findings

        resources = hcl_data.get('resource', [])
        for resource_block in resources:
            for resource_type, resource_instances in resource_block.items():
                for name, config in resource_instances.items():
                    if not self.snake_case_pattern.match(name):
                        findings.append({
                            "resource": f"{resource_type}.{name}",
                            "severity": "LOW",
                            "message": f"Resource name '{name}' does not follow snake_case convention."
                        })
        return findings

    def check_hardcoded_secrets(self, hcl_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []

        # Check provider blocks
        providers = hcl_data.get('provider', [])
        for provider_block in providers:
            for provider_name, config in provider_block.items():
                # Config might be a list or dict depending on hcl2 parser
                if isinstance(config, list):
                    config = config[0] # Take first block if list

                if isinstance(config, dict):
                    for key, value in config.items():
                        if self.aws_key_pattern.search(str(value)):
                             findings.append({
                                "resource": f"provider.{provider_name}",
                                "severity": "CRITICAL",
                                "message": f"Potential AWS Access Key found in provider configuration."
                            })
                        if key in ['access_key', 'secret_key'] and not str(value).startswith(('var.', '${var.')):
                             findings.append({
                                "resource": f"provider.{provider_name}",
                                "severity": "HIGH",
                                "message": f"Hardcoded '{key}' in provider configuration. Use variables instead."
                            })

        # Check resource blocks
        resources = hcl_data.get('resource', [])
        for resource_block in resources:
            for resource_type, resource_instances in resource_block.items():
                for name, config in resource_instances.items():
                    for key, value in config.items():
                        # Check keys
                        if self.secret_pattern.search(key):
                             # If value is hardcoded string (not var reference)
                             if isinstance(value, str) and not value.startswith(('var.', '${var.')):
                                  findings.append({
                                    "resource": f"{resource_type}.{name}",
                                    "severity": "HIGH",
                                    "message": f"Potential hardcoded secret in attribute '{key}'."
                                })
        return findings
