from langchain_core.prompts import ChatPromptTemplate

FAITHFULNESS_PROMPT = ChatPromptTemplate.from_template("""
You are an expert evaluator. Your task is to evaluate the faithfulness of an answer given a context.
Score the faithfulness on a scale from 0 to 1, where 1 means the answer is fully supported by the context and 0 means it is not supported at all.

Context:
{context}

Answer:
{answer}

Return ONLY the score as a float between 0 and 1.
""")

ANSWER_RELEVANCE_PROMPT = ChatPromptTemplate.from_template("""
You are an expert evaluator. Your task is to evaluate the relevance of an answer to a question.
Score the relevance on a scale from 0 to 1, where 1 means the answer directly addresses the question and 0 means it is irrelevant.

Question:
{question}

Answer:
{answer}

Return ONLY the score as a float between 0 and 1.
""")

CONTEXT_PRECISION_PROMPT = ChatPromptTemplate.from_template("""
You are an expert evaluator. Your task is to evaluate the precision of the retrieved context for a given question.
Score the precision on a scale from 0 to 1, where 1 means the context contains all necessary information to answer the question, and 0 means it contains no relevant information.

Question:
{question}

Context:
{context}

Return ONLY the score as a float between 0 and 1.
""")
