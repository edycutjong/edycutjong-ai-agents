from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from .analysis import Analyzer
import numpy as np

class ChatAgent:
    def __init__(self, embeddings, metadata, api_key, embedder):
        self.embeddings = embeddings
        self.metadata = metadata  # List of strings corresponding to embeddings
        self.api_key = api_key
        self.embedder = embedder # Instance of Embedder class
        self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
        self.tools = self._create_tools()
        self.agent_executor = self._initialize_agent()

    def describe_dataset(self) -> str:
        """Returns basic statistics about the dataset."""
        if self.embeddings is None:
            return "No data loaded."

        n_samples, n_features = self.embeddings.shape
        return f"The dataset contains {n_samples} samples with {n_features} dimensions."

    def get_sample_data(self, n: int = 5) -> list:
        """Returns a sample of the data (metadata)."""
        if not self.metadata:
            return ["No metadata available."]
        return self.metadata[:n]

    def search_knowledge_base(self, query: str) -> str:
        """Search for relevant information in the uploaded documents using vector similarity."""
        if not query:
            return "Please provide a query."
        if self.embeddings is None or len(self.embeddings) == 0:
            return "No embeddings available to search."

        try:
            query_vec = self.embedder.embed_query(query)
            if query_vec is None:
                return "Failed to embed query."

            # Find nearest neighbors
            indices, distances = Analyzer.find_nearest_neighbors(self.embeddings, query_vec, k=5)

            # Retrieve corresponding text chunks
            results = []
            for i, idx in enumerate(indices):
                score = 1 - distances[i] # Convert distance to similarity score approx if using cosine distance
                # Note: NearestNeighbors uses Euclidean distance by default.
                # For normalized vectors, Euclidean distance relates to Cosine Similarity.
                # We'll just return the text.
                if idx < len(self.metadata):
                    results.append(f"Chunk {i+1}:\n{self.metadata[idx]}")

            return "\n\n".join(results)
        except Exception as e:
            return f"Error during search: {e}"

    def _create_tools(self):
        return [
            StructuredTool.from_function(
                func=self.describe_dataset,
                name="describe_dataset",
                description="Get basic statistics about the dataset like number of samples and dimensions."
            ),
            StructuredTool.from_function(
                func=self.get_sample_data,
                name="get_sample_data",
                description="Get a sample of the metadata/text associated with the embeddings."
            ),
            StructuredTool.from_function(
                func=self.search_knowledge_base,
                name="search_knowledge_base",
                description="Search for relevant information in the uploaded documents using vector similarity. Use this to answer questions about the content."
            )
        ]

    def _initialize_agent(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant for analyzing vector embeddings. Use the provided tools to inspect the data. When asked about content, use 'search_knowledge_base' to find relevant info."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def run(self, query):
        if not query:
            return "Please ask a question."
        try:
            result = self.agent_executor.invoke({"input": query})
            return result["output"]
        except Exception as e:
            return f"Error running agent: {e}"
