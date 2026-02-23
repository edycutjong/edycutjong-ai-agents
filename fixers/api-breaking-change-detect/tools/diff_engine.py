from typing import Dict, List, Any, Optional
from enum import Enum
import logging

class ChangeType(Enum):
    BREAKING = "BREAKING"
    NON_BREAKING = "NON_BREAKING"
    INFO = "INFO"

class APIChange:
    def __init__(self, change_type: ChangeType, description: str, location: str):
        self.change_type = change_type
        self.description = description
        self.location = location

    def __repr__(self):
        return f"[{self.change_type.value}] {self.description} at {self.location}"

    def to_dict(self):
        return {
            "type": self.change_type.value,
            "description": self.description,
            "location": self.location
        }

def detect_breaking_changes(old_spec: Dict[str, Any], new_spec: Dict[str, Any]) -> List[APIChange]:
    changes = []

    # Check for removed paths
    old_paths = set(old_spec.get('paths', {}).keys())
    new_paths = set(new_spec.get('paths', {}).keys())
    removed_paths = old_paths - new_paths
    for path in removed_paths:
        changes.append(APIChange(ChangeType.BREAKING, f"Path removed: {path}", f"paths.{path}"))

    # Check for operations in common paths
    common_paths = old_paths.intersection(new_paths)
    for path in common_paths:
        old_ops_map = old_spec['paths'][path]
        new_ops_map = new_spec['paths'][path]

        old_ops = set(old_ops_map.keys())
        new_ops = set(new_ops_map.keys())

        # Standard HTTP methods
        http_methods = {'get', 'post', 'put', 'delete', 'patch', 'options', 'head', 'trace'}
        old_ops = {op for op in old_ops if op.lower() in http_methods}
        new_ops = {op for op in new_ops if op.lower() in http_methods}

        removed_ops = old_ops - new_ops
        for op in removed_ops:
            changes.append(APIChange(ChangeType.BREAKING, f"Operation {op.upper()} removed from {path}", f"paths.{path}.{op}"))

        common_ops = old_ops.intersection(new_ops)
        for op in common_ops:
            _check_operation_changes(old_ops_map[op], new_ops_map[op], path, op, changes)

    return changes

def _check_operation_changes(old_op: Dict, new_op: Dict, path: str, method: str, changes: List[APIChange]):
    # Check parameters
    # Skip parameters that are refs (missing 'name') to avoid crashes
    old_params = {p['name']: p for p in old_op.get('parameters', []) if 'name' in p}
    new_params = {p['name']: p for p in new_op.get('parameters', []) if 'name' in p}

    # Check for added required parameters
    for name, param in new_params.items():
        if param.get('required', False):
            if name not in old_params:
                changes.append(APIChange(ChangeType.BREAKING, f"New required parameter '{name}' added", f"paths.{path}.{method}.parameters.{name}"))
            elif not old_params[name].get('required', False):
                 changes.append(APIChange(ChangeType.BREAKING, f"Parameter '{name}' became required", f"paths.{path}.{method}.parameters.{name}"))

    # Check for type changes in existing parameters
    for name in old_params:
        if name in new_params:
             old_schema = old_params[name].get('schema', {})
             new_schema = new_params[name].get('schema', {})
             old_type = old_schema.get('type')
             new_type = new_schema.get('type')

             if old_type and new_type and old_type != new_type:
                 changes.append(APIChange(ChangeType.BREAKING, f"Parameter '{name}' type changed from {old_type} to {new_type}", f"paths.{path}.{method}.parameters.{name}"))

    # Check response schemas (simplistic check for now)
    # If a successful response structure changes, it could be breaking.
    # For now, let's just check if 200/201 response schema type changes.
    old_responses = old_op.get('responses', {})
    new_responses = new_op.get('responses', {})

    for code in old_responses:
        code_str = str(code)
        if code_str.startswith('2') and code in new_responses:
             # Basic check: did we change the return type?
             # Navigating deep into schema is complex, let's check high level type
             try:
                 old_content = old_responses[code].get('content', {}).get('application/json', {}).get('schema', {})
                 new_content = new_responses[code].get('content', {}).get('application/json', {}).get('schema', {})

                 old_rtype = old_content.get('type')
                 new_rtype = new_content.get('type')

                 if old_rtype and new_rtype and old_rtype != new_rtype:
                      changes.append(APIChange(ChangeType.BREAKING, f"Response {code} type changed from {old_rtype} to {new_rtype}", f"paths.{path}.{method}.responses.{code}"))
             except Exception:
                 pass # Schema might be complex or $ref
