from .schema_parser import SchemaParser
from .llm_engine import LLMEngine
from .mongo_generator import MongoGenerator
from .dynamo_generator import DynamoGenerator
from .migration_generator import MigrationGenerator

class Converter:
    def __init__(self):
        self.parser = SchemaParser()
        self.llm = LLMEngine()
        self.mongo_gen = MongoGenerator(self.llm)
        self.dynamo_gen = DynamoGenerator(self.llm)
        self.migration_gen = MigrationGenerator(self.llm)

    def run(self, sql_content: str, target_db: str, strategy: str = "embed"):
        # 1. Parse SQL
        sql_schema = self.parser.parse(sql_content)
        if not sql_schema:
            return {"error": "Failed to parse SQL or no tables found."}

        # 2. Generate NoSQL Schema
        nosql_schema = ""
        if target_db.lower() == "mongodb":
            nosql_schema = self.mongo_gen.generate_schema(sql_schema, strategy)
        elif target_db.lower() == "dynamodb":
            nosql_schema = self.dynamo_gen.generate_schema(sql_schema, strategy)
        else:
            return {"error": f"Unsupported target database: {target_db}"}

        # 3. Generate Migration Script
        migration_script = self.migration_gen.generate_script(sql_schema, nosql_schema, target_db, strategy)

        # 4. Generate Documentation
        documentation = self._generate_docs(sql_schema, nosql_schema, target_db, strategy)

        return {
            "sql_schema": sql_schema,
            "nosql_schema": nosql_schema,
            "migration_script": migration_script,
            "documentation": documentation
        }

    def _generate_docs(self, sql_schema, nosql_schema, target_db, strategy):
        return f"""
# Migration Documentation

## Source SQL Schema
{len(sql_schema)} tables found.

## Target {target_db} Schema
Strategy used: {strategy}

## Migration Plan
1. Connect to SQL source.
2. Read data from tables.
3. Transform data according to new schema (embedding/referencing).
4. Write to {target_db}.

See the generated migration script for implementation details.
"""
