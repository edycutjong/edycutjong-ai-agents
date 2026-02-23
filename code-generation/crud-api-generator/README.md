# CRUD API Generator 🔧
Generate Express.js and FastAPI CRUD routes from model definitions.
## Quick Start
```bash
python main.py generate "User: name:string, email:string" --framework express
python main.py generate "Product: title:string, price:number" --framework fastapi
python -m pytest tests/ -v
```
