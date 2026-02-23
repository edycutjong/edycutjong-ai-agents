# Migration File Writer Agent

An AI-powered agent that compares database schemas and generates migration files for Prisma, Alembic, and Knex.

## Features

- **Schema Comparison**: Input old and new schemas to detect changes.
- **Multi-ORM Support**: Generates migrations for Prisma (SQL), Alembic (Python), and Knex (JS/TS).
- **Rollback Scripts**: Automatically generates rollback logic.
- **Safety Analysis**: Analyzes migrations for potential data loss or locking issues.
- **Premium UI**: Modern Streamlit interface.
- **CLI Mode**: Command-line interface for automation.

## Installation

1. Navigate to the project directory:
   ```bash
   cd apps/agents/code-generation/migration-file-writer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API Key:
   - Create a `.env` file and add `OPENAI_API_KEY=your_key_here`.
   - Or pass it via CLI / UI.

## Usage

### Streamlit UI (Recommended)

Run the interactive web interface:

```bash
streamlit run app.py
```

### CLI

Run the command-line tool:

```bash
python main.py old_schema.prisma new_schema.prisma --orm prisma
```

Arguments:
- `old_schema`: Path to the old schema file.
- `new_schema`: Path to the new schema file.
- `--orm`: Target ORM (`prisma`, `alembic`, `knex`). Default: `prisma`.
- `--api-key`: Optional API key override.

## Testing

Run unit tests:

```bash
pytest tests/
```
