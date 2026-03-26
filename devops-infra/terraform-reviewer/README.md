# Terraform Reviewer

Reviews Terraform and IaC plans, flags security risks and cost implications.

## Features
- Parse Terraform HCL files
- Flag security misconfigurations
- Estimate resource costs
- Detect drift from state
- Suggest best practices
- Validate naming conventions
- Check for hardcoded values
- Generate review report

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
