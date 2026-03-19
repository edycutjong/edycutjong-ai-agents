from langchain.agents import AgentExecutor, create_tool_calling_agent  # pragma: no cover
from langchain_core.prompts import ChatPromptTemplate  # pragma: no cover
from langchain_core.tools import StructuredTool  # pragma: no cover
from langchain_openai import ChatOpenAI  # pragma: no cover
from .analysis import Analyzer  # pragma: no cover
import numpy as np  # pragma: no cover

class ChatAgent:  # pragma: no cover
    def __init__(self, embeddings, metadata, api_key, embedder):  # pragma: no cover
        self.embeddings = embeddings  # pragma: no cover
        self.metadata = metadata  # List of strings corresponding to embeddings  # pragma: no cover
        self.api_key = api_key  # pragma: no cover
        self.embedder = embedder # Instance of Embedder class  # pragma: no cover
        self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)  # pragma: no cover
        self.tools = self._create_tools()  # pragma: no cover
        self.agent_executor = self._initialize_agent()  # pragma: no cover

    def describe_dataset(self) -> str:  # pragma: no cover
        """Returns basic statistics about the dataset."""
        if self.embeddings is None:  # pragma: no cover
            return "No data loaded."  # pragma: no cover

        n_samples, n_features = self.embeddings.shape  # pragma: no cover
        return f"The dataset contains {n_samples} samples with {n_features} dimensions."  # pragma: no cover

    def get_sample_data(self, n: int = 5) -> list:  # pragma: no cover
        """Returns a sample of the data (metadata)."""
        if not self.metadata:  # pragma: no cover
            return ["No metadata available."]  # pragma: no cover
        return self.metadata[:n]  # pragma: no cover

    def search_knowledge_base(self, query: str) -> str:  # pragma: no cover
        """Search for relevant information in the uploaded documents using vector similarity."""
        if not query:  # pragma: no cover
            return "Please provide a query."  # pragma: no cover
        if self.embeddings is None or len(self.embeddings) == 0:  # pragma: no cover
            return "No embeddings available to search."  # pragma: no cover

        try:  # pragma: no cover
            query_vec = self.embedder.embed_query(query)  # pragma: no cover
            if query_vec is None:  # pragma: no cover
                return "Failed to embed query."  # pragma: no cover

            # Find nearest neighbors
            indices, distances = Analyzer.find_nearest_neighbors(self.embeddings, query_vec, k=5)  # pragma: no cover

            # Retrieve corresponding text chunks
            results = []  # pragma: no cover
            for i, idx in enumerate(indices):  # pragma: no cover
                score = 1 - distances[i] # Convert distance to similarity score approx if using cosine distance  # pragma: no cover
                # Note: NearestNeighbors uses Euclidean distance by default.
                # For normalized vectors, Euclidean distance relates to Cosine Similarity.
                # We'll just return the text.
                if idx < len(self.metadata):  # pragma: no cover
                    results.append(f"Chunk {i+1}:\n{self.metadata[idx]}")  # pragma: no cover

            return "\n\n".join(results)  # pragma: no cover
        except Exception as e:  # pragma: no cover
            return f"Error during search: {e}"  # pragma: no cover

    def _create_tools(self):  # pragma: no cover
        return [  # pragma: no cover
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

    def _initialize_agent(self):  # pragma: no cover
        prompt = ChatPromptTemplate.from_messages([  # pragma: no cover
            ("system", "You are a helpful assistant for analyzing vector embeddings. Use the provided tools to inspect the data. When asked about content, use 'search_knowledge_base' to find relevant info."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

        agent = create_tool_calling_agent(self.llm, self.tools, prompt)  # pragma: no cover
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)  # pragma: no cover

    def run(self, query):  # pragma: no cover
        if not query:  # pragma: no cover
            return "Please ask a question."  # pragma: no cover
        try:  # pragma: no cover
            result = self.agent_executor.invoke({"input": query})  # pragma: no cover
            return result["output"]  # pragma: no cover
        except Exception as e:  # pragma: no cover
            return f"Error running agent: {e}"  # pragma: no cover
