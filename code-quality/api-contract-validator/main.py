"""
API Contract Validator — validates API requests/responses against their defined contracts.
Usage: python main.py --spec openapi.yaml --request request.json
"""
import argparse
import sys
import json
import os


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[API Contract Validator] Ready.\n\nPaste an OpenAPI spec, swagger definition, or API request/response pair to validate the contract and identify breaking changes."


def validate_json_schema_basic(data: dict, schema: dict) -> list:
    """Basic JSON schema validation (required fields + types)."""
    errors = []
    required = schema.get("required", [])
    properties = schema.get("properties", {})
    for field in required:
        if field not in data:
            errors.append(f"❌ Missing required field: '{field}'")
    for field, value in data.items():
        if field in properties:
            expected_type = properties[field].get("type")
            actual_type = type(value).__name__
            type_map = {"string": str, "integer": int, "number": (int, float), "boolean": bool, "array": list, "object": dict}
            if expected_type and expected_type in type_map:
                if not isinstance(value, type_map[expected_type]):
                    errors.append(f"⚠️  Field '{field}': expected {expected_type}, got {actual_type}")
    return errors


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

    schema = {}
    if args.schema and os.path.isfile(args.schema):
        with open(args.schema) as f:
            schema = json.load(f)

    data = {}
    if args.data and os.path.isfile(args.data):
        with open(args.data) as f:
            data = json.load(f)
    elif args.input:
        try:
            data = json.loads(args.input)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON input: {e}")
            sys.exit(1)

    if not schema:
        print("⚠️  No schema provided — performing basic JSON syntax check only.")
        print(f"✅ JSON is valid. Keys: {list(data.keys()) if isinstance(data, dict) else 'array'}")
        sys.exit(0)

    errors = validate_json_schema_basic(data, schema)
    if errors:
        print(f"\n❌ Validation failed ({len(errors)} error(s)):")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("✅ Data matches the contract schema.")


if __name__ == "__main__":
    main()
