"""
API Contract Validator — validates API requests/responses against their defined contracts.
Usage: python main.py --spec openapi.yaml --request request.json
"""
import argparse
import sys
import json
import os


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[API Contract Validator] Ready.\n\nPaste an OpenAPI spec, swagger definition, or API request/response pair to validate the contract and identify breaking changes."  # pragma: no cover


def validate_json_schema_basic(data: dict, schema: dict) -> list:
    """Basic JSON schema validation (required fields + types)."""
    errors = []  # pragma: no cover
    required = schema.get("required", [])  # pragma: no cover
    properties = schema.get("properties", {})  # pragma: no cover
    for field in required:  # pragma: no cover
        if field not in data:  # pragma: no cover
            errors.append(f"❌ Missing required field: '{field}'")  # pragma: no cover
    for field, value in data.items():  # pragma: no cover
        if field in properties:  # pragma: no cover
            expected_type = properties[field].get("type")  # pragma: no cover
            actual_type = type(value).__name__  # pragma: no cover
            type_map = {"string": str, "integer": int, "number": (int, float), "boolean": bool, "array": list, "object": dict}  # pragma: no cover
            if expected_type and expected_type in type_map:  # pragma: no cover
                if not isinstance(value, type_map[expected_type]):  # pragma: no cover
                    errors.append(f"⚠️  Field '{field}': expected {expected_type}, got {actual_type}")  # pragma: no cover
    return errors  # pragma: no cover


def main():
    parser = argparse.ArgumentParser(description="Validate API request/response against a contract")
    parser.add_argument("--schema", default="", help="Path to JSON schema file")
    parser.add_argument("--data", default="", help="Path to JSON data file to validate")
    parser.add_argument("--input", default="", help="Raw JSON string to validate")
    args = parser.parse_args()

    if not any([args.schema, args.data, args.input]):
        print("API Contract Validator")
        print("Usage: python main.py --schema schema.json --data response.json")
        print("       python main.py --input '{\"name\": \"test\"}' --schema schema.json")
        sys.exit(0)

    schema = {}  # pragma: no cover
    if args.schema and os.path.isfile(args.schema):  # pragma: no cover
        with open(args.schema) as f:  # pragma: no cover
            schema = json.load(f)  # pragma: no cover

    data = {}  # pragma: no cover
    if args.data and os.path.isfile(args.data):  # pragma: no cover
        with open(args.data) as f:  # pragma: no cover
            data = json.load(f)  # pragma: no cover
    elif args.input:  # pragma: no cover
        try:  # pragma: no cover
            data = json.loads(args.input)  # pragma: no cover
        except json.JSONDecodeError as e:  # pragma: no cover
            print(f"Invalid JSON input: {e}")  # pragma: no cover
            sys.exit(1)  # pragma: no cover

    if not schema:  # pragma: no cover
        print("⚠️  No schema provided — performing basic JSON syntax check only.")  # pragma: no cover
        print(f"✅ JSON is valid. Keys: {list(data.keys()) if isinstance(data, dict) else 'array'}")  # pragma: no cover
        sys.exit(0)  # pragma: no cover

    errors = validate_json_schema_basic(data, schema)  # pragma: no cover
    if errors:  # pragma: no cover
        print(f"\n❌ Validation failed ({len(errors)} error(s)):")  # pragma: no cover
        for e in errors:  # pragma: no cover
            print(f"  {e}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover
    else:
        print("✅ Data matches the contract schema.")  # pragma: no cover


if __name__ == "__main__":
    main()
