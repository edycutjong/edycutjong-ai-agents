from typing import Dict, Any, List, Set

class DriftDetector:
    def detect(self, hcl_data: Dict[str, Any], state_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compares HCL (code) against Terraform State.
        Returns resources found in Code but not State (to be created),
        and resources in State but not Code (to be destroyed/or deleted from code).
        """
        if not state_data:
            return {"status": "No State Provided", "diff": {}}

        # Parse HCL resources
        code_resources = set()
        resources_hcl = hcl_data.get('resource', [])
        for resource_block in resources_hcl:
            for resource_type, resource_instances in resource_block.items():
                for name in resource_instances.keys():
                    code_resources.add(f"{resource_type}.{name}")

        # Parse State resources
        state_resources = set()
        resources_state = state_data.get('resources', [])
        for resource in resources_state:
            # State format varies by version, but usually has 'type', 'name', 'instances'
            # We look for 'mode': 'managed'
            if resource.get('mode') == 'managed':
                r_type = resource.get('type')
                r_name = resource.get('name')
                state_resources.add(f"{r_type}.{r_name}")

        # Calculate Diff
        in_code_only = list(code_resources - state_resources)
        in_state_only = list(state_resources - code_resources)

        return {
            "status": "Drift Detected" if in_code_only or in_state_only else "Synced",
            "in_code_not_in_state": in_code_only,
            "in_state_not_in_code": in_state_only
        }
