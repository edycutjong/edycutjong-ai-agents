# Database Diagram Generator

Reads database schemas (SQL/ORM) and generates ERD diagrams in Mermaid or PlantUML.

## Features
- Parse SQL CREATE TABLE statements
- Read ORM model definitions (SQLAlchemy/Prisma)
- Generate Mermaid ERD diagrams
- Generate PlantUML diagrams
- Show relationships and cardinality
- Color-code tables by module
- Export as SVG/PNG
- Support PostgreSQL/MySQL/SQLite

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
