from langchain_core.prompts import ChatPromptTemplate

# 1. Title & Metadata
TITLE_METADATA_PROMPT = ChatPromptTemplate.from_template("""
You are an expert technical writer creating a Standard Operating Procedure (SOP).
Based on the following process description, generate a professional Title, a unique SOP ID (e.g., SOP-XXX), the Version number (start at 1.0), and the Date of creation.

Process Description:
{process_description}

Output Format (Markdown):
# {{Title}}
**SOP ID:** {{SOP ID}}
**Version:** {{Version}}
**Date:** {{Date}}
""")

# 2. Purpose & Scope
PURPOSE_SCOPE_PROMPT = ChatPromptTemplate.from_template("""
Based on the process description and target audience, write the 'Purpose' and 'Scope' sections of the SOP.
- **Purpose**: Clearly state the goal of this procedure.
- **Scope**: Define what is covered and what is not covered, and who this applies to.

Process Description:
{process_description}

Target Audience:
{audience}

Output Format (Markdown):
## 1. Purpose
{{Purpose content}}

## 2. Scope
{{Scope content}}
""")

# 3. Safety & Compliance
SAFETY_COMPLIANCE_PROMPT = ChatPromptTemplate.from_template("""
Identify potential hazards, safety precautions, and compliance requirements for the following process.
List required Personal Protective Equipment (PPE) if applicable, and any warnings.

Process Description:
{process_description}

Output Format (Markdown):
## 3. Safety & Compliance
### Warnings
- {{Warning 1}}
- {{Warning 2}}

### PPE Required
- {{PPE Item 1}}
- {{PPE Item 2}}

### Compliance
- {{Compliance Note}}
""")

# 4. Procedure Steps (with Decision Trees)
PROCEDURE_STEPS_PROMPT = ChatPromptTemplate.from_template("""
Break down the process into detailed, numbered steps.
- Use clear, action-oriented language (imperative mood).
- If there are decision points, represent them clearly (e.g., "If X, go to step Y; if Z, go to step A").
- Include substeps where necessary.

Process Description:
{process_description}

Output Format (Markdown):
## 4. Procedure

1. **{{Step Title}}**
   - {{Detailed instruction}}
   - {{Substep if needed}}

2. **{{Step Title}}**
   - {{Detailed instruction}}
   *Decision Point:*
   - If {{Condition A}}: {{Action}}
   - If {{Condition B}}: {{Action}}

...
""")

# 5. Review & Approval
REVIEW_APPROVAL_PROMPT = ChatPromptTemplate.from_template("""
Generate a placeholder section for Review and Approval signatures.
Include roles typically involved in approving such a process (e.g., Process Owner, Quality Assurance, Manager).

Output Format (Markdown):
## 5. Review & Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Author | ________________ | ________________ | ________ |
| Reviewer | ________________ | ________________ | ________ |
| Approver | ________________ | ________________ | ________ |
""")

# 6. Diagram Description (for Mermaid generation)
DIAGRAM_DESCRIPTION_PROMPT = ChatPromptTemplate.from_template("""
Based on the procedure steps below, describe the flowchart logic in a way that can be converted into a Mermaid.js flowchart.
Focus on the flow of actions and decisions.

Procedure Steps:
{procedure_steps}

Output should be a list of nodes and edges logic, not the Mermaid code itself yet.
""")

# 7. Mermaid Code Generator
MERMAID_CODE_PROMPT = ChatPromptTemplate.from_template("""
Convert the following flowchart logic into a valid Mermaid.js graph TD code block.
Ensure the syntax is correct. Do not include markdown formatting (```mermaid), just the code.

Flowchart Logic:
{flowchart_logic}

Output:
graph TD
    A[Start] --> B{{Decision}}
    ...
""")
