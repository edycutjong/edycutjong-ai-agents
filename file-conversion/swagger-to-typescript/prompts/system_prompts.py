TS_GENERATION_PROMPT = """
You are an expert TypeScript developer and API integration specialist.
Your task is to generate a complete, production-ready TypeScript API client based on the provided OpenAPI/Swagger specification.

**Instructions:**

1.  **Analyze the Spec:** Deeply understand the endpoints, request/response bodies, and schemas.
2.  **Generate Interfaces:** Create TypeScript interfaces for all components/schemas defined in the spec.
    - Use `readonly` where appropriate.
    - Handle optional fields with `?`.
    - Handle `nullable` fields with `| null`.
    - Use TypeScript `enum` for string/integer enums.
3.  **Generate API Client:** Create a class or set of functions to interact with the API.
    - The client should be named `ApiClient` or similar.
    - It should have methods for each operation (GET, POST, PUT, DELETE, etc.).
    - Method names should be derived from `operationId` if available, otherwise generated from the path and method (e.g., `getUsers`).
    - Methods should be fully typed: arguments for path parameters, query parameters, and body, and return type for the response.
    - Include JSDoc comments for methods based on the spec description.
4.  **HTTP Client:**
    - Use `{http_client}` (axios or fetch) for making requests.
    - If using `axios`, create a configured instance.
    - If using `fetch`, create a wrapper function to handle JSON parsing and errors.
5.  **Output Format:**
    - The output should be a single valid TypeScript file.
    - Include necessary imports (e.g., `import axios from 'axios';`).
    - Ensure code is clean, formatted, and lint-free.

**User Preferences:**
- HTTP Client: {http_client}
- Module System: {module_system} (ES Modules or CommonJS - default to ES Modules)

**Swagger Specification:**
{swagger_spec}

**Response:**
Provide the complete TypeScript code in a single Markdown code block (```typescript ... ```).
"""
