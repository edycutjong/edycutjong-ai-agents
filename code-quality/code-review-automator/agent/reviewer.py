import logging
import json
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from unidiff import PatchSet

try:
    from ..prompts.review_prompts import REVIEW_SYSTEM_PROMPT, SUMMARY_SYSTEM_PROMPT
except ImportError:
    # Fallback for when running tests or scripts where parent package context is lost
    import sys
    import os
    # Add parent directory to path if not present
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from prompts.review_prompts import REVIEW_SYSTEM_PROMPT, SUMMARY_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class Reviewer:
    def __init__(self, openai_api_key: str, model_name: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(api_key=openai_api_key, model=model_name, temperature=0.2)

    def analyze_diff(self, diff_data: List[Dict], guidelines: str = "", focus: List[str] = None) -> Dict[str, Any]:
        """
        Analyzes the diff and returns a structured review.
        diff_data: List of dicts with 'filename', 'patch', etc.
        guidelines: Custom review guidelines.
        focus: List of categories to focus on (e.g., ['Logic', 'Security']).
        """
        if not focus:
            focus = ["Logic", "Security", "Style"]

        comments = []
        full_diff_text = ""

        # We process each file individually to keep context clear and avoid token limits if possible
        # For very large PRs, we might need more sophisticated chunking.
        for file_data in diff_data:
            filename = file_data['filename']
            patch = file_data['patch']

            # fast-fail for huge files or lock files
            if filename.endswith('.lock') or len(patch) > 10000:
                logger.info(f"Skipping large/lock file: {filename}")
                continue

            full_diff_text += f"\nFile: {filename}\n{patch}\n"

            file_comments = self._analyze_file(filename, patch, guidelines, focus)
            comments.extend(file_comments)

        # Generate summary based on all comments and the diff
        summary = self._generate_summary(full_diff_text, comments)

        return {
            "summary": summary,
            "comments": comments
        }

    def _analyze_file(self, filename: str, patch: str, guidelines: str, focus: List[str]) -> List[Dict]:
        """
        Analyzes a single file's patch.
        Returns a list of comment dicts.
        """
        system_prompt = REVIEW_SYSTEM_PROMPT.format(
            focus_categories=", ".join(focus),
            guidelines=guidelines
        )

        user_message = f"File: {filename}\n\nDiff:\n{patch}"

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{input}")
        ])

        chain = prompt | self.llm | JsonOutputParser()

        try:
            result = chain.invoke({"input": user_message})
            comments = result.get("comments", [])

            # Post-processing: Add filename to each comment
            for c in comments:
                c['filename'] = filename

            return self.verify_hallucinations(comments, patch)

        except Exception as e:
            logger.error(f"Error analyzing file {filename}: {e}")
            return []

    def _generate_summary(self, diff_text: str, comments: List[Dict]) -> str:
        """
        Generates a summary of the review.
        """
        comments_summary = json.dumps(comments, indent=2)
        # Truncate diff_text if too long
        if len(diff_text) > 5000:
            diff_text = diff_text[:5000] + "...(truncated)"

        user_message = f"Diff Content (excerpt):\n{diff_text}\n\nComments Generated:\n{comments_summary}"

        prompt = ChatPromptTemplate.from_messages([
            ("system", SUMMARY_SYSTEM_PROMPT),
            ("user", "{input}")
        ])

        chain = prompt | self.llm
        try:
            res = chain.invoke({"input": user_message})
            return res.content
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "Could not generate summary."

    def verify_hallucinations(self, comments: List[Dict], patch_text: str) -> List[Dict]:
        """
        Verifies that the commented lines actually exist in the changed part of the file.
        Uses `unidiff` to parse the patch.
        """
        try:
            # unidiff expects a complete diff/patch format.
            # PyGithub returns just the hunk (usually). We might need to wrap it.
            # But let's try parsing it as a patch string directly.
            # Usually patches from GH start with `@@ ... @@`.
            # Unidiff expects a header like `--- a/file` usually, but `PatchSet` might handle fragments if formatted right.
            # The safest way is to construct a dummy header.

            # Or, we can manually parse the line numbers from the patch string.
            # "@@ -old,count +new,count @@"

            # Let's use a simple manual parser for validation since we just need to check if a line number is "in the diff".
            # A line is valid for commenting if it is in the "new" file version and preferably in the added/context lines of the hunk.

            valid_lines = set()
            current_new_line = 0

            for line in patch_text.split('\n'):
                if line.startswith('@@'):
                    # Parse header: @@ -1,5 +1,5 @@
                    # We want the second pair (+1,5) which corresponds to the new file.
                    try:
                        parts = line.split(' ')
                        new_hunk_info = parts[2] # "+1,5"
                        start_line = int(new_hunk_info.split(',')[0].replace('+', ''))
                        current_new_line = start_line
                    except:
                        continue
                elif line.startswith('+'):
                    valid_lines.add(current_new_line)
                    current_new_line += 1
                elif line.startswith(' '):
                    valid_lines.add(current_new_line)
                    current_new_line += 1
                elif line.startswith('-'):
                    # Removed line, doesn't increment new file line counter
                    pass

            verified_comments = []
            for comment in comments:
                try:
                    line_num = int(comment.get('line'))
                    if line_num in valid_lines:
                        comment['line'] = line_num  # Update to integer
                        verified_comments.append(comment)
                    else:
                        logger.warning(f"Hallucination detected: Line {line_num} not in diff for {comment.get('filename')}. Dropping comment.")
                except (ValueError, TypeError):
                    logger.warning(f"Invalid line number format: {comment.get('line')} for {comment.get('filename')}. Dropping comment.")

            return verified_comments

        except Exception as e:
            logger.error(f"Error verifying hallucinations: {e}")
            # If verification fails, we return the comments but flag them?
            # Or just return them all to be safe?
            # Let's return them all but log the error.
            return comments
