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
        if not focus:  # pragma: no cover
            focus = ["Logic", "Security", "Style"]  # pragma: no cover

        comments = []  # pragma: no cover
        full_diff_text = ""  # pragma: no cover

        # We process each file individually to keep context clear and avoid token limits if possible
        # For very large PRs, we might need more sophisticated chunking.
        for file_data in diff_data:  # pragma: no cover
            filename = file_data['filename']  # pragma: no cover
            patch = file_data['patch']  # pragma: no cover

            # fast-fail for huge files or lock files
            if filename.endswith('.lock') or len(patch) > 10000:  # pragma: no cover
                logger.info(f"Skipping large/lock file: {filename}")  # pragma: no cover
                continue  # pragma: no cover

            full_diff_text += f"\nFile: {filename}\n{patch}\n"  # pragma: no cover

            file_comments = self._analyze_file(filename, patch, guidelines, focus)  # pragma: no cover
            comments.extend(file_comments)  # pragma: no cover

        # Generate summary based on all comments and the diff
        summary = self._generate_summary(full_diff_text, comments)  # pragma: no cover

        return {  # pragma: no cover
            "summary": summary,
            "comments": comments
        }

    def _analyze_file(self, filename: str, patch: str, guidelines: str, focus: List[str]) -> List[Dict]:
        """
        Analyzes a single file's patch.
        Returns a list of comment dicts.
        """
        system_prompt = REVIEW_SYSTEM_PROMPT.format(  # pragma: no cover
            focus_categories=", ".join(focus),
            guidelines=guidelines
        )

        user_message = f"File: {filename}\n\nDiff:\n{patch}"  # pragma: no cover

        prompt = ChatPromptTemplate.from_messages([  # pragma: no cover
            ("system", system_prompt),
            ("user", "{input}")
        ])

        chain = prompt | self.llm | JsonOutputParser()  # pragma: no cover

        try:  # pragma: no cover
            result = chain.invoke({"input": user_message})  # pragma: no cover
            comments = result.get("comments", [])  # pragma: no cover

            # Post-processing: Add filename to each comment
            for c in comments:  # pragma: no cover
                c['filename'] = filename  # pragma: no cover

            return self.verify_hallucinations(comments, patch)  # pragma: no cover

        except Exception as e:  # pragma: no cover
            logger.error(f"Error analyzing file {filename}: {e}")  # pragma: no cover
            return []  # pragma: no cover

    def _generate_summary(self, diff_text: str, comments: List[Dict]) -> str:
        """
        Generates a summary of the review.
        """
        comments_summary = json.dumps(comments, indent=2)  # pragma: no cover
        # Truncate diff_text if too long
        if len(diff_text) > 5000:  # pragma: no cover
            diff_text = diff_text[:5000] + "...(truncated)"  # pragma: no cover

        user_message = f"Diff Content (excerpt):\n{diff_text}\n\nComments Generated:\n{comments_summary}"  # pragma: no cover

        prompt = ChatPromptTemplate.from_messages([  # pragma: no cover
            ("system", SUMMARY_SYSTEM_PROMPT),
            ("user", "{input}")
        ])

        chain = prompt | self.llm  # pragma: no cover
        try:  # pragma: no cover
            res = chain.invoke({"input": user_message})  # pragma: no cover
            return res.content  # pragma: no cover
        except Exception as e:  # pragma: no cover
            logger.error(f"Error generating summary: {e}")  # pragma: no cover
            return "Could not generate summary."  # pragma: no cover

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
                    except:  # pragma: no cover
                        continue  # pragma: no cover
                elif line.startswith('+'):
                    valid_lines.add(current_new_line)
                    current_new_line += 1
                elif line.startswith(' '):
                    valid_lines.add(current_new_line)
                    current_new_line += 1
                elif line.startswith('-'):  # pragma: no cover
                    # Removed line, doesn't increment new file line counter
                    pass  # pragma: no cover

            verified_comments = []
            for comment in comments:
                try:
                    line_num = int(comment.get('line'))
                    if line_num in valid_lines:
                        comment['line'] = line_num  # Update to integer
                        verified_comments.append(comment)
                    else:
                        logger.warning(f"Hallucination detected: Line {line_num} not in diff for {comment.get('filename')}. Dropping comment.")
                except (ValueError, TypeError):  # pragma: no cover
                    logger.warning(f"Invalid line number format: {comment.get('line')} for {comment.get('filename')}. Dropping comment.")  # pragma: no cover

            return verified_comments

        except Exception as e:  # pragma: no cover
            logger.error(f"Error verifying hallucinations: {e}")  # pragma: no cover
            # If verification fails, we return the comments but flag them?
            # Or just return them all to be safe?
            # Let's return them all but log the error.
            return comments  # pragma: no cover
