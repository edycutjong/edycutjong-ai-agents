import os
import json
import re
from typing import List, Dict, Any

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

# Add project root to sys.path for consistent imports from pytest and CLI
import sys as _sys
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _project_root not in _sys.path:
    _sys.path.insert(0, _project_root)

from prompts.claim_extraction import claim_extraction_prompt
from prompts.verification import verification_prompt
from agent.document_loader import load_document, split_documents
from config import OPENAI_API_KEY


class HallucinationDetector:
    def __init__(self, api_key=None):
        self.api_key = api_key or OPENAI_API_KEY
        if not self.api_key:
            # For testing without key, we might mock. But for real usage it's needed.
            print("Warning: OpenAI API Key not found. Set OPENAI_API_KEY environment variable.")

        self.llm = ChatOpenAI(temperature=0, openai_api_key=self.api_key, model="gpt-3.5-turbo")
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)

    def extract_claims(self, text: str) -> List[str]:
        """
        Extracts factual claims from the given text using the LLM.
        """
        chain = claim_extraction_prompt | self.llm
        response = chain.invoke({"text": text})
        result = response.content

        # Parse the numbered list
        claims = []
        for line in result.split('\n'):
            line = line.strip()
            # Regex to match "1. " or "1) " or "- "
            if re.match(r'^(\d+[\.\)]|-)\s+', line):
                parts = re.split(r'^(\d+[\.\)]|-)\s+', line, maxsplit=1)
                if len(parts) > 2:
                    claims.append(parts[2].strip())
            elif line:
                # If it's a non-empty line but doesn't start with number,
                # check if it looks like a claim (heuristic).
                # For now, maybe just skip or append if it seems like a continuation.
                pass

        return claims

    def verify_claim(self, claim: str, vectorstore) -> Dict[str, Any]:
        """
        Verifies a single claim against the source documents in the vectorstore.
        """
        # Retrieve relevant documents
        docs = vectorstore.similarity_search(claim, k=3)
        context_text = "\n\n".join([doc.page_content for doc in docs])

        # Verify
        chain = verification_prompt | self.llm
        response = chain.invoke({"claim": claim, "source_text": context_text})
        result_json_str = response.content

        # Parse JSON
        try:
            # Robust JSON extraction: look for the first '{' and last '}'
            match = re.search(r'\{.*\}', result_json_str, re.DOTALL)
            if match:
                clean_json = match.group(0)
                result = json.loads(clean_json)
            else:
                 raise json.JSONDecodeError("No JSON object found", result_json_str, 0)
        except json.JSONDecodeError as e:
             # Fallback if JSON is malformed
            print(f"JSON Parse Error: {e}\nRaw output: {result_json_str}")
            result = {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": f"Failed to parse verification result. Raw: {result_json_str[:50]}..."
            }

        return {
            "claim": claim,
            "status": result.get("status", "UNKNOWN"),
            "confidence": result.get("confidence", 0.0),
            "explanation": result.get("explanation", "No explanation provided."),
            "sources": [doc.page_content for doc in docs]
        }

    def process_document(self, source_file_path: str):
         # 1. Load and process source documents
        raw_docs = load_document(source_file_path)
        chunks = split_documents(raw_docs)

        # 2. Create VectorStore
        # Note: If chunks is empty, this will fail.
        if not chunks:
            raise ValueError("No text extracted from source document.")

        vectorstore = FAISS.from_documents(chunks, self.embeddings)
        return vectorstore

    def process(self, ai_text: str, source_file_path: str) -> Dict[str, Any]:
        """
        Main process: Load source, extract claims, verify each.
        """
        vectorstore = self.process_document(source_file_path)

        # 3. Extract claims
        claims = self.extract_claims(ai_text)

        if not claims:
             return {"score": 0, "results": [], "message": "No claims extracted."}

        # 4. Verify each claim
        results = []
        verified_count = 0

        for claim in claims:
            verification = self.verify_claim(claim, vectorstore)
            results.append(verification)
            if verification["status"] == "VERIFIED":
                verified_count += 1

        # 5. Calculate overall score
        total = len(claims)
        score = (verified_count / total) * 100 if total > 0 else 0

        return {
            "score": score,
            "results": results,
            "total_claims": total,
            "verified_claims": verified_count
        }
