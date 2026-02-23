# Invoice Generator 🧾

Generate professional invoices with line items, tax calculation, multi-currency support, and Markdown/text output.

## Quick Start
```bash
pip install -r requirements.txt
python main.py create --from-name "My Corp" --to-name "Client" --items "Web Dev,40,150" "Hosting,1,99,0.10" --markdown
python main.py list
python main.py show INV-20260219-ABCD
python -m pytest tests/ -v
```
