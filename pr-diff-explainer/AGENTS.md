## Overview
Agent that translates pull request diffs into clear, non-technical explanations.

## Inputs
- Git diff or PR URL
- Optional audience type (exec, product, QA)

## Outputs
- Plain-language summary
- Risk assessment
- Key changes grouped by feature

## Capabilities
- Parse unified diffs
- Detect file types and intent
- Map code changes to product impact

## Constraints
- Avoid jargon
- Do not hallucinate intent beyond diff

## Workflow
1. Parse diff
2. Cluster changes
3. Translate to plain language
4. Generate summary + risks

## Edge Cases
- Large PRs: summarize per directory
- Renames vs edits
