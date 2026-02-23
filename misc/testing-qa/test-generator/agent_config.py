import os
from crewai import Agent, Task
from langchain_openai import ChatOpenAI
from textwrap import dedent

class TestGeneratorAgents:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o"),
            temperature=0.7
        )

    def code_analyst(self):
        return Agent(
            role='Code Analyst',
            goal='Analyze python code and understand its structure, dependencies, and logic.',
            backstory=dedent("""
                You are an expert software engineer with a keen eye for detail.
                Your job is to read python source code and break it down into its components.
                You identify functions, classes, their inputs, outputs, and side effects.
                You also identify external dependencies that might need mocking.
            """),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def test_developer(self):
        return Agent(
            role='Test Developer',
            goal='Write comprehensive pytest unit tests for the analyzed code.',
            backstory=dedent("""
                You are a senior QA automation engineer.
                You specialize in writing robust, maintainable, and readable unit tests using pytest.
                You cover happy paths, edge cases, and error conditions.
                You are expert at using mocks, fixtures, and parameterization.
                You ensure high code coverage.
            """),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def qa_engineer(self):
        return Agent(
            role='QA Engineer',
            goal='Review generated tests for correctness, style, and completeness.',
            backstory=dedent("""
                You are a meticulous QA lead.
                You review test code to ensure it follows best practices.
                You check if the tests actually test the logic and aren't just tautologies.
                You verify that mocks are used correctly and that no external calls are made during unit tests.
                You ensure the code is valid python.
            """),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

class TestGeneratorTasks:
    def analyze_code_task(self, agent, code_content):
        return Task(
            description=dedent(f"""
                Analyze the following Python code:

                ```python
                {code_content}
                ```

                Identify:
                1. All functions and methods.
                2. Input parameters and their types.
                3. Return types.
                4. External dependencies and side effects (API calls, file I/O, database access).
                5. Logic branches that need testing.

                Produce a detailed report of the code structure.
            """),
            agent=agent,
            expected_output="A detailed report of the code structure, functions, parameters, and dependencies."
        )

    def write_tests_task(self, agent):
        return Task(
            description=dedent(f"""
                Based on the code analysis provided in the previous task, write a complete python test file using `pytest`.

                Requirements:
                1. Import the necessary modules.
                2. Use `pytest` fixtures where appropriate.
                3. Mock all external dependencies identified in the analysis.
                4. Write tests for:
                   - Happy paths (valid inputs).
                   - Edge cases (boundary values, empty inputs, nulls).
                   - Error conditions (exceptions raised).
                5. Use `pytest.mark.parametrize` for data-driven tests.
                6. Ensure the code is syntactically correct and follows PEP 8.
                7. Output ONLY the python code for the test file. Do not include markdown formatting like ```python.
            """),
            agent=agent,
            expected_output="A valid python file content containing pytest unit tests."
        )

    def review_tests_task(self, agent):
        return Task(
            description=dedent(f"""
                Review the test code generated in the previous task.

                Check for:
                1. Syntax errors.
                2. Missing imports.
                3. Correct usage of mocks.
                4. Logical correctness of assertions.
                5. Completeness of coverage based on the analysis.

                If the code is good, output the code as is.
                If there are issues, fix them and output the corrected code.
                Output ONLY the final python code. Do not include markdown formatting.
            """),
            agent=agent,
            expected_output="The final, reviewed, and corrected python test code."
        )
