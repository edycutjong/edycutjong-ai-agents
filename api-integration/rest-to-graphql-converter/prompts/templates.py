from langchain_core.prompts import PromptTemplate

# Prompt for generating GraphQL Types
GRAPHQL_TYPES_PROMPT = PromptTemplate(
    input_variables=["schemas", "api_summary"],
    template="""
You are an expert GraphQL Architect. Your task is to generate GraphQL Type Definitions based on the provided REST API Schemas.

API Summary:
{api_summary}

REST API Schemas (JSON/YAML format):
{schemas}

Instructions:
1. Analyze the provided schemas.
2. Convert each schema into a GraphQL `type`.
3. Use appropriate GraphQL scalar types (Int, Float, String, Boolean, ID).
4. Identify relationships and use object types for nested structures.
5. Add comments/descriptions to fields based on the schema descriptions.
6. Do NOT generate Query or Mutation types yet, just the data types.
7. Output ONLY the GraphQL SDL for the types.

GraphQL Types:
"""
)

# Prompt for generating Queries and Mutations
GRAPHQL_OPERATIONS_PROMPT = PromptTemplate(
    input_variables=["endpoints", "api_summary", "existing_types"],
    template="""
You are an expert GraphQL Architect. Your task is to generate the `Query` and `Mutation` types for a GraphQL schema, based on REST API endpoints.

API Summary:
{api_summary}

Existing GraphQL Types:
{existing_types}

REST API Endpoints:
{endpoints}

Instructions:
1. Map GET requests to fields in the `Query` type.
2. Map POST, PUT, PATCH, DELETE requests to fields in the `Mutation` type.
3. Name the fields following GraphQL best practices (camelCase, descriptive).
   - e.g., `GET /users` -> `users` or `getUsers`
   - e.g., `POST /users` -> `createUser`
   - e.g., `GET /users/{{id}}` -> `user(id: ID!)`
4. Define appropriate arguments for each field based on path parameters and query parameters.
5. Use the provided "Existing GraphQL Types" for return types.
6. If an endpoint returns a list, wrap the type in `[]`.
7. Output ONLY the GraphQL SDL for `type Query` and `type Mutation`.

GraphQL Operations:
"""
)

# Prompt for generating Resolvers
RESOLVER_GENERATOR_PROMPT = PromptTemplate(
    input_variables=["language", "schema_sdl", "endpoints"],
    template="""
You are an expert Backend Developer. Your task is to generate GraphQL Resolvers in {language} for the provided GraphQL Schema, mapping them to the original REST API endpoints.

GraphQL Schema:
{schema_sdl}

Original REST API Endpoints:
{endpoints}

Instructions:
1. Generate code in {language} (e.g., Python with Ariadne/Strawberry, or Node.js with Apollo Server).
2. For each field in `Query` and `Mutation`, write a resolver function.
3. The resolver should make an HTTP request to the corresponding REST endpoint.
   - Use `requests` for Python or `fetch`/`axios` for Node.js.
   - Pass arguments from the GraphQL query to the REST API request (path params, query params, body).
4. Handle basic errors.
5. Provide a complete, runnable file or module structure.
6. Include necessary imports.

Resolver Code:
"""
)

# Prompt for generating Migration Guide
MIGRATION_GUIDE_PROMPT = PromptTemplate(
    input_variables=["api_summary", "schema_sdl", "endpoints"],
    template="""
You are a Technical Writer. Your task is to create a Migration Guide for developers moving from the REST API to the new GraphQL API.

API Summary:
{api_summary}

New GraphQL Schema:
{schema_sdl}

Original REST API Endpoints:
{endpoints}

Instructions:
1. Create a Markdown document.
2. Explain the key differences between the old REST API and the new GraphQL API.
3. Provide a mapping table: REST Endpoint -> GraphQL Query/Mutation.
4. Give examples of how to fetch data in GraphQL versus the old REST way.
   - Example: Fetching a user and their posts.
5. Highlight any benefits (e.g., fetching nested data in one request).

Migration Guide:
"""
)
